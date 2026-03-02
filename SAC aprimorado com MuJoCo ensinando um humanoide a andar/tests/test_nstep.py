import numpy as np
import torch

from sac_rl.algo.replay_buffer import ReplayBuffer

def test_n_step_returns():
    obs_dim, act_dim = 2, 1
    device = torch.device("cpu")
    rb = ReplayBuffer(obs_dim, act_dim, capacity=10, device=device, n_step=3, gamma=1.0)
    for i in range(3):
        obs = np.array([i, i], dtype=np.float32)
        act = np.array([0.0], dtype=np.float32)
        rb.push(obs, act, reward=1.0, next_obs=obs + 1, done=False)
    assert rb.size == 1
    sample = rb.sample(1)
    rew = sample["rew"][0].item()
    assert abs(rew - 3.0) < 1e-5
    done_flag = sample["done"][0].item()
    assert done_flag == 0.0
    rb2 = ReplayBuffer(obs_dim, act_dim, capacity=10, device=device, n_step=3, gamma=1.0)
    rb2.push(np.zeros(2, dtype=np.float32), np.zeros(1, dtype=np.float32), 1.0, np.zeros(2, dtype=np.float32), True)
    rb2.push(np.ones(2, dtype=np.float32), np.zeros(1, dtype=np.float32), 1.0, np.ones(2, dtype=np.float32), False)
    assert rb2.size == 0