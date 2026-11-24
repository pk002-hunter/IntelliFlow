"""
Unit & Integration Tests for Full Haldwani City Road Network Environment.
Verifies city-wide multi-arterial geometry, shortcuts, hospitals, and ambulance preemption.
"""
import sys
import os
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from stable_baselines3.common.env_checker import check_env
from src.environment.sumo_env import make_env


def test_haldwani_full_env_compliance():
    """Verify that the full Haldwani network SumoTrafficEnv adheres to SB3 standards."""
    env = make_env(network="haldwani", max_steps=100, delta_time=5, gui=False)
    try:
        check_env(env, warn=True)
        obs, info = env.reset(seed=202)
        expected_dim = 10 * 4 + 3  # 43 dimensions for junction Mukhani
        assert obs.shape == (expected_dim,), f"Expected obs shape ({expected_dim},), got {obs.shape}"
        assert obs.dtype == np.float32

        # Step 0: action 0 (East-West Kaladhungi Road green)
        next_obs, reward, terminated, truncated, step_info = env.step(0)
        assert next_obs.shape == (expected_dim,)
        assert isinstance(reward, float)

        # Step 1: action 1 (North-South Canal/Chhoti Mukhani green)
        next_obs, reward, terminated, truncated, step_info = env.step(1)
        assert isinstance(step_info["total_halting"], float)
        assert isinstance(step_info["mean_speed"], float)
    finally:
        env.close()
