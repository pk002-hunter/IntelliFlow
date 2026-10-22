"""
PPO Training and Evaluation Pipeline for Traffic Signal Control.
"""
import os
import sys
import argparse
import numpy as np
import pandas as pd

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from src.environment.sumo_env import SumoTrafficEnv, make_env


def train_ppo(
    total_timesteps: int = 15000,
    network: str = "single",
    config_path: Optional[str] = None,
    save_dir: Optional[str] = None,
    log_dir: Optional[str] = None,
    metrics_path: Optional[str] = None,
    seed: int = 42,
    gui: bool = False
):
    """
    Trains a PPO agent on SumoTrafficEnv and evaluates its performance against baselines.
    """
    if save_dir is None:
        save_dir = f"results/models/ppo/{network}" if network != "single" else "results/models/ppo"
    if log_dir is None:
        log_dir = f"results/logs/ppo/{network}" if network != "single" else "results/logs/ppo"
    if metrics_path is None:
        metrics_path = f"results/metrics/ppo_{network}.csv" if network != "single" else "results/metrics/ppo_baseline.csv"

    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)

    print("\n========================================================")
    print(f"  IntelliFlow [Traffic Signal Control] PPO Training: {network.upper()}")
    print(f"  Total Timesteps: {total_timesteps} | Seed: {seed}")
    print(f"  Model Save Directory: {save_dir}")
    print("========================================================\n")

    # Initialize Training Environment (720 steps = 3600s with delta_time=5)
    train_env = make_env(
        network=network,
        config_path=config_path,
        gui=gui,
        max_steps=3600,
        delta_time=5
    )

    # Initialize PPO Model with traffic-optimized actor-critic hyperparameters
    model = PPO(
        policy="MlpPolicy",
        env=train_env,
        learning_rate=3e-4,
        n_steps=720,
        batch_size=72,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        vf_coef=0.5,
        max_grad_norm=0.5,
        verbose=1,
        seed=seed,
        tensorboard_log=log_dir,
        policy_kwargs=dict(net_arch=dict(pi=[128, 128], vf=[128, 128]))
    )

    # Checkpoint callback
    checkpoint_callback = CheckpointCallback(
        save_freq=max(720, total_timesteps // 5),
        save_path=save_dir,
        name_prefix="ppo_ckpt"
    )

    print("Beginning PPO model training...")
    try:
        model.learn(
            total_timesteps=total_timesteps,
            callback=checkpoint_callback,
            progress_bar=True
        )
        print("Training finished successfully.")
    finally:
        train_env.close()

    final_model_path = os.path.join(save_dir, "ppo_final.zip")
    model.save(final_model_path)
    print(f"Final PPO model saved to {final_model_path}")

    # Evaluate the trained policy for 1 full episode (3600 steps)
    print("\nEvaluating trained PPO agent for baseline comparison...")
    evaluate_ppo_agent(model, network=network, config_path=config_path, metrics_path=metrics_path, gui=gui)


def evaluate_ppo_agent(model, network: str = "single", config_path: Optional[str] = None, metrics_path: Optional[str] = None, gui: bool = False):
    """
    Runs a full 3600-second evaluation episode and exports CSV metrics.
    """
    if metrics_path is None:
        metrics_path = f"results/metrics/ppo_{network}.csv" if network != "single" else "results/metrics/ppo_baseline.csv"
    tripinfo_path = f"results/metrics/ppo_{network}_tripinfo.xml" if network != "single" else "results/metrics/ppo_tripinfo.xml"

    eval_env = make_env(
        network=network,
        config_path=config_path,
        max_steps=3600,
        delta_time=5,
        tripinfo_output=tripinfo_path,
        gui=gui
    )

    metrics = []
    try:
        obs, info = eval_env.reset(seed=123)
        terminated = False
        step_idx = 0

        while not terminated:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, step_info = eval_env.step(action)
            step_idx += 1

            # Log metrics every 10 simulation seconds
            sim_time = step_info["sim_step"]
            if sim_time % 10 == 0 or terminated:
                metrics.append({
                    "step": sim_time,
                    "halting_vehicles": step_info["total_halting"],
                    "mean_speed": step_info["mean_speed"],
                    "waiting_time": step_info["total_waiting_time"],
                    "reward": reward,
                    "co2_emissions": step_info["co2_emissions"]
                })

        df = pd.DataFrame(metrics)
        df.to_csv(metrics_path, index=False)
        print(f"Evaluation metrics saved to {metrics_path}")
        if "episode_summary" in step_info:
            print("\n--- Episode Summary ---")
            for k, v in step_info["episode_summary"].items():
                print(f"  {k}: {v:.2f}")

    finally:
        eval_env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train PPO Agent on SUMO Traffic Signal Environment")
    parser.add_argument("--network", type=str, choices=["single", "mukhani"], default="single", help="Network type: 'single' or 'mukhani'")
    parser.add_argument("--timesteps", type=int, default=10000, help="Total training timesteps")
    parser.add_argument("--config", type=str, default=None, help="SUMO config path (optional override)")
    parser.add_argument("--save-dir", type=str, default=None, help="Directory to save model weights")
    parser.add_argument("--metrics-path", type=str, default=None, help="Evaluation metrics CSV path")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--gui", action="store_true", help="Launch with SUMO-GUI")
    args = parser.parse_args()

    train_ppo(
        total_timesteps=args.timesteps,
        network=args.network,
        config_path=args.config,
        save_dir=args.save_dir,
        metrics_path=args.metrics_path,
        seed=args.seed,
        gui=args.gui
    )
