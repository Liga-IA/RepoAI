import gymnasium as gym
import numpy as np

from sac_rl.envs.wrappers import (
    DomainRandomizationWrapper,
    ObservationNormWrapper,
    CurriculumWrapper,
)

def test_domain_randomization_changes_params():
    env = gym.make("CartPole-v1")
    cfg = {"mass_range": (0.8, 1.2), "friction_range": (0.5, 1.5), "slope_range": (-0.1, 0.1), "action_noise_range": (0.0, 0.01)}
    wrapped = DomainRandomizationWrapper(env, cfg)
    _, _ = wrapped.reset()
    params1 = getattr(wrapped.env, "_random_params")
    _, _ = wrapped.reset()
    params2 = getattr(wrapped.env, "_random_params")
    assert params1 != params2


def test_observation_norm_wrapper():
    env = gym.make("CartPole-v1")
    wrapped = ObservationNormWrapper(env)
    obs, _ = wrapped.reset()
    obs2, reward, terminated, truncated, info = wrapped.step(env.action_space.sample())
    assert not np.allclose(wrapped.running_stat.mean, 0)

def test_curriculum_wrapper_stage_transition():
    env = gym.make("CartPole-v1")
    cfg = {"curriculum_step_threshold": 1, "curriculum_return_threshold": 1.0}
    wrapped = CurriculumWrapper(env, cfg)
    obs, _ = wrapped.reset()
    obs, reward, terminated, truncated, info = wrapped.step(env.action_space.sample())
    obs, _ = wrapped.reset()
    assert wrapped.stage == 1