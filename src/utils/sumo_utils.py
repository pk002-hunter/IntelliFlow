"""
SUMO Utility functions for path resolution, binary discovery, and TraCI connection management.
"""
import os
import sys
import shutil


def setup_sumo_path():
    """Ensure SUMO tools are on sys.path and SUMO_HOME is set."""
    if 'SUMO_HOME' not in os.environ:
        candidates = [
            r"C:\Program Files (x86)\Eclipse\Sumo",
            r"C:\Program Files\Eclipse\Sumo",
            r"C:\sumo",
            "/usr/share/sumo",
            "/opt/homebrew/opt/sumo/share/sumo"
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                os.environ['SUMO_HOME'] = candidate
                break

    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        if os.path.exists(tools) and tools not in sys.path:
            sys.path.append(tools)


def get_sumo_binary(gui: bool = False) -> str:
    """
    Find sumo or sumo-gui executable across system path and SUMO_HOME.
    """
    setup_sumo_path()
    binary_name = "sumo-gui" if gui else "sumo"
    if sys.platform.startswith("win"):
        binary_name += ".exe"

    # 1. Direct which search
    which_path = shutil.which(binary_name)
    if which_path:
        return which_path

    # 2. Check SUMO_HOME/bin
    if 'SUMO_HOME' in os.environ:
        candidate = os.path.join(os.environ['SUMO_HOME'], 'bin', binary_name)
        if os.path.exists(candidate):
            return candidate

    # 3. Known fallback locations on Windows
    for base in [r"C:\Program Files (x86)\Eclipse\Sumo", r"C:\Program Files\Eclipse\Sumo", r"C:\sumo"]:
        candidate = os.path.join(base, "bin", binary_name)
        if os.path.exists(candidate):
            return candidate

    return binary_name
