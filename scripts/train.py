"""
IntelliFlow 🚦 Unified RL Training CLI Entrypoint.
Enables training DQN or PPO agents with a single command.
"""
import os
import sys
import argparse

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.agents.dqn.train_dqn import train_dqn
from src.agents.ppo.train_ppo import train_ppo


def main():
    parser = argparse.ArgumentParser(description="IntelliFlow RL Training CLI")
    parser.add_argument(
        "--network",
        type=str,
        choices=["single", "mukhani", "haldwani"],
        default="single",
        help="Road network: 'single' (generic 4-way), 'mukhani' (Mukhani Chauraha), or 'haldwani' (Full City Network)"
    )
    parser.add_argument(
        "--agent",
        type=str,
        choices=["dqn", "ppo"],
        default="dqn",
        help="RL algorithm to train ('dqn' or 'ppo')"
    )
    parser.add_argument(
        "--timesteps",
        type=int,
        default=10000,
        help="Total training timesteps (default: 10000)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Optional path to custom SUMO configuration file"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for environment and policy reproducibility"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Enable 2D SUMO-GUI during training/evaluation"
    )

    args = parser.parse_args()

    if args.agent == "dqn":
        train_dqn(
            total_timesteps=args.timesteps,
            network=args.network,
            config_path=args.config,
            seed=args.seed,
            gui=args.gui
        )
    elif args.agent == "ppo":
        train_ppo(
            total_timesteps=args.timesteps,
            network=args.network,
            config_path=args.config,
            seed=args.seed,
            gui=args.gui
        )


if __name__ == "__main__":
    main()
