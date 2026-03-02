from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from .networks import PolicyNetwork, QNetwork
from .utils import polyak_update


@dataclass
class SACAgent:
    obs_space: Any
    act_space: Any
    cfg: Dict[str, Any]
    device: torch.device

    def __post_init__(self) -> None:
        obs_dim = int(self.obs_space.shape[0])
        act_dim = int(self.act_space.shape[0])
        hidden = tuple(self.cfg.get("hidden_sizes", [256, 256]))
        self.actor = PolicyNetwork(obs_dim, act_dim, hidden).to(self.device)
        self.q1 = QNetwork(obs_dim, act_dim, hidden).to(self.device)
        self.q2 = QNetwork(obs_dim, act_dim, hidden).to(self.device)
        self.q1_target = QNetwork(obs_dim, act_dim, hidden).to(self.device)
        self.q2_target = QNetwork(obs_dim, act_dim, hidden).to(self.device)
        self.q1_target.load_state_dict(self.q1.state_dict())
        self.q2_target.load_state_dict(self.q2.state_dict())
        target_entropy_cfg = self.cfg.get("target_entropy", "auto")
        self.target_entropy = float(target_entropy_cfg) if isinstance(target_entropy_cfg, (int, float)) else -float(act_dim)
        self.log_alpha = torch.nn.Parameter(torch.tensor(0.0, device=self.device))
        self.actor_opt = torch.optim.Adam(self.actor.parameters(), lr=self.cfg.get("lr_actor", 3e-4))
        self.q1_opt = torch.optim.Adam(self.q1.parameters(), lr=self.cfg.get("lr_critic", 3e-4))
        self.q2_opt = torch.optim.Adam(self.q2.parameters(), lr=self.cfg.get("lr_critic", 3e-4))
        self.alpha_opt = torch.optim.Adam([self.log_alpha], lr=self.cfg.get("lr_alpha", 3e-4))
        self.gamma = self.cfg.get("gamma", 0.99)
        self.tau = self.cfg.get("tau", 0.005)
        self.clip_grad_norm = float(self.cfg.get("clip_grad_norm", 1.0))

    @property
    def alpha(self) -> torch.Tensor:
        return self.log_alpha.exp()

    def act(self, obs: torch.Tensor, deterministic: bool = False) -> Tuple[torch.Tensor, torch.Tensor]:
        if deterministic:
            mu, _ = self.actor(obs)
            action = torch.tanh(mu)
            return action, torch.zeros(action.shape[0], 1, device=self.device)
        return self.actor.sample(obs)

    def update(self, batch: Dict[str, torch.Tensor]) -> Dict[str, float]:

        obs, act = batch["obs"], batch["act"]
        rew, next_obs, done = batch["rew"], batch["next_obs"], batch["done"]

        n_step = int(self.cfg.get("n_step", 1))
        with torch.no_grad():
            next_action, next_logp = self.actor.sample(next_obs)
            q1_target = self.q1_target(next_obs, next_action)
            q2_target = self.q2_target(next_obs, next_action)
            min_q_target = torch.min(q1_target, q2_target) - self.alpha * next_logp.squeeze(-1)
            target = rew.squeeze(-1) + (1.0 - done.squeeze(-1)) * (self.gamma ** n_step) * min_q_target

        q1_pred, q2_pred = self.q1(obs, act), self.q2(obs, act)
        q1_loss, q2_loss = F.mse_loss(q1_pred, target), F.mse_loss(q2_pred, target)

        if not torch.isfinite(q1_loss) or not torch.isfinite(q2_loss):
            return {"q1_loss": float("nan"), "q2_loss": float("nan"), "actor_loss": float("nan"), "alpha_loss": float("nan"), "alpha": self.alpha.item(), "nan_skip": 1.0}

        self.q1_opt.zero_grad()
        q1_loss.backward()
        if self.clip_grad_norm > 0:
            torch.nn.utils.clip_grad_norm_(self.q1.parameters(), self.clip_grad_norm)
        self.q1_opt.step()

        self.q2_opt.zero_grad()
        q2_loss.backward()
        if self.clip_grad_norm > 0:
            torch.nn.utils.clip_grad_norm_(self.q2.parameters(), self.clip_grad_norm)
        self.q2_opt.step()

        action_new, logp = self.actor.sample(obs)
        q1_val, q2_val = self.q1(obs, action_new), self.q2(obs, action_new)
        min_q = torch.min(q1_val, q2_val)
        actor_loss = (self.alpha * logp.squeeze(-1) - min_q).mean()

        if not torch.isfinite(actor_loss):
            return {"q1_loss": q1_loss.item(), "q2_loss": q2_loss.item(), "actor_loss": float("nan"), "alpha_loss": float("nan"), "alpha": self.alpha.item(), "nan_skip": 1.0}

        self.actor_opt.zero_grad()
        actor_loss.backward()
        if self.clip_grad_norm > 0:
            torch.nn.utils.clip_grad_norm_(self.actor.parameters(), self.clip_grad_norm)
        self.actor_opt.step()

        alpha_loss = -(self.log_alpha * (logp + self.target_entropy).detach()).mean()
        if not torch.isfinite(alpha_loss):
            return {"q1_loss": q1_loss.item(), "q2_loss": q2_loss.item(), "actor_loss": actor_loss.item(), "alpha_loss": float("nan"), "alpha": self.alpha.item(), "nan_skip": 1.0}

        self.alpha_opt.zero_grad()
        alpha_loss.backward()
        self.alpha_opt.step()

        polyak_update(self.q1, self.q1_target, self.tau)
        polyak_update(self.q2, self.q2_target, self.tau)

        return {"q1_loss": q1_loss.item(), "q2_loss": q2_loss.item(), "actor_loss": actor_loss.item(), "alpha_loss": alpha_loss.item(), "alpha": self.alpha.item()}
