from __future__ import annotations

import random
from typing import Any, List

import numpy as np
import torch


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def polyak_update(source: torch.nn.Module, target: torch.nn.Module, tau: float) -> None:
    with torch.no_grad():
        for src_param, tgt_param in zip(source.parameters(), target.parameters()):
            tgt_param.data.mul_(1.0 - tau)
            tgt_param.data.add_(tau * src_param.data)


def update_nested_dict(d: dict, keys: List[str], value: Any) -> None:
    for key in keys[:-1]:
        if key not in d or not isinstance(d[key], dict):
            d[key] = {}
        d = d[key]
    d[keys[-1]] = value