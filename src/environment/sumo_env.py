"""
Gymnasium SUMO Traffic Signal Control Environment.
Wraps Eclipse SUMO and TraCI into a standard Gymnasium environment compatible with Stable-Baselines3.
"""
import os
import sys
import uuid
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Optional, Dict, Any, Tuple, List

try:
    from ..utils.sumo_utils import setup_sumo_path, get_sumo_binary
except (ImportError, ValueError):
    try:
        from src.utils.sumo_utils import setup_sumo_path, get_sumo_binary
    except ImportError:
        from utils.sumo_utils import setup_sumo_path, get_sumo_binary

setup_sumo_path()

try:
    import traci
except ImportError:
    traci = None


class SumoTrafficEnv(gym.Env):
    """
    Custom Gymnasium Environment for 4-Way Traffic Signal Control using SUMO.
    
    Action Space:
        Discrete(2):
            0: North-South Green (Phase 0: GGGgrrrrGGGgrrrr)
            1: East-West Green   (Phase 2: rrrrGGGgrrrrGGGg)

    Observation Space:
        Box(35,) float32 in range [0, 1]:
            For each of 8 incoming lanes (N2C_0, N2C_1, S2C_0, S2C_1, E2C_0, E2C_1, W2C_0, W2C_1):
                - Halting vehicles / max_capacity (normalized)
                - Mean speed / max_speed (normalized)
                - Accumulated waiting time / 300.0 (normalized)
                - Vehicle count / max_capacity (normalized)
            Traffic light status:
                - One-hot phase indicator [NS_green, EW_green] (2 dims)
                - Elapsed seconds in current green phase / 100.0 (1 dim)
    """

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}

    # Signal Phase Index Mapping from single_intersection.net.xml
    PHASE_NS_GREEN = 0
    PHASE_NS_YELLOW = 1
    PHASE_EW_GREEN = 2
    PHASE_EW_YELLOW = 3

    INCOMING_LANES = [
        "N2C_0", "N2C_1",
        "S2C_0", "S2C_1",
        "E2C_0", "E2C_1",
        "W2C_0", "W2C_1"
    ]
    
    INCOMING_EDGES = ["N2C", "S2C", "E2C", "W2C"]
    OUTGOING_EDGES = ["C2N", "C2S", "C2E", "C2W"]

    def __init__(
        self,
        net_file: str = "sumo/networks/single_intersection/single_intersection.net.xml",
        route_file: str = "sumo/networks/single_intersection/single_intersection.rou.xml",
        cfg_file: Optional[str] = "sumo/networks/single_intersection/single_intersection.sumocfg",
        tls_id: str = "C",
        incoming_lanes: Optional[List[str]] = None,
        incoming_edges: Optional[List[str]] = None,
        phase_ns_green: Optional[int] = None,
        phase_ns_yellow: Optional[int] = None,
        phase_ew_green: Optional[int] = None,
        phase_ew_yellow: Optional[int] = None,
        delta_time: int = 5,
        yellow_duration: int = 3,
        min_green: int = 5,
        max_steps: int = 3600,
        gui: bool = False,
        gui_delay: int = 50,
        tripinfo_output: Optional[str] = None,
        reward_type: str = "multi_objective",
        reward_weights: Optional[Dict[str, float]] = None,
        starvation_threshold: float = 120.0,
        lane_capacity: float = 25.0,
        max_speed: float = 13.89,
    ):
        super().__init__()

        if traci is None:
            raise ImportError("SUMO 'traci' module is required. Ensure SUMO is installed and SUMO_HOME is set.")

        self.net_file = os.path.abspath(net_file)
        self.route_file = os.path.abspath(route_file)
        self.cfg_file = os.path.abspath(cfg_file) if cfg_file else None
        self.tls_id = tls_id

        # Modular lane, edge, and phase definitions
        self.incoming_lanes = incoming_lanes if incoming_lanes is not None else list(self.INCOMING_LANES)
        self.incoming_edges = incoming_edges if incoming_edges is not None else list(self.INCOMING_EDGES)
        self.phase_ns_green = phase_ns_green if phase_ns_green is not None else self.PHASE_NS_GREEN
        self.phase_ns_yellow = phase_ns_yellow if phase_ns_yellow is not None else self.PHASE_NS_YELLOW
        self.phase_ew_green = phase_ew_green if phase_ew_green is not None else self.PHASE_EW_GREEN
        self.phase_ew_yellow = phase_ew_yellow if phase_ew_yellow is not None else self.PHASE_EW_YELLOW

        self.delta_time = int(delta_time)
        self.yellow_duration = int(yellow_duration)
        self.min_green = int(min_green)
        self.max_steps = int(max_steps)
        self.gui = gui
        self.gui_delay = int(gui_delay)
        self.tripinfo_output = tripinfo_output
        self.reward_type = reward_type
        self.starvation_threshold = starvation_threshold
        self.lane_capacity = float(lane_capacity)
        self.max_speed = float(max_speed)

        # Default Multi-Objective Reward Weights
        self.reward_weights = {
            "queue": 1.0,         # Penalty for halted vehicles
            "waiting_time": 0.02, # Penalty for accumulated waiting seconds
            "speed": 0.5,         # Bonus for throughput speed
            "emissions": 0.0001,  # Penalty for CO2 emissions (mg/s)
            "switch": 1.5,        # Penalty for changing phase
            "starvation": 0.05    # Penalty for vehicles waiting > starvation_threshold
        }
        if reward_weights:
            self.reward_weights.update(reward_weights)

        # Action: 0 = NS Green, 1 = EW Green
        self.action_space = spaces.Discrete(2)

        # Observation: dynamic lanes * 4 features + 2 (one-hot phase) + 1 (phase duration)
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(len(self.incoming_lanes) * 4 + 3,),
            dtype=np.float32
        )

        # Internal Simulation State
        self.conn = None
        self.conn_label = None
        self.sim_step = 0
        self.current_green_phase = 0  # 0: NS Green, 1: EW Green
        self.time_in_phase = 0
        self.is_closed = True
        
        # Episode metrics accumulators
        self.episode_rewards = []
        self.episode_halting = []
        self.episode_waiting_times = []
        self.episode_speeds = []
        self.episode_co2 = []

    def _get_sumo_cmd(self, seed: Optional[int] = None) -> List[str]:
        """Construct the SUMO command arguments list."""
        binary = get_sumo_binary(self.gui)
        cmd = [binary]

        if self.cfg_file and os.path.exists(self.cfg_file):
            cmd.extend(["-c", self.cfg_file])
        else:
            cmd.extend(["-n", self.net_file, "-r", self.route_file])

        cmd.extend([
            "--no-step-log", "true",
            "--time-to-teleport", "-1",
            "--waiting-time-memory", "1000",
            "--no-warnings", "true"
        ])

        if self.gui:
            cmd.extend(["--start", "--delay", str(self.gui_delay)])

        if seed is not None:
            cmd.extend(["--seed", str(seed)])

        if self.tripinfo_output:
            os.makedirs(os.path.dirname(os.path.abspath(self.tripinfo_output)), exist_ok=True)
            cmd.extend(["--tripinfo-output", self.tripinfo_output])

        return cmd

    def reset(self, seed: Optional[int] = None, options: Optional[Dict[str, Any]] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Resets the SUMO simulation environment."""
        super().reset(seed=seed)
        self.close()

        self.conn_label = f"sumo_env_{uuid.uuid4().hex[:8]}"
        cmd = self._get_sumo_cmd(seed=seed)

        traci.start(cmd, label=self.conn_label)
        self.conn = traci.getConnection(self.conn_label)
        self.is_closed = False

        self.sim_step = 0
        self.current_green_phase = 0  # Action 0 starts active
        self.time_in_phase = 0
        self.conn.trafficlight.setPhase(self.tls_id, self.phase_ns_green)

        # Reset episode trackers
        self.episode_rewards = []
        self.episode_halting = []
        self.episode_waiting_times = []
        self.episode_speeds = []
        self.episode_co2 = []

        obs = self._get_observation()
        info = self._get_info()
        return obs, info

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Executes one RL step (advances simulation by delta_time seconds with yellow transitions).
        """
        if self.is_closed or self.conn is None:
            raise RuntimeError("Environment is closed. Call reset() before stepping.")

        action = int(action)
        switched = False

        # Phase Transition Logic
        if action != self.current_green_phase:
            if self.time_in_phase >= self.min_green:
                # Transition yellow phase
                yellow_phase = self.phase_ns_yellow if self.current_green_phase == 0 else self.phase_ew_yellow
                self.conn.trafficlight.setPhase(self.tls_id, yellow_phase)
                
                # Advance yellow interval
                for _ in range(self.yellow_duration):
                    self.conn.simulationStep()
                    self.sim_step += 1

                # Set new green phase
                new_green_phase = self.phase_ns_green if action == 0 else self.phase_ew_green
                self.conn.trafficlight.setPhase(self.tls_id, new_green_phase)
                self.current_green_phase = action
                self.time_in_phase = 0
                switched = True

                # Advance remaining green steps in this RL cycle
                green_duration = max(1, self.delta_time - self.yellow_duration)
                for _ in range(green_duration):
                    self.conn.simulationStep()
                    self.sim_step += 1
                    self.time_in_phase += 1
            else:
                # Minimum green not reached, continue current phase
                for _ in range(self.delta_time):
                    self.conn.simulationStep()
                    self.sim_step += 1
                    self.time_in_phase += 1
        else:
            # Maintain current green phase
            for _ in range(self.delta_time):
                self.conn.simulationStep()
                self.sim_step += 1
                self.time_in_phase += 1

        # Collect Observation, Reward, and Termination Status
        obs = self._get_observation()
        reward, step_metrics = self._compute_reward(switched=switched)
        
        terminated = bool(self.sim_step >= self.max_steps or self.conn.simulation.getMinExpectedNumber() <= 0)
        truncated = False

        # Update episode metrics
        self.episode_rewards.append(reward)
        self.episode_halting.append(step_metrics["total_halting"])
        self.episode_waiting_times.append(step_metrics["total_waiting_time"])
        self.episode_speeds.append(step_metrics["mean_speed"])
        self.episode_co2.append(step_metrics["co2_emissions"])

        info = self._get_info()
        info.update(step_metrics)
        info["action_switched"] = switched

        if terminated:
            info["episode_summary"] = {
                "total_reward": float(np.sum(self.episode_rewards)),
                "mean_reward": float(np.mean(self.episode_rewards)),
                "mean_halting": float(np.mean(self.episode_halting)),
                "mean_waiting_time": float(np.mean(self.episode_waiting_times)),
                "mean_speed": float(np.mean(self.episode_speeds)),
                "total_co2_kg": float(np.sum(self.episode_co2) / 1e6)
            }

        return obs, reward, terminated, truncated, info

    def _get_observation(self) -> np.ndarray:
        """
        Extracts normalized state representation across configured incoming lanes.
        """
        features = []

        for lane_id in self.incoming_lanes:
            try:
                halting = self.conn.lane.getLastStepHaltingNumber(lane_id)
                mean_speed = self.conn.lane.getLastStepMeanSpeed(lane_id)
                waiting_time = self.conn.lane.getWaitingTime(lane_id)
                veh_count = self.conn.lane.getLastStepVehicleNumber(lane_id)
            except Exception:
                halting, mean_speed, waiting_time, veh_count = 0.0, 0.0, 0.0, 0.0

            # Normalize values
            norm_queue = np.clip(halting / self.lane_capacity, 0.0, 1.0)
            norm_speed = np.clip(mean_speed / self.max_speed, 0.0, 1.0)
            norm_wait = np.clip(waiting_time / 300.0, 0.0, 1.0)
            norm_density = np.clip(veh_count / self.lane_capacity, 0.0, 1.0)

            features.extend([norm_queue, norm_speed, norm_wait, norm_density])

        # Traffic light state: One-hot phase [NS, EW]
        phase_onehot = [1.0, 0.0] if self.current_green_phase == 0 else [0.0, 1.0]
        norm_phase_time = np.clip(self.time_in_phase / 100.0, 0.0, 1.0)

        features.extend(phase_onehot)
        features.append(norm_phase_time)

        return np.array(features, dtype=np.float32)

    def _compute_reward(self, switched: bool = False) -> Tuple[float, Dict[str, float]]:
        """
        Multi-objective reward shaping combining queues, delays, speed, emissions, starvation,
        and emergency vehicle (ambulance) priority preemption.
        """
        total_halting = 0.0
        total_waiting = 0.0
        starvation_count = 0.0
        co2_emissions = 0.0
        ambulance_delay = 0.0

        for lane_id in self.incoming_lanes:
            try:
                total_halting += self.conn.lane.getLastStepHaltingNumber(lane_id)
                total_waiting += self.conn.lane.getWaitingTime(lane_id)
                
                # Check vehicles on this lane
                lane_vehs = self.conn.lane.getLastStepVehicleIDs(lane_id)
                for veh in lane_vehs:
                    wait_time = self.conn.vehicle.getWaitingTime(veh)
                    if wait_time > self.starvation_threshold:
                        starvation_count += 1.0
                    # Emergency ambulance preemption check
                    if self.conn.vehicle.getVehicleClass(veh) == "emergency" and wait_time > 0:
                        ambulance_delay += wait_time
            except Exception:
                pass

        # CO2 emissions across configured incoming edges
        for edge_id in self.incoming_edges:
            try:
                co2_emissions += self.conn.edge.getCO2Emission(edge_id)
            except Exception:
                pass

        # Network mean speed
        edge_speeds = []
        for edge_id in self.incoming_edges:
            try:
                edge_speeds.append(self.conn.edge.getLastStepMeanSpeed(edge_id))
            except Exception:
                pass
        mean_speed = np.mean(edge_speeds) if edge_speeds else 0.0

        w = self.reward_weights
        
        # Reward calculation
        reward = (
            - (w["queue"] * total_halting)
            - (w["waiting_time"] * (total_waiting / 10.0))
            - (w["emissions"] * (co2_emissions / 1000.0))
            - (w["starvation"] * starvation_count)
            - (5.0 * ambulance_delay)  # Priority penalty if ambulance is stuck
            + (w["speed"] * (mean_speed / self.max_speed))
            - (w["switch"] * (1.0 if switched else 0.0))
        )

        metrics = {
            "total_halting": float(total_halting),
            "total_waiting_time": float(total_waiting),
            "mean_speed": float(mean_speed),
            "co2_emissions": float(co2_emissions),
            "starvation_count": float(starvation_count)
        }

        return float(reward), metrics

    def _get_info(self) -> Dict[str, Any]:
        """Returns step metadata."""
        return {
            "sim_step": self.sim_step,
            "current_phase": self.current_green_phase,
            "time_in_phase": self.time_in_phase
        }

    def close(self):
        """Safely terminates the TraCI connection."""
        if not self.is_closed and self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
            finally:
                self.conn = None
                self.is_closed = True


def make_env(
    network: str = "single",
    config_path: Optional[str] = None,
    gui: bool = False,
    gui_delay: int = 50,
    tripinfo_output: Optional[str] = None,
    max_steps: int = 3600,
    delta_time: int = 5
) -> SumoTrafficEnv:
    """
    Factory function to instantiate SumoTrafficEnv for single_intersection or mukhani_chauraha.
    """
    if network.lower() in ["mukhani", "mukhani_chauraha"]:
        cfg = config_path or "sumo/networks/mukhani_chauraha/mukhani.sumocfg"
        mukhani_lanes = [
            "KW2M_0", "KW2M_1", "KW2M_2",
            "KE2M_0", "KE2M_1", "KE2M_2",
            "CN2M_0", "CN2M_1",
            "CS2M_0", "CS2M_1"
        ]
        mukhani_edges = ["KW2M", "KE2M", "CN2M", "CS2M"]
        return SumoTrafficEnv(
            cfg_file=cfg,
            tls_id="Mukhani",
            incoming_lanes=mukhani_lanes,
            incoming_edges=mukhani_edges,
            phase_ns_green=2,
            phase_ns_yellow=3,
            phase_ew_green=0,
            phase_ew_yellow=1,
            max_steps=max_steps,
            delta_time=delta_time,
            yellow_duration=3,
            min_green=5,
            gui=gui,
            gui_delay=gui_delay,
            tripinfo_output=tripinfo_output
        )
    else:
        cfg = config_path or "sumo/networks/single_intersection/single_intersection.sumocfg"
        return SumoTrafficEnv(
            cfg_file=cfg,
            tls_id="C",
            max_steps=max_steps,
            delta_time=delta_time,
            yellow_duration=3,
            min_green=5,
            gui=gui,
            gui_delay=gui_delay,
            tripinfo_output=tripinfo_output
        )
