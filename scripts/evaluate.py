"""
IntelliFlow 🚦 Unified Benchmark Evaluation CLI Entrypoint.
Runs evaluation, statistical significance tests, and generates comparison plots.
"""
import os
import sys

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.evaluation.evaluate import main

if __name__ == "__main__":
    main()
