import argparse
from typing import Any, Dict

import torch
import yaml

from .algo.sac_agent import SACAgent
from .algo.utils import set_seed
from .envs.make_env import make_vec_env


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained SAC policy")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--config", type=str, default="configs/default.yaml")
    parser.add_argument("--episodes", type=int, default=10)
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg: Dict[str, Any] = yaml.safe_load(f)

    eval_env = make_vec_env(cfg["env"], num_envs=1, eval_mode=True)
    seed = cfg.get("algo", {}).get("seed", 0)
    set_seed(seed)

    obs_space = eval_env.single_observation_space
    act_space = eval_env.single_action_space
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    agent = SACAgent(obs_space, act_space, cfg["algo"], device)
    actor_state = torch.load(args.checkpoint, map_location=device)
    agent.actor.load_state_dict(actor_state)
    agent.actor.eval()

    returns = []
    for ep in range(args.episodes):
        obs, _ = eval_env.reset()
        total_reward = 0.0
        while True:
            with torch.no_grad():
                action, _ = agent.actor.sample(torch.as_tensor(obs, dtype=torch.float32, device=device))
            next_obs, reward, terminated, truncated, info = eval_env.step(action.cpu().numpy())
            total_reward += float(reward[0])
            done = bool(terminated[0] or truncated[0])
            obs = next_obs
            if done:
                break
        returns.append(total_reward)
        print(f"Episode {ep + 1}/{args.episodes}: return={total_reward:.2f}")

    avg_return = sum(returns) / len(returns) if returns else 0.0
    print(f"Average return over {args.episodes} episodes: {avg_return:.2f}")


if __name__ == "__main__":
    main()
