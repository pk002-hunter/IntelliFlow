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
        if not os.path.exists(model_path) and network == "haldwani":
            model_path = os.path.join(PROJECT_ROOT, "results", "models", "ppo", "mukhani", "ppo_final.zip")
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

        actuated_current_action = 0
        actuated_time_in_phase = 0

        while not terminated and step_idx * 5 < steps:
            if model is not None:
                action, _ = model.predict(obs, deterministic=True)
            elif agent.lower() == "fixed":
                # Webster's Optimal Split for Mukhani (45s East-West Kaladhungi, 30s North-South Canal Rd)
                if network == "mukhani":
                    cycle_step = step_idx % 15  # 15 steps * 5s = 75s green cycle
                    action = 0 if cycle_step < 9 else 1
                else:
                    action = 0 if (step_idx // 6) % 2 == 0 else 1
            elif agent.lower() == "actuated":
                # Sensor-Actuated Inductive Loop Controller (Min green 10s, Max green 50s, Gap-Out logic)
                actuated_time_in_phase += 5
                active_lanes = []
                if network == "mukhani":
                    if actuated_current_action == 0:
                        active_lanes = ["KW2M_0", "KW2M_1", "KW2M_2", "KE2M_0", "KE2M_1", "KE2M_2"]
                    else:
                        active_lanes = ["CN2M_0", "CN2M_1", "CS2M_0", "CS2M_1"]
                else:
                    active_lanes = env.incoming_lanes[:len(env.incoming_lanes)//2] if actuated_current_action == 0 else env.incoming_lanes[len(env.incoming_lanes)//2:]

                active_queue = 0
                try:
                    active_queue = sum(env.conn.lane.getLastStepHaltingNumber(lane) for lane in active_lanes if lane in env.conn.lane.getIDList())
                except Exception:
                    active_queue = 0

                # Gap-out when queue is clear after min green (10s), or force switch at max green (50s)
                if actuated_time_in_phase >= 10:
                    if active_queue == 0 or actuated_time_in_phase >= 50:
                        actuated_current_action = 1 - actuated_current_action
                        actuated_time_in_phase = 0

                action = actuated_current_action
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
    parser.add_argument("--network", type=str, choices=["single", "mukhani", "haldwani"], default="haldwani", help="Road network to visualize")
    parser.add_argument("--agent", type=str, choices=["ppo", "dqn", "fixed", "actuated"], default="ppo", help="Controller type")
    parser.add_argument("--delay", type=int, default=60, help="Simulation step delay in ms for visible motion (default: 60)")
    parser.add_argument("--steps", type=int, default=1800, help="Total simulation seconds to run")
    args = parser.parse_args()

    run_live_gui_demo(
        network=args.network,
        agent=args.agent,
        delay=args.delay,
        steps=args.steps
    )
