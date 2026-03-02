import argparse, torch, yaml, time, gymnasium as gym
from sac_rl.algo.sac_agent import SACAgent

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--config", default="configs/mujoco_humanoid.yaml")
    p.add_argument("--episodes", type=int, default=3)
    p.add_argument("--deterministic", action="store_true")
    args = p.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    env = gym.make(cfg["env"]["name"], render_mode="human", terminate_when_unhealthy=False)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    obs_space = env.observation_space
    act_space = env.action_space
    agent = SACAgent(obs_space, act_space, cfg["algo"], device)
    actor_state = torch.load(args.checkpoint, map_location=device)
    agent.actor.load_state_dict(actor_state)
    agent.actor.eval()

    for _ in range(args.episodes):
        obs, _ = env.reset()
        ret = 0.0
        while True:
            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=device)
            if obs_t.ndim == 1:
                obs_t = obs_t.unsqueeze(0)
            with torch.no_grad():
                if args.deterministic and hasattr(agent, "act"):
                    a_t, _ = agent.act(obs_t, deterministic=True)
                else:
                    a_t, _ = agent.actor.sample(obs_t)
            a_np = a_t.detach().cpu().numpy()
            if a_np.ndim == 2:
                a_np = a_np[0]
            obs, rew, term, trunc, info = env.step(a_np)
            env.render()
            ret += float(rew)
            if bool(term or trunc):
                print(f"episode_return={ret:.2f}")
                break
            time.sleep(1/60)
    env.close()

if __name__ == "__main__":
    main()
