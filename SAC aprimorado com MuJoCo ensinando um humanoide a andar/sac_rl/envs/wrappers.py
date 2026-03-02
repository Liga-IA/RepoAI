from __future__ import annotations

import random
from typing import Any, Dict, Tuple

import gymnasium as gym
import numpy as np


class RunningStat:
    def __init__(self, shape: Tuple[int, ...], eps: float = 1e-4) -> None:
        self.shape = shape
        self.mean = np.zeros(shape, dtype=np.float64)
        self.var = np.ones(shape, dtype=np.float64)
        self.count = eps

    def update(self, x: np.ndarray) -> None:
        batch_mean = np.mean(x, axis=0)
        batch_var = np.var(x, axis=0)
        batch_count = x.shape[0]
        delta = batch_mean - self.mean
        tot_count = self.count + batch_count
        new_mean = self.mean + delta * batch_count / tot_count
        m_a = self.var * self.count
        m_b = batch_var * batch_count
        M2 = m_a + m_b + delta**2 * self.count * batch_count / tot_count
        self.mean = new_mean
        self.var = M2 / tot_count
        self.count = tot_count

    @property
    def std(self) -> np.ndarray:
        return np.sqrt(self.var + 1e-8)


class ObservationNormWrapper(gym.ObservationWrapper):
    def __init__(self, env: gym.Env) -> None:
        super().__init__(env)
        shape = env.observation_space.shape or ()
        self.running_stat = RunningStat(shape)

    def observation(self, observation: np.ndarray) -> np.ndarray:
        obs = np.asarray(observation, dtype=np.float64)
        self.running_stat.update(obs[None, :])
        normed = (obs - self.running_stat.mean) / self.running_stat.std
        return normed.astype(np.float32)


class RewardScaleWrapper(gym.RewardWrapper):
    def __init__(self, env: gym.Env, gamma: float = 0.99) -> None:
        super().__init__(env)
        self.gamma = gamma
        self.running_stat = RunningStat(())
        self.ret = 0.0

    def reward(self, reward: float) -> float:
        self.ret = self.ret * self.gamma + reward
        self.running_stat.update(np.array([[self.ret]]))
        scale = max(self.running_stat.std.item(), 1e-4)
        return float(reward / scale)


class DomainRandomizationWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env, env_cfg: Dict[str, Any]) -> None:
        super().__init__(env)
        self.mass_range = env_cfg.get("mass_range", (0.8, 1.2))
        self.friction_range = env_cfg.get("friction_range", (0.5, 1.5))
        self.slope_range = env_cfg.get("slope_range", (-0.05, 0.05))
        self.action_noise_range = env_cfg.get("action_noise_range", (0.0, 0.05))
        self.random_params: Dict[str, float] = {}

    def reset(self, **kwargs: Any) -> Tuple[np.ndarray, Dict[str, Any]]:
        self.random_params = {
            "mass_multiplier": random.uniform(*self.mass_range),
            "friction_multiplier": random.uniform(*self.friction_range),
            "ground_slope": random.uniform(*self.slope_range),
            "action_noise": random.uniform(*self.action_noise_range),
        }
        setattr(self.env, "_random_params", self.random_params)
        return self.env.reset(**kwargs)

    def step(self, action):
        noise = self.random_params.get("action_noise", 0.0)
        if noise > 0.0:
            noisy_action = action + np.random.uniform(-noise, noise, size=action.shape)
            low = self.env.action_space.low
            high = self.env.action_space.high
            action = np.clip(noisy_action, low, high)
        return self.env.step(action)


class CurriculumWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env, env_cfg: Dict[str, Any]) -> None:
        super().__init__(env)
        self.stage = 0
        self.step_threshold = env_cfg.get("curriculum_step_threshold", 500_000)
        self.return_threshold = env_cfg.get("curriculum_return_threshold", 10.0)
        self.total_steps = 0
        self.episode_returns: float = 0.0

    def reset(self, **kwargs: Any):
        if self.stage == 0 and (
            self.total_steps >= self.step_threshold or self.episode_returns >= self.return_threshold
        ):
            self.stage = 1
        self.episode_returns = 0.0
        return self.env.reset(**kwargs)

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        self.total_steps += 1
        self.episode_returns += reward
        if self.stage == 0:
            reward = min(reward, self.return_threshold)
        return obs, reward, terminated, truncated, info