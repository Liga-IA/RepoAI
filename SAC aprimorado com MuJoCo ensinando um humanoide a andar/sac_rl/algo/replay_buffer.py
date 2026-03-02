from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Tuple

import numpy as np
import torch


class ReplayBuffer:
    def __init__(
        self,
        obs_dim: int,
        act_dim: int,
        capacity: int,
        device: torch.device,
        n_step: int = 1,
        gamma: float = 0.99,
    ) -> None:
        self.obs_buf = np.zeros((capacity, obs_dim), dtype=np.float32)
        self.act_buf = np.zeros((capacity, act_dim), dtype=np.float32)
        self.rew_buf = np.zeros((capacity,), dtype=np.float32)
        self.next_obs_buf = np.zeros((capacity, obs_dim), dtype=np.float32)
        self.done_buf = np.zeros((capacity,), dtype=np.float32)
        self.capacity = capacity
        self.device = device
        self.n_step = n_step
        self.gamma = gamma
        self.n_step_buffer: Deque[Tuple[np.ndarray, np.ndarray, float, np.ndarray, bool]] = deque(
            maxlen=n_step
        )
        self.ptr = 0
        self.size = 0

    def _get_n_step_info(self) -> Tuple[np.ndarray, float, np.ndarray, bool]:
        reward, next_state, done = 0.0, self.n_step_buffer[-1][3], False
        for idx, (_, _, r, ns, d) in enumerate(self.n_step_buffer):
            reward += (self.gamma**idx) * r
            if d:
                next_state = ns
                done = True
                break
        return next_state, reward, done

    def push(
        self, obs: np.ndarray, act: np.ndarray, reward: float, next_obs: np.ndarray, done: bool
    ) -> None:
        transition = (obs, act, reward, next_obs, done)
        self.n_step_buffer.append(transition)
        if len(self.n_step_buffer) < self.n_step:
            return
        first_obs, first_act, _, _, _ = self.n_step_buffer[0]
        next_state, ret, d = self._get_n_step_info()
        self.obs_buf[self.ptr] = first_obs
        self.act_buf[self.ptr] = first_act
        self.rew_buf[self.ptr] = ret
        self.next_obs_buf[self.ptr] = next_state
        self.done_buf[self.ptr] = float(d)
        self.ptr = (self.ptr + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)
        if done:
            self.n_step_buffer.clear()

    def sample(self, batch_size: int) -> Dict[str, torch.Tensor]:
        idxs = np.random.randint(0, self.size, size=batch_size)
        obs = torch.as_tensor(self.obs_buf[idxs], device=self.device)
        act = torch.as_tensor(self.act_buf[idxs], device=self.device)
        rew = torch.as_tensor(self.rew_buf[idxs], device=self.device).unsqueeze(-1)
        next_obs = torch.as_tensor(self.next_obs_buf[idxs], device=self.device)
        done = torch.as_tensor(self.done_buf[idxs], device=self.device).unsqueeze(-1)
        return {"obs": obs, "act": act, "rew": rew, "next_obs": next_obs, "done": done}

    def save(self, path: str) -> None:
        size = int(self.size)
        data = {
            "obs": torch.from_numpy(self.obs_buf[:size]),
            "act": torch.from_numpy(self.act_buf[:size]),
            "rew": torch.from_numpy(self.rew_buf[:size]),
            "next_obs": torch.from_numpy(self.next_obs_buf[:size]),
            "done": torch.from_numpy(self.done_buf[:size]),
            "ptr": int(self.ptr),
            "size": size,
            "capacity": int(self.capacity),
            "n_step": int(self.n_step),
            "gamma": float(self.gamma),
        }
        torch.save(data, path)

    def load(self, path: str) -> None:
        data = torch.load(path, map_location="cpu", weights_only=True)
        size = int(data["size"])
        self.obs_buf[:size] = data["obs"].cpu().numpy()
        self.act_buf[:size] = data["act"].cpu().numpy()
        self.rew_buf[:size] = data["rew"].cpu().numpy()
        self.next_obs_buf[:size] = data["next_obs"].cpu().numpy()
        self.done_buf[:size] = data["done"].cpu().numpy()
        self.ptr = int(data["ptr"])
        self.size = size