"""
IntelliFlow 🚦 Live SUMO-GUI Visual Simulation Demo.
Runs trained RL models (or baseline controllers) live inside SUMO-GUI on your desktop.
"""
import os
import sys
import time
import argparse

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from stable_baselines3 import PPO, DQN
from src.environment.sumo_env import make_env


def run_live_gui_demo(
    network: str = "mukhani",
    agent: str = "ppo",
    delay: int = 60,
    steps: int = 1200
):
    """
    Launches SUMO-GUI with real-time visual playback and active AI signal control.
    """
    print("\n========================================================")
    print("  IntelliFlow 🚦 Live SUMO-GUI Visual Simulation Demo")
    print(f"  Network: {network.upper()} | Controller: {agent.upper()}")
    print(f"  Visual Step Delay: {delay}ms | Max Steps: {steps}")
    print("========================================================\n")

    # 1. Locate Model Weights if RL agent requested
    model = None
    if agent.lower() == "ppo":
        model_path = os.path.join(PROJECT_ROOT, "results", "models", "ppo", network if network != "single" else "", "ppo_final.zip")
        if not os.path.exists(model_path):
            model_path = os.path.join(PROJECT_ROOT, "results", "models", "ppo", "ppo_final.zip")
        if os.path.exists(model_path):
            print(f"Loading trained PPO weights from: {model_path}")
            model = PPO.load(model_path)
        else:
            print(f"Warning: PPO weights not found at {model_path}. Running with random/heuristic actions.")
    elif agent.lower() == "dqn":
        model_path = os.path.join(PROJECT_ROOT, "results", "models", "dqn", network if network != "single" else "", "dqn_final.zip")
        if not os.path.exists(model_path):
            model_path = os.path.join(PROJECT_ROOT, "results", "models", "dqn", "dqn_final.zip")
        if os.path.exists(model_path):
            print(f"Loading trained DQN weights from: {model_path}")
            model = DQN.load(model_path)
        else:
            print(f"Warning: DQN weights not found at {model_path}. Running with random actions.")

    # 2. Instantiate Environment with GUI enabled
    print("\nLaunching SUMO-GUI window on your desktop screen...")
    print("Note: If the simulation window does not pop up in foreground, check your Windows taskbar.")
    
    env = make_env(
        network=network,
        gui=True,
        gui_delay=delay,
        max_steps=steps,
        delta_time=5
    )

    try:
        obs, info = env.reset(seed=42)
        terminated = False
        step_idx = 0

        print("\n[ACTIVE SIMULATION RUNNING]")
        print("Time (s) | Active Phase | Queued Cars | Avg Speed (km/h) | Ambulance Status")
        print("-" * 75)

        phase_names = {
            0: "Kaladhungi Rd Green (EW)" if network == "mukhani" else "North-South Green",
            1: "Canal/Chhoti Green (NS)" if network == "mukhani" else "East-West Green"
        }

        while not terminated and step_idx * 5 < steps:
            if model is not None:
                action, _ = model.predict(obs, deterministic=True)
            elif agent.lower() == "fixed":
                # Fixed 30s cycle
                action = 0 if (step_idx // 6) % 2 == 0 else 1
            else:
                action = env.action_space.sample()

            obs, reward, terminated, truncated, step_info = env.step(action)
            step_idx += 1

            sim_time = step_info["sim_step"]
            cur_phase = step_info["current_phase"]
            queue = step_info["total_halting"]
            speed = step_info["mean_speed"] * 3.6

            # Check if ambulance is currently in network
            amb_status = "None"
            try:
                for v in env.conn.vehicle.getIDList():
                    if env.conn.vehicle.getVehicleClass(v) == "emergency":
                        wait = env.conn.vehicle.getWaitingTime(v)
                        amb_status = f"APPROACHING (Wait: {wait:.0f}s)" if wait > 0 else "FLOWING (Priority Green)"
                        break
            except Exception:
                pass

            if sim_time % 10 == 0:
                print(f" {sim_time:>6}s | {phase_names.get(cur_phase, str(cur_phase)):<24} | {queue:>10.0f} | {speed:>16.1f} | {amb_status}")

            time.sleep(0.01)

        print("\nSimulation run complete.")

    except KeyboardInterrupt:
        print("\nSimulation demo interrupted by user.")
    finally:
        env.close()
        print("SUMO-GUI session closed cleanly.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live SUMO-GUI Visual Simulation Demo")
    parser.add_argument("--network", type=str, choices=["single", "mukhani"], default="mukhani", help="Road network to visualize")
    parser.add_argument("--agent", type=str, choices=["ppo", "dqn", "fixed"], default="ppo", help="Controller type")
    parser.add_argument("--delay", type=int, default=60, help="Simulation step delay in ms for visible motion (default: 60)")
    parser.add_argument("--steps", type=int, default=1800, help="Total simulation seconds to run")
    args = parser.parse_args()

    run_live_gui_demo(
        network=args.network,
        agent=args.agent,
        delay=args.delay,
        steps=args.steps
    )
