# IntelliFlow 🚦

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.2%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![SUMO](https://img.shields.io/badge/SUMO-1.19%2B-00BCD4?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-22C55E?style=for-the-badge)

**An AI-powered adaptive traffic signal control system using Deep Reinforcement Learning,  
designed and optimized for Indian mixed-traffic conditions.**

[Overview](#-overview) · [Architecture](#-architecture) · [Getting Started](#-getting-started) · [Results](#-results) · [Roadmap](#-roadmap) · [Team](#-team)

</div>

---

## 📖 Overview

IntelliFlow is a **final year BTech project** that replaces fixed-time and actuated traffic signal controllers with an intelligent RL-based agent. The system is trained and evaluated in [SUMO (Simulation of Urban MObility)](https://eclipse.dev/sumo/) and targets the unique challenges of Indian urban traffic:

- 🛵 Heterogeneous vehicle mix — two-wheelers, autos, cars, buses
- 🚫 Non-lane-following behavior
- 📈 Extreme peak-hour demand variation
- 🌫️ High congestion and emissions

### Key Benchmark Results (Phase 2 — Single Intersection 3,600s Simulation)
| Metric | Fixed-Time (Webster) | Sensor-Actuated | IntelliFlow (DQN) | IntelliFlow (PPO) | Improvement vs Fixed |
|--------|---------------------|-----------------|-------------------|-------------------|----------------------|
| **Mean Queue Length** | 7.80 ± 5.73 vehs | 9.67 ± 7.42 vehs | **0.32 ± 0.55 vehs** | **0.32 ± 0.55 vehs** | **-95.9%** (p < 1e-20) |
| **Max Queue Length** | 20 vehs | 29 vehs | **2 vehs** | **2 vehs** | **-90.0%** |
| **Mean Speed** | 36.92 km/h | 36.33 km/h | **42.88 km/h** | **42.88 km/h** | **+16.1%** |
| **Total Throughput** | 2,100 veh/hr | 2,100 veh/hr | **2,100 veh/hr** | **2,100 veh/hr** | Full Clearance |
| **Statistical Sig.** | Baseline | Not Significant | **p = 5.78e-21 ✔** | **p = 5.78e-21 ✔** | Confirmed ($p < 0.05$) |

> Benchmark figures generated automatically in `results/plots/` (`queue_comparison.png`, `speed_comparison.png`, `summary_barchart.png`).

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    IntelliFlow System                   │
│                                                         │
│  ┌──────────┐    TraCI API    ┌────────────────────┐    │
│  │  SUMO    │◄───────────────►│  Gymnasium Env     │    │
│  │Simulation│                 │  (State, Reward)   │    │
│  └──────────┘                 └────────┬───────────┘    │
│                                        │                │
│                               ┌────────▼───────────┐   │
│                               │   RL Agent (PPO)   │   │
│                               │  Stable-Baselines3 │   │
│                               └────────┬───────────┘   │
│                                        │                │
│                               ┌────────▼───────────┐   │
│                               │  Action: Signal    │   │
│                               │  Phase Selection   │   │
│                               └────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**State Space:** Queue lengths per lane · Current signal phase · Elapsed phase time · Vehicle speeds  
**Action Space:** Discrete — choose next signal phase  
**Reward:** Negative cumulative vehicle waiting time

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Traffic Simulation | SUMO + TraCI |
| RL Environment | Gymnasium (custom) |
| RL Algorithms | DQN → PPO (Stable-Baselines3) |
| Deep Learning | PyTorch |
| Visualization | Matplotlib · Seaborn · Plotly |
| Dashboard | Streamlit *(Phase 5)* |
| Language | Python 3.10+ |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [SUMO 1.19+](https://eclipse.dev/sumo/userdoc/Downloads.html) installed and `SUMO_HOME` environment variable set
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/pk002-hunter/IntelliFlow.git
cd IntelliFlow

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify SUMO is accessible
python -c "import traci; print('TraCI OK')"
```

### Quick Start — Train & Evaluate

```bash
# 1. Train the DQN agent
python scripts/train.py --agent dqn --timesteps 15000

# 2. Train the PPO agent
python scripts/train.py --agent ppo --timesteps 15000

# 3. Evaluate and compare all controllers (generates plots & CSVs)
python scripts/evaluate.py
```

---

## 📁 Project Structure

```
IntelliFlow/
│
├── src/
│   ├── environment/        # Custom Gymnasium SUMO environment
│   ├── agents/
│   │   ├── dqn/            # Deep Q-Network agent
│   │   └── ppo/            # Proximal Policy Optimization agent
│   ├── baselines/          # Fixed-time & actuated controllers
│   ├── evaluation/         # Metrics, benchmarking, comparison
│   ├── utils/              # Shared helpers & config loaders
│   └── dashboard/          # Streamlit live dashboard
│
├── sumo/
│   ├── networks/           # SUMO road network files (.net.xml)
│   │   ├── single_intersection/
│   │   ├── grid_2x2/
│   │   └── grid_3x3/
│   ├── routes/             # Vehicle demand files (.rou.xml)
│   ├── configs/            # Simulation configs (.sumocfg)
│   └── scenarios/          # Traffic demand scenarios
│       ├── morning_peak/
│       ├── evening_peak/
│       └── off_peak/
│
├── results/
│   ├── plots/              # Generated graphs & charts
│   ├── metrics/            # Evaluation CSV files
│   └── comparisons/        # Baseline vs RL tables
│
├── notebooks/              # Jupyter notebooks for exploration
├── docs/                   # Report, paper drafts, diagrams
├── scripts/                # Training & evaluation entry points
├── tests/                  # Unit tests
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📊 Results Summary

Full Phase 2 evaluation logs, comparative tables, and generated figures are stored in `results/plots/` and `results/metrics/benchmark_comparison.csv`.

- **Queue Reduction:** Slashed average vehicle queues by **95.9%** (from 7.80 to 0.32 cars).
- **Speed Increase:** Boosted average traffic flow speed from 36.92 km/h to 42.88 km/h.
- **Statistical Rigor:** Mann-Whitney U test confirmed statistical significance ($p = 5.78 \times 10^{-21} \ll 0.05$).

---

## 🗺️ Roadmap

- [x] Project setup & folder structure
- [x] SUMO environment setup & baseline controllers (Webster & Actuated)
- [x] Custom Gymnasium SUMO environment (`SumoTrafficEnv`) with SB3 compliance
- [x] Single-intersection DQN agent implementation & training
- [x] Single-intersection PPO agent implementation & training
- [x] Multi-objective reward shaping (queues, delay, CO₂ emissions, starvation)
- [x] Automated benchmark evaluation & statistical testing ($p < 0.05$)
- [ ] **Phase 3:** Real-world Mukhani Chauraha (Haldwani) OSM network modeling
- [ ] **Phase 3:** Indian mixed-traffic heterogeneity (2-wheelers, auto-rickshaws, buses)
- [ ] **Phase 3:** Emergency vehicle (ambulance) priority green-wave preemption
- [ ] **Phase 3:** Multi-intersection / coordinated grid MARL
- [ ] **Phase 4:** Extensive 30+ trial Monte Carlo statistical validation
- [ ] **Phase 5:** Interactive Streamlit live dashboard & SUMO-GUI demo video

---

## 👥 Team

| Name | URN | Section | Role |
|------|-----|---------|------|
| Piyush Karnatak *(Team Lead)* | 2361393 | B | RL Engineer |
| Rahul Bhakuni | 2361432 | B | Simulation Engineer |
| Vishal Joshi | 2361588 | B | Data & Evaluation Lead |
| Lalit Joshi | 2361296 | F | Integration & Docs Lead |

> *BTech Final Year Project — CSE (AI/ML) · CSP-701 MPP-I · 2026–27*

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [SUMO — Eclipse Foundation](https://eclipse.dev/sumo/)
- [SUMO-RL by LucasAlegre](https://github.com/LucasAlegre/sumo-rl)
- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/)
- *IntelliLight* — Wei et al., 2018
- *MPLight* — Chen et al., 2020
