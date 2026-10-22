import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
import numpy as np
from stable_baselines3.common.env_checker import check_env
from src.environment.sumo_env import SumoTrafficEnv


def test_env_sb3_compliance():
    """Verify that SumoTrafficEnv adheres to all Gymnasium and SB3 standards."""
    env = SumoTrafficEnv(
        cfg_file="sumo/networks/single_intersection/single_intersection.sumocfg",
        max_steps=100,
        delta_time=5,
        yellow_duration=3,
        min_green=5,
        gui=False
    )
    try:
        # check_env checks action space, observation space, reset(), step(), datatypes, etc.
        check_env(env, warn=True)
    finally:
        env.close()


def test_env_step_and_observation_bounds():
    """Verify observation shape, range [0, 1], and step return format."""
    env = SumoTrafficEnv(
        cfg_file="sumo/networks/single_intersection/single_intersection.sumocfg",
        max_steps=50,
        delta_time=5,
        gui=False
    )
    try:
        obs, info = env.reset(seed=42)
        assert obs.shape == (35,), f"Expected obs shape (35,), got {obs.shape}"
        assert obs.dtype == np.float32, f"Expected float32, got {obs.dtype}"
        assert np.all(obs >= 0.0) and np.all(obs <= 1.0), "Obs values out of [0, 1] range"

        # Step 0: action 0 (NS)
        next_obs, reward, terminated, truncated, step_info = env.step(0)
        assert next_obs.shape == (35,)
        assert isinstance(reward, float)
        assert isinstance(terminated, bool)
        assert isinstance(truncated, bool)
        assert "total_halting" in step_info

        # Step 1: action 1 (EW) -> triggers yellow transition
        next_obs, reward, terminated, truncated, step_info = env.step(1)
        assert step_info["action_switched"] is True
    finally:
        env.close()


if __name__ == "__main__":
    print("Running test_env_sb3_compliance...")
    test_env_sb3_compliance()
    print("PASS: test_env_sb3_compliance")
    
    print("Running test_env_step_and_observation_bounds...")
    test_env_step_and_observation_bounds()
    print("PASS: test_env_step_and_observation_bounds")
    print("All unit tests passed successfully!")
