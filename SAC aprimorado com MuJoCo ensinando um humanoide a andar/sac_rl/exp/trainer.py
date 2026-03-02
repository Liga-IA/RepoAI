from __future__ import annotations

import os
from collections import deque
from typing import Any, Dict

import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter

from ..algo.replay_buffer import ReplayBuffer
from ..algo.sac_agent import SACAgent
from ..algo.utils import set_seed
from ..envs.make_env import make_vec_env


class Trainer:

    def __init__(self, cfg: Dict[str, Any]) -> None:
        self.cfg = cfg
        exp_name = cfg.get("log", {}).get("experiment_name", "exp")
        self.run_dir = os.path.join("runs", exp_name)
        self.checkpoint_dir = os.path.join(self.run_dir, "checkpoints")
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        self.num_envs = int(cfg["env"].get("vec_envs", 8))
        self.env = make_vec_env(cfg["env"], num_envs=self.num_envs, eval_mode=False)
        self.use_obs_norm = bool(cfg["algo"].get("obs_norm", False))
        self.use_reward_norm = bool(cfg["algo"].get("reward_norm", False))
        if self.use_obs_norm:
            pass
        if self.use_reward_norm:
            pass
        self.eval_env = make_vec_env(cfg["env"], num_envs=1, eval_mode=True)
        seed = int(cfg.get("algo", {}).get("seed", 0))
        set_seed(seed)
        obs_space = self.env.single_observation_space
        act_space = self.env.single_action_space
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.agent = SACAgent(obs_space, act_space, cfg["algo"], device)
        obs_dim = int(obs_space.shape[0])
        act_dim = int(act_space.shape[0])
        capacity = int(cfg["algo"].get("replay_size", 1_000_000))
        n_step = int(cfg["algo"].get("n_step", 1))
        gamma = float(cfg["algo"].get("gamma", 0.99))
        self.replay = ReplayBuffer(obs_dim, act_dim, capacity, device, n_step, gamma)
        self.batch_size = int(cfg["algo"].get("batch_size", 256))
        self.warmup_steps = int(cfg["algo"].get("warmup_steps", 10_000))
        self.utd = int(cfg["algo"].get("utd", 1))
        self.eval_interval = int(cfg["log"].get("eval_interval", 10_000))
        self.eval_episodes = int(cfg["log"].get("eval_episodes", 5))
        self.checkpoint_interval = int(cfg["log"].get("checkpoint_interval", 50_000))
        self.max_steps = int(cfg["env"].get("max_steps", 1_000_000)) * self.num_envs
        self.writer = SummaryWriter(log_dir=self.run_dir) if cfg["log"].get("tensorboard", True) else None

    def save_checkpoint(self, step: int) -> None:
        actor_path = os.path.join(self.checkpoint_dir, f"actor_{step}.pt")
        torch.save(self.agent.actor.state_dict(), actor_path)
        latest = os.path.join(self.checkpoint_dir, "actor_latest.pt")
        try:
            if os.path.islink(latest):
                os.unlink(latest)
            os.symlink(os.path.basename(actor_path), latest)
        except Exception:
            pass
        if self.cfg.get("log", {}).get("save_replay", True):
            self.replay.save(os.path.join(self.checkpoint_dir, f"replay_{step}.pt"))

    def evaluate(self, step: int) -> None:
        returns = []
        for _ in range(self.eval_episodes):
            obs, _ = self.eval_env.reset()
            total = 0.0
            while True:
                with torch.no_grad():
                    obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.agent.device)
                    if obs_t.ndim == 1:
                        obs_t = obs_t.unsqueeze(0)
                    action, _ = self.agent.act(obs_t, deterministic=True)
                    a = action.detach().cpu().numpy()
                    if a.ndim == 1:
                        a = a[None, :]
                next_obs, reward, terminated, truncated, info = self.eval_env.step(a)
                total += float(reward[0])
                done = bool(terminated[0] or truncated[0])
                obs = next_obs
                if done:
                    break
            returns.append(total)
        avg_return = float(np.mean(returns))
        if self.writer:
            self.writer.add_scalar("eval/return", avg_return, step)
        print(f"Step {step}: eval average return {avg_return:.2f}")

    def train(self) -> None:
        obs, _ = self.env.reset()
        episode_rewards = np.zeros(self.num_envs, dtype=np.float32)
        episode_lengths = np.zeros(self.num_envs, dtype=np.int32)
        returns_queue: deque[float] = deque(maxlen=100)
        for step in range(1, self.max_steps + 1):
            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.agent.device)
            with torch.no_grad():
                action, _ = self.agent.act(obs_t, deterministic=False)
            action_np = action.cpu().numpy()
            next_obs, reward, terminated, truncated, info = self.env.step(action_np)
            done = np.logical_or(terminated, truncated)
            for i in range(self.num_envs):
                self.replay.push(obs[i], action_np[i], reward[i], next_obs[i], bool(done[i]))
            episode_rewards += reward
            episode_lengths += 1
            for i, d in enumerate(done):
                if d:
                    returns_queue.append(float(episode_rewards[i]))
                    episode_rewards[i] = 0.0
                    episode_lengths[i] = 0
            obs = next_obs
            if step > self.warmup_steps and self.replay.size >= self.batch_size:
                for _ in range(self.utd):
                    batch = self.replay.sample(self.batch_size)
                    metrics = self.agent.update(batch)
                    if self.writer:
                        for k, v in metrics.items():
                            self.writer.add_scalar(f"loss/{k}", v, step)
            if self.writer and len(returns_queue) > 0 and step % 1000 == 0:
                self.writer.add_scalar("train/episodic_return", np.mean(returns_queue), step)
            if step % self.eval_interval == 0:
                self.evaluate(step)
            if step % self.checkpoint_interval == 0:
                self.save_checkpoint(step)
        self.save_checkpoint(self.max_steps)
        if self.writer:
            self.writer.close()