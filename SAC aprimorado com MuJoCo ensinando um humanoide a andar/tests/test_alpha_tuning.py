import gymnasium as gym
import numpy as np
import torch

from sac_rl.algo.sac_agent import SACAgent

def _make_batch(agent, batch_size: int = 4):
    obs = torch.zeros((batch_size, agent.obs_space.shape[0]), dtype=torch.float32, device=agent.device)
    act = torch.zeros((batch_size, agent.act_space.shape[0]), dtype=torch.float32, device=agent.device)
    rew = torch.zeros((batch_size, 1), dtype=torch.float32, device=agent.device)
    next_obs = torch.zeros_like(obs)
    done = torch.zeros((batch_size, 1), dtype=torch.float32, device=agent.device)
    return {"obs": obs, "act": act, "rew": rew, "next_obs": next_obs, "done": done}

def test_alpha_increase_decrease():
    obs_space = gym.spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)
    act_space = gym.spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)
    device = torch.device("cpu")
    cfg_dec = {"target_entropy": -1.0, "lr_alpha": 0.1, "lr_actor": 0.001, "lr_critic": 0.001}
    agent_dec = SACAgent(obs_space, act_space, cfg_dec, device)
    batch = _make_batch(agent_dec)
    alpha_before = agent_dec.alpha.item()
    agent_dec.update(batch)
    alpha_after = agent_dec.alpha.item()
    assert alpha_after < alpha_before
    cfg_inc = {"target_entropy": 1.0, "lr_alpha": 0.1, "lr_actor": 0.001, "lr_critic": 0.001}
    agent_inc = SACAgent(obs_space, act_space, cfg_inc, device)
    batch = _make_batch(agent_inc)
    alpha_before = agent_inc.alpha.item()
    agent_inc.update(batch)
    alpha_after = agent_inc.alpha.item()
    assert alpha_after > alpha_before