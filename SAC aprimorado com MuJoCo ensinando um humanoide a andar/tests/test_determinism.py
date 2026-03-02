import random
import numpy as np
import torch

from sac_rl.algo.utils import set_seed

def test_set_seed_determinism():
    set_seed(123)
    r1 = random.random()
    n1 = np.random.rand()
    t1 = torch.rand(1).item()
    set_seed(123)
    r2 = random.random()
    n2 = np.random.rand()
    t2 = torch.rand(1).item()
    assert r1 == r2
    assert n1 == n2
    assert abs(t1 - t2) < 1e-6