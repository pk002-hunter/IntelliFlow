"""
Sensor-Actuated Baseline Signal Controller for SUMO.
Extends green light phases dynamically based on vehicle arrival gaps (Gap-Out logic).
"""
import os
import sys
import shutil
import argparse
import pandas as pd

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    if tools not in sys.path:
        sys.path.append(tools)
else:
    possible_paths = [
        r"C:\Program Files (x86)\Eclipse\Sumo\tools",
        r"C:\Program Files\Eclipse\Sumo\tools",
        r"C:\sumo\tools"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            sys.path.append(path)
            break

try:
    import traci
except ImportError:
    sys.exit("SUMO 'traci' module not found. Ensure SUMO is installed and SUMO_HOME environment variable is set.")


def get_sumo_binary(gui=False):
    """Locate sumo or sumo-gui executable across system paths."""
    binary_name = "sumo-gui.exe" if gui else "sumo.exe"
    if shutil.which(binary_name):
        return binary_name
    if 'SUMO_HOME' in os.environ:
        path = os.path.join(os.environ['SUMO_HOME'], 'bin', binary_name)
        if os.path.exists(path):
            return path
    for base in [r"C:\Program Files (x86)\Eclipse\Sumo", r"C:\Program Files\Eclipse\Sumo", r"C:\sumo"]:
        path = os.path.join(base, "bin", binary_name)
        if os.path.exists(path):
            return path
    return binary_name


def run_actuated_simulation(config_path, min_green=10, max_green=50, total_steps=3600, gui=False):
    """
    Runs sensor-actuated signal control.
    """
    sumo_binary = get_sumo_binary(gui)
    os.makedirs("results/metrics", exist_ok=True)
    sumo_cmd = [sumo_binary, "-c", config_path, "--tripinfo-output", "results/metrics/actuated_tripinfo.xml"]

    print(f"Starting Actuated Simulation using binary: {sumo_binary}")
    traci.start(sumo_cmd)
    
    tl_ids = traci.trafficlight.getIDList()
    if not tl_ids:
        print("No traffic lights found in network.")
        traci.close()
        return

    tl_id = tl_ids[0]
    num_phases = len(traci.trafficlight.getAllProgramLogics(tl_id)[0].phases)
    step = 0
    current_phase = 0
    phase_timer = 0
    metrics = []

    print(f"Simulating actuated control on junction '{tl_id}' for {total_steps} steps...")

    while step < total_steps:
        traci.simulationStep()
        step += 1
        phase_timer += 1

        controlled_lanes = traci.trafficlight.getControlledLanes(tl_id)
        current_queue = sum([traci.lane.getLastStepHaltingNumber(lane) for lane in controlled_lanes])

        if phase_timer >= min_green:
            if current_queue == 0 or phase_timer >= max_green:
                current_phase = (current_phase + 1) % max(1, num_phases)
                traci.trafficlight.setPhase(tl_id, current_phase)
                phase_timer = 0

        if step % 10 == 0:
            halting = sum([traci.edge.getLastStepHaltingNumber(edge) for edge in traci.edge.getIDList()])
            mean_speed = sum([traci.edge.getLastStepMeanSpeed(edge) for edge in traci.edge.getIDList()]) / max(1, len(traci.edge.getIDList()))
            metrics.append({
                "step": step,
                "halting_vehicles": halting,
                "mean_speed": mean_speed
            })

    traci.close()

    df = pd.DataFrame(metrics)
    output_csv = "results/metrics/actuated_baseline.csv"
    df.to_csv(output_csv, index=False)
    print(f"Actuated simulation finished successfully. Results saved to {output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Actuated Signal Control Baseline")
    parser.add_argument("--config", type=str, default="sumo/networks/single_intersection/single_intersection.sumocfg", help="SUMO config file path")
    parser.add_argument("--min-green", type=int, default=10, help="Minimum green time")
    parser.add_argument("--max-green", type=int, default=50, help="Maximum green time")
    parser.add_argument("--steps", type=int, default=3600, help="Total simulation steps")
    parser.add_argument("--gui", action="store_true", help="Run with SUMO-GUI")
    args = parser.parse_args()

    run_actuated_simulation(args.config, args.min_green, args.max_green, args.steps, args.gui)
