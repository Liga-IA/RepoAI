from __future__ import annotations

from typing import Any, Dict, Callable
import gymnasium as gym
from gymnasium.vector import AsyncVectorEnv, VectorEnv
from .wrappers import CurriculumWrapper, DomainRandomizationWrapper, ObservationNormWrapper, RewardScaleWrapper


def _make_single_env(env_cfg: Dict[str, Any], eval_mode: bool = False) -> Callable[[], gym.Env]:
    def _thunk() -> gym.Env:
        name = env_cfg.get("name", "HumanoidBulletEnv-v0")
        max_steps = env_cfg.get("max_steps")
        try:
            env = gym.make(name, max_episode_steps=max_steps)
            return env if eval_mode else _maybe_wrap(env, env_cfg)
        except Exception:
            if ("Bullet" not in name) and ("PyBullet" not in name):
                raise
            import gym as classic_gym
            env_gym = classic_gym.make(name)
            from gymnasium.wrappers.compatibility import EnvCompatibility
            env = EnvCompatibility(env_gym)
            return env if eval_mode else _maybe_wrap(env, env_cfg)
    return _thunk


def _maybe_wrap(env: gym.Env, env_cfg: Dict[str, Any]) -> gym.Env:
    if env_cfg.get("domain_randomization", False):
        env = DomainRandomizationWrapper(env, env_cfg.get("randomization", {}))
    if env_cfg.get("curriculum", False):
        env = CurriculumWrapper(env, env_cfg.get("curriculum_cfg", {}))
    if env_cfg.get("normalize_obs", False):
        env = ObservationNormWrapper(env)
    if env_cfg.get("normalize_reward", False):
        env = RewardScaleWrapper(env)
    return env


def make_vec_env(env_cfg: Dict[str, Any], num_envs: int, eval_mode: bool = False) -> VectorEnv:
    thunks = [_make_single_env(env_cfg, eval_mode) for _ in range(num_envs)]
    vec_env: VectorEnv = AsyncVectorEnv(thunks)
    return vec_env
