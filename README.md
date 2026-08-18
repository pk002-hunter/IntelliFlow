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

### Key Results *(updated as training progresses)*
| Metric | Fixed-Time | Actuated | IntelliFlow (PPO) |
|--------|-----------|----------|-------------------|
| Avg. Waiting Time | — | — | — |
| Avg. Queue Length | — | — | — |
| Throughput (veh/hr) | — | — | — |
| CO₂ Emissions | — | — | — |

> Results will be populated once experiments are complete.

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

### Quick Start — Run a Baseline

```bash
# Train the RL agent on a single intersection
python scripts/train.py --agent ppo --intersection single --episodes 500

# Evaluate and compare against baselines
python scripts/evaluate.py --agent ppo --compare fixed_time actuated

# Launch the results dashboard
streamlit run src/dashboard/app.py
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

## 📊 Results

*Experiments in progress. Results and training curves will be added here.*

---

## 🗺️ Roadmap

- [x] Project setup & folder structure
- [ ] SUMO environment setup & baseline controllers
- [ ] Single-intersection DQN agent
- [ ] Single-intersection PPO agent
- [ ] Indian mixed-traffic modeling
- [ ] Multi-intersection MARL (grid network)
- [ ] Ambulance priority preemption
- [ ] Pedestrian safety phase integration
- [ ] Pollution-aware reward shaping
- [ ] Streamlit live dashboard
- [ ] Research paper submission

---

## 👥 Team

| Member | Role |
|--------|------|
| Member 1 | RL Engineer |
| Member 2 | Simulation Engineer |
| Member 3 | Data & Evaluation Lead |
| Member 4 | Integration & Docs Lead |

> *BTech Final Year Project — CSE (AI/ML), 2026–27*

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
