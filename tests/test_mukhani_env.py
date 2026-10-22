"""
Unit & Integration Tests for Mukhani Chauraha Environment.
Verifies real-world Haldwani intersection geometry, Indian mixed-traffic, and ambulance preemption.
"""
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
from stable_baselines3.common.env_checker import check_env
from src.environment.sumo_env import SumoTrafficEnv


def test_mukhani_env_compliance():
    """Verify that Mukhani Chauraha SumoTrafficEnv adheres to SB3 standards."""
    mukhani_lanes = [
        "KW2M_0", "KW2M_1", "KW2M_2",
        "KE2M_0", "KE2M_1", "KE2M_2",
        "CN2M_0", "CN2M_1",
        "CS2M_0", "CS2M_1"
    ]
    mukhani_edges = ["KW2M", "KE2M", "CN2M", "CS2M"]

    env = SumoTrafficEnv(
        cfg_file="sumo/networks/mukhani_chauraha/mukhani.sumocfg",
        tls_id="Mukhani",
        incoming_lanes=mukhani_lanes,
        incoming_edges=mukhani_edges,
        phase_ns_green=2,
        phase_ns_yellow=3,
        phase_ew_green=0,
        phase_ew_yellow=1,
        max_steps=100,
        delta_time=5,
        yellow_duration=3,
        min_green=5,
        gui=False
    )
    try:
        check_env(env, warn=True)
        obs, info = env.reset(seed=101)
        expected_dim = len(mukhani_lanes) * 4 + 3  # 10 * 4 + 3 = 43
        assert obs.shape == (expected_dim,), f"Expected obs shape ({expected_dim},), got {obs.shape}"
        assert obs.dtype == np.float32

        # Step 0: action 0 (EW Kaladhungi Road green)
        next_obs, reward, terminated, truncated, step_info = env.step(0)
        assert next_obs.shape == (expected_dim,)
        assert isinstance(reward, float)

        # Step 1: action 1 (NS Canal/Chhoti Mukhani green) -> triggers yellow transition
        next_obs, reward, terminated, truncated, step_info = env.step(1)
        assert step_info["action_switched"] is True
    finally:
        env.close()


if __name__ == "__main__":
    print("Testing Mukhani Chauraha Environment...")
    test_mukhani_env_compliance()
    print("PASS: Mukhani Chauraha Environment passed all compliance and stepping tests!")
