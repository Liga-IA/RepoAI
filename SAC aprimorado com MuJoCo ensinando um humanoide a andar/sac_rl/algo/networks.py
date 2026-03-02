from __future__ import annotations

import math
from typing import Tuple

import torch
import torch.nn as nn

def orthogonal_init(layer: nn.Module, gain: float = 1.0) -> None:
    if isinstance(layer, (nn.Linear, nn.Conv2d)):
        nn.init.orthogonal_(layer.weight, gain=gain)
        if layer.bias is not None:
            nn.init.zeros_(layer.bias)


class MLP(nn.Module):
    def __init__(self, input_dim: int, output_dim: int, hidden_sizes: Tuple[int, ...], activation=nn.ReLU) -> None:
        super().__init__()
        layers = []
        last_dim = input_dim
        for h in hidden_sizes:
            linear = nn.Linear(last_dim, h)
            orthogonal_init(linear, gain=math.sqrt(2))
            layers += [linear, activation()]
            last_dim = h
        linear = nn.Linear(last_dim, output_dim)
        orthogonal_init(linear, gain=1.0)
        layers.append(linear)
        self.model = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)


class PolicyNetwork(nn.Module):
    def __init__(self, obs_dim: int, act_dim: int, hidden_sizes: Tuple[int, ...] = (256, 256)) -> None:
        super().__init__()
        self.net = MLP(obs_dim, 2 * act_dim, hidden_sizes)
        self.act_dim = act_dim
        self.log_std_min = -20.0
        self.log_std_max = 2.0

    def forward(self, obs: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        mu_logstd = self.net(obs)
        mu, log_std = mu_logstd.split(self.act_dim, dim=-1)
        log_std = torch.clamp(log_std, self.log_std_min, self.log_std_max)
        return mu, log_std

    def sample(self, obs: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        mu, log_std = self(obs)
        std = torch.exp(log_std)
        normal = torch.distributions.Normal(mu, std)
        z = normal.rsample()
        action = torch.tanh(z)
        eps = 1e-6
        logp = normal.log_prob(z) - torch.log(1 - action.pow(2) + eps)
        logp = logp.sum(dim=-1, keepdim=True)
        return action, logp


class QNetwork(nn.Module):
    def __init__(self, obs_dim: int, act_dim: int, hidden_sizes: Tuple[int, ...] = (256, 256)) -> None:
        super().__init__()
        self.net = MLP(obs_dim + act_dim, 1, hidden_sizes)

    def forward(self, obs: torch.Tensor, act: torch.Tensor) -> torch.Tensor:
        x = torch.cat([obs, act], dim=-1)
        q = self.net(x)
        return q.squeeze(-1)
