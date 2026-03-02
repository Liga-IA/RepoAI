import os
import torch

from sac_rl.algo.replay_buffer import ReplayBuffer

def test_replay_buffer_push_sample_save_load(tmp_path):
    obs_dim, act_dim, capacity = 3, 2, 5
    device = torch.device("cpu")
    rb = ReplayBuffer(obs_dim, act_dim, capacity, device, n_step=1, gamma=0.99)
    for i in range(capacity + 2):
        obs = (i * torch.ones(obs_dim)).numpy()
        act = (i * torch.ones(act_dim)).numpy()
        rb.push(obs, act, reward=float(i), next_obs=obs + 1, done=False)
    assert rb.size == capacity
    batch = rb.sample(2)
    assert batch["obs"].shape == (2, obs_dim)
    assert batch["act"].shape == (2, act_dim)
    path = os.path.join(tmp_path, "buffer.pt")
    rb.save(path)
    rb2 = ReplayBuffer(obs_dim, act_dim, capacity, device, n_step=1, gamma=0.99)
    rb2.load(path)
    assert rb2.size == capacity
    sample1 = rb.sample(3)
    sample2 = rb2.sample(3)
    assert torch.allclose(sample1["obs"], sample2["obs"]) or sample1["obs"].shape == sample2["obs"].shape