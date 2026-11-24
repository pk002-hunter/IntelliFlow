# IntelliFlow 🚦
### AI-Powered Adaptive Traffic Signal Control System
*Deep Reinforcement Learning & Edge Computer Vision for Indian Mixed-Traffic Networks*

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.2%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![SUMO](https://img.shields.io/badge/SUMO-1.19%2B-00BCD4?style=for-the-badge)
![React](https://img.shields.io/badge/React-19-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Phase_2_Roadmap-00599C?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-4%2F4%20Passing-22C55E?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

**An intelligent, multi-objective Deep Reinforcement Learning (PPO & DQN) traffic signal controller,  
grounded in real-world OpenStreetMap city networks and calibrated for Indian mixed-traffic dynamics.**

[Overview](#-overview) · [Key Innovations](#-key-innovations) · [Case Study: Haldwani](#-case-study-haldwani-city--mukhani-chauraha) · [Architecture](#-architecture) · [Benchmark Results](#-benchmark-results) · [Quick Start](#-quick-start) · [Project Structure](#-project-structure) · [Team](#-team)

</div>

---

## 📖 Overview

Conventional traffic control in developing nations relies predominantly on **fixed-time Webster cycles** or simplistic actuated timers. In Indian cities, these static systems fail catastrophically due to:
1. **Extreme Traffic Heterogeneity:** Unsegregated mixture of two-wheelers, auto-rickshaws, passenger cars, buses, and freight vehicles sharing narrow lanes.
2. **Non-Lane Disciplined Behavior:** Frequent filtering, creeping, and lateral lane encroachment.
3. **Asymmetric Diurnal Swells:** Morning inbound commuter surges and evening outbound egress that quickly overwhelm fixed splits.

**IntelliFlow** replaces legacy timing plans with an autonomous Deep Reinforcement Learning agent (**PPO** & **Double DQN** with Prioritized Experience Replay) coupled with an edge **YOLOv8** computer vision bridge. Operating over the microscopic simulation engine **SUMO (Simulation of Urban MObility)**, IntelliFlow dynamically modulates signal phases based on real-time multi-lane queue pressures, queue dissipation rates, and waiting times.

---

## 🌟 Key Innovations

* 🧠 **State-of-the-Art Dual RL Engine:**
  - **PPO (Proximal Policy Optimization):** Clipped surrogate objective with Generalized Advantage Estimation (GAE) for robust, stable phase optimization without catastrophic policy collapse.
  - **DQN (Deep Q-Network):** Target networks with Huber loss and $\epsilon$-greedy exploration for discrete action value estimation.
* 🗺️ **Real-World City Scale Simulation (Haldwani, Uttarakhand):**
  - **Mukhani Chauraha (10-Lane Junction):** A critical 4-approach arterial intersection modeled with authentic geometries, turn bays, and signal phases.
  - **Full City Road Network (37,000+ Streets):** Complete OpenStreetMap extraction spanning Kathgodam down to Motahaldu, compressed natively (`haldwani_osm_real.net.xml.gz`) for zero-loss simulation.
* 📈 **24-Hour Diurnal Google Maps Traffic Ingestion:**
  - Microscopic traffic generator utilizing the **Bureau of Public Roads (BPR)** formulation to transform real-world speed and congestion indices into continuous 24-hour demand curves.
  - Dedicated scenarios for **Morning Peak (8:00 AM – 10:30 AM)** and **Evening Peak (5:30 PM – 8:30 PM)**.
* 🛵 **Indian Mixed-Traffic Calibration:**
  - Realistic Krauss car-following parameters calibrated for 6 distinct vehicle classes: motorcycles, three-wheeler autos, compact cars, SUVs, public buses, and commercial trucks.
  - Sublane model integration accounting for motorcycle filtering and lateral lane sharing.
* 👁️ **YOLOv8 Edge Computer Vision Bridge *(Phase 2 Hardware Roadmap)*:**
  - Architecture and pipeline designed for estimating physical approach queues from roadside CCTV feeds; real-time hardware camera deployment is scoped for Phase 2 while Phase 1 operates directly over Eclipse SUMO & TraCI telemetry.
* 🌿 **Green AI & Economic Impact Ledger:**
  - Comprehensive environmental accounting tracking CO₂, CO, NOx, PMx, and idling fuel consumption.
  - Projected annual economic savings of **₹2.48+ Crores** in commuter fuel for Haldwani arterial corridors.
* 📊 **Interactive Operations UI & Master Launcher:**
  - **React + TypeScript + Tailwind v4 Frontend (`frontend/`):** Features a synchronized **Split-Screen "AI vs. Legacy" Traffic Duel** (60fps HTML5 Canvas mixed-traffic micro-simulation comparing Webster Fixed-Time / Sensor-Actuated against PPO / Double DQN), **Full-Screen Animated Haldwani City Flow Map**, **Dedicated Team #54 Individual Contributions Page**, **Light & Dark Mode**, **5-Axis Controller Radar & BPR Stress-Tester**, and **24-Hour Google Maps BPR Wave & Fuel Ledger**.
  - **One-Click Master Launcher (`run.bat`):** Launches live SUMO-GUI simulations, the React Operations UI (Option 10), evaluation suites, and automated tests from a single terminal menu (`stop.bat` terminates all SUMO, Python, and Vite UI processes cleanly).

---

## 📍 Case Study: Haldwani City & Mukhani Chauraha

| Parameter | Mukhani Chauraha Arterial | Full Haldwani City Network |
| :--- | :--- | :--- |
| **Location** | Haldwani, Nainital District, UK, India | Kathgodam ⇄ Haldwani ⇄ Motahaldu |
| **Topology** | 4-Way 10-Lane Multi-Arterial Junction | 37,000+ Real OSM Road Segments |
| **Connecting Corridors** | Kaladhungi Rd, Nainital Rd, Bareilly Rd | NH-109, Arterials, Gullies & Hospital Zones |
| **Peak Demand** | 2,100 – 3,400 vehicles / hour | 15,000+ concurrent city trips |
| **Vehicle Mix** | 45% 2-Wheelers, 20% Autos, 30% Cars, 5% Buses | Heterogeneous Indian Urban Mix |
| **Control Logic** | 4-Phase NEMA with Minimum Green Protection | Coordinated Arterial Corridor Management |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              IntelliFlow System                             │
│                                                                             │
│  ┌──────────────────────────┐                   ┌────────────────────────┐  │
│  │   Physical Road Sensors  │                   │     SUMO Simulation    │  │
│  │   & CCTV Video Feeds     │                   │   (Mukhani / Haldwani) │  │
│  └─────────────┬────────────┘                   └───────────▲────────────┘  │
│                │                                            │               │
│  ┌─────────────▼────────────┐                               │  TraCI API    │
│  │ YOLOv8 Vehicle Detector  │                               │  Phase Dwell  │
│  │  (Edge Queue Estimation) │                               │  & Actuation  │
│  └─────────────┬────────────┘                   ┌───────────┴────────────┐  │
│                │                                │  Gymnasium Environment │  │
│                └───────────────►┬──────────────►│ (State, Reward, Reset) │  │
│                                 │               └───────────┬────────────┘  │
│                                 │                           │               │
│                                 │ Normalized State Vector   │ Reward Signal │
│                                 │ [Queues, Phase, Dwell, V] │ (Delay, Co2)  │
│                                 │                           │               │
│                                 │               ┌───────────▼────────────┐  │
│                                 │               │     Deep RL Policy     │  │
│                                 │               │   (PPO Actor-Critic    │  │
│                                 └───────────────┤   / Double DQN Agent)  │  │
│                                                 └────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### State Space ($\mathcal{S}$)
A continuous normalized vector $\mathbf{s}_t \in \mathbb{R}^{n}$:
- **Lane Queue Densities:** $\frac{q_i}{q_{\max}}$ for each incoming lane approach.
- **Current Active Phase:** One-hot encoded vector representing the active green signal.
- **Phase Dwell Time:** Normalized time elapsed since the last phase change $\frac{t_{\text{phase}}}{t_{\max}}$.
- **Mean Approach Speeds:** $\frac{v_i}{v_{\text{speedlimit}}}$ across all inbound edges.

### Action Space ($\mathcal{A}$)
Discrete action space $\mathcal{A} = \{0, 1, 2, 3\}$ selecting the next green phase:
- **Phase 0:** North-South Through & Right Turn
- **Phase 1:** North-South Left Turn & Filter
- **Phase 2:** East-West Through & Right Turn
- **Phase 3:** East-West Left Turn & Filter
*Enforces hard 5-second minimum green constraint and 3-second yellow clearance for physical safety.*

### Reward Function ($\mathcal{R}$)
Multi-objective shaped reward penalizing total delay, excessive queues, starvation, and fuel consumption:
$$R_t = - \left( w_1 \sum_{i} \text{WaitTime}_i + w_2 \sum_{i} \text{Queue}_i^2 + w_3 \sum_{i} \text{Emissions}_i + w_4 \cdot \text{StarvationPenalty} \right)$$

---

## 📊 Benchmark Results

Evaluated across a 3,600-second continuous simulation under peak Indian mixed-traffic demand (2,100 veh/hr):

| Metric | Fixed-Time (Webster) | Sensor-Actuated | IntelliFlow (DQN) | IntelliFlow (PPO) | Improvement vs Fixed |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mean Queue Length** | 7.80 ± 5.73 vehs | 9.67 ± 7.42 vehs | 0.32 ± 0.55 vehs | **0.32 ± 0.55 vehs** | **-95.9%** ($p < 10^{-20}$) |
| **Max Queue Length** | 20.0 vehs | 29.0 vehs | 2.0 vehs | **2.0 vehs** | **-90.0%** |
| **Mean Travel Speed** | 36.92 km/h | 36.33 km/h | 42.88 km/h | **42.88 km/h** | **+16.1%** |
| **Average Delay per Vehicle** | 24.8 s | 29.2 s | 5.3 s | **5.3 s** | **-78.6%** |
| **Total Throughput** | 2,100 veh/hr | 2,100 veh/hr | 2,100 veh/hr | **2,100 veh/hr** | 100% Cleared |
| **CO₂ Emissions / Veh** | 142.6 g | 148.1 g | 114.2 g | **114.2 g** | **-19.9%** |
| **Mann-Whitney U Test** | Baseline | $p = 0.12$ (N.S.) | $p = 5.78 \times 10^{-21}$ | **$p = 5.78 \times 10^{-21}$** | Statistically Significant |

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python:** 3.10 or higher
- **Node.js:** 18+ (for the React + TypeScript frontend in `frontend/`)
- **SUMO:** [Eclipse SUMO 1.19+](https://eclipse.dev/sumo/) installed with `SUMO_HOME` set in environment variables.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/pk002-hunter/IntelliFlow.git
cd IntelliFlow

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux / macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Master Interactive Launcher (Windows)
Run the master control menu to access all simulation, demo, and evaluation tools:
```bat
run.bat
```
```
===================================================================
  IntelliFlow: AI Adaptive Traffic Signal Control (Team #54)
  Case Study: Mukhani Chauraha and Full Haldwani Road Network
===================================================================
  [AI-CONTROLLED LIVE DEMOS - PPO REINFORCEMENT LEARNING]
  1. Mukhani Chauraha 10-Lane Junction (Live AI Signal Control)
  2. Full Haldwani City Corridors (Live AI Signal Control)

  [STANDALONE ROAD NETWORK AND PEAK TRAFFIC VISUALIZERS]
  3. View Complete 37,000+ Streets Real OSM City Network
  4. View Morning Peak Hour Traffic Rush (8:00 AM - 10:30 AM)
  5. View Evening Peak Hour Traffic Rush (5:30 PM - 8:30 PM)

  [COMPUTER VISION, WEB UI AND VALIDATION]
  9. Run YOLOv8 Computer Vision Bridge (Traffic State Estimation)
  10. Launch Interactive Operations UI (React + TypeScript Web App)
  11. Run Empirical Benchmark and Statistical Hypothesis Tests
  12. Run Project Test Suite (pytest - 4/4 Tests)
  0. Exit
===================================================================
```

### 4. Direct Command-Line Usage

```bash
# Train PPO agent on Mukhani Chauraha
python scripts/train.py --agent ppo --timesteps 30000

# Train DQN agent
python scripts/train.py --agent dqn --timesteps 30000

# Run evaluation & generate publication figures
python scripts/evaluate.py

# Launch React + TypeScript Operations UI (AI vs. Legacy Duel + Haldwani Map)
cd frontend && npm install && npm run dev

# Build React Frontend for Production
cd frontend && npm run build

# Run YOLOv8 Vision Bridge
python scripts/yolo_traffic_detector.py

# Run Automated Test Suite
pytest tests/ -v
```

---

## ☁️ Google Colab Cloud Training

For high-speed GPU training and headless evaluation, open the canonical notebook in Google Colab:
- **Notebook Path:** [`notebooks/IntelliFlow_Google_Colab_Haldwani_PPO.ipynb`](notebooks/IntelliFlow_Google_Colab_Haldwani_PPO.ipynb)
- **Features Included:**
  - Automated cloud installation of `sumo`, `sumo-tools`, and Python dependencies.
  - Pretrained weight auto-detection for instant evaluation without retraining.
  - Multi-scenario evaluation (Normal, Morning Peak, Evening Peak).
  - 5-Axis Polar Spider Radar Charts.
  - Green AI Carbon & Commuter Economic Savings Ledger.

---

## 📁 Project Structure

```
IntelliFlow/
├── frontend/                                        # React 19 + TypeScript + Tailwind v4 Operations UI
│   ├── src/
│   │   ├── components/ui/                           # shadcn/ui primitives (button, card, input, label, select, tabs)
│   │   ├── features/
│   │   │   ├── operations/                          # TopCommandBar, TrafficDuelArena, 60fps MukhaniFlowCanvas, Specs
│   │   │   ├── benchmarks/                          # ControllerRaceArena (delay race + 5-axis SVG radar)
│   │   │   ├── corridors/                           # HaldwaniCorridorMap (animated city traffic flow + Green-Wave)
│   │   │   ├── economics/                           # DiurnalGreenSection (24h BPR wave + fuel/CO2 ledger)
│   │   │   └── team/                                # TeamContributionsPage (individual member deliverables)
│   │   ├── data/                                    # Exported 360-step telemetry.json & typed models/networks
│   │   ├── lib/                                     # Traffic phase derivation, Green AI calculations & cn()
│   │   ├── types/                                   # Shared TypeScript domain interfaces
│   │   ├── App.tsx                                  # 4-Act Operations & Viva Showcase shell
│   │   └── index.css                                # Light & Dark mode CSS tokens
│   ├── components.json
│   ├── package.json
│   └── vite.config.ts
│
├── notebooks/
│   └── IntelliFlow_Google_Colab_Haldwani_PPO.ipynb  # Cloud GPU training & benchmark notebook
│
├── results/
│   ├── metrics/                                     # CSV benchmark & evaluation logs
│   └── plots/                                       # Generated queue, speed, and radar plots
│
├── scripts/
│   ├── demo.py                                      # Live AI control runner via TraCI
│   ├── train.py                                     # Training script for PPO & DQN
│   ├── evaluate.py                                  # Statistical evaluation & plotting
│   ├── google_maps_24h_traffic.py                   # BPR 24-hour diurnal demand generator
│   └── yolo_traffic_detector.py                     # YOLOv8 CCTV queue estimator (Phase 2)
│
├── src/
│   ├── agents/
│   │   ├── dqn/                                     # Deep Q-Network implementation
│   │   └── ppo/                                     # Proximal Policy Optimization implementation
│   ├── baselines/
│   │   ├── actuated.py                              # Dynamic sensor-actuated baseline
│   │   └── fixed_time.py                            # Webster fixed-time baseline
│   ├── environment/
│   │   └── sumo_env.py                              # Custom Gymnasium SUMO TraCI environment
│   ├── evaluation/
│   │   └── evaluate.py                              # Hypothesis testing & statistical metrics
│   └── utils/
│       └── sumo_utils.py                            # SUMO route & configuration utilities
│
├── sumo/
│   └── networks/
│       ├── haldwani_full/                           # 37,000+ street full city OSM network
│       │   ├── haldwani_osm_real.net.xml.gz         # Compressed real OSM network
│       │   ├── haldwani_real.sumocfg                # Master city simulation configuration
│       │   └── haldwani_real_landmarks.add.xml      # Hospitals, bus terminals, intersections
│       │
│       ├── mukhani_chauraha/                        # Primary 10-lane experimental junction
│       │   ├── mukhani.net.xml                      # Accurate junction road geometry
│       │   ├── mukhani_24h.rou.xml                  # 24-hour diurnal Google Maps demand
│       │   ├── mukhani_morning_peak.rou.xml         # Inbound morning commuter surge
│       │   ├── mukhani_evening_peak.rou.xml         # Outbound evening commuter surge
│       │   └── mukhani.sumocfg                      # Mukhani simulation configuration
│       │
│       └── single_intersection/                     # Baseline 4-way single intersection
│
├── tests/
│   ├── test_sumo_env.py                             # Gymnasium environment compliance tests
│   ├── test_mukhani_env.py                          # Mukhani 10-lane junction validation
│   └── test_haldwani_env.py                         # Full Haldwani network loading tests
│
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

---

## 🗺️ Roadmap & Project Status

- [x] **Phase 1: Foundation & Simulation Baselines**
  - [x] Custom Gymnasium SUMO Environment (`SumoTrafficEnv`) with TraCI integration.
  - [x] Baseline controllers: Webster fixed-time & sensor-actuated logic.
  - [x] Initial 4-way synthetic intersection modeling.
- [x] **Phase 2: Deep Reinforcement Learning Core**
  - [x] Single-intersection DQN agent with Experience Replay & Target Networks.
  - [x] Single-intersection PPO agent with Generalized Advantage Estimation (GAE).
  - [x] Multi-objective reward shaping (queue penalty, delay reduction, emissions).
  - [x] Automated benchmark suite with Mann-Whitney U statistical hypothesis testing.
- [x] **Phase 3: Real-World Road Networks (Haldwani Case Study)**
  - [x] 10-Lane Mukhani Chauraha junction modeling with authentic turn bays and signal phases.
  - [x] Full Haldwani 37,000+ street OSM extraction (Kathgodam to Motahaldu) with gzip compression.
  - [x] Indian mixed-traffic calibration (Krauss car-following for 6 vehicle classes, sublane model).
  - [x] Landmark integration: Sushila Tiwari Hospital, Haldwani Railway Station, Bus Terminal.
- [x] **Phase 4: Real-World Ingestion & Advanced Traffic Scenarios**
  - [x] 24-Hour Diurnal Google Maps traffic generation using BPR capacity-delay functions.
  - [x] Calibrated Morning Peak (8:00 AM – 10:30 AM) and Evening Peak (5:30 PM – 8:30 PM) scenarios.
  - [x] Automated 4/4 pytest regression suite verifying all environments and routes.
- [x] **Phase 5: Operations UI & Green AI Ledger**
  - [x] React 19 + TypeScript + Tailwind v4 Operations Console (`frontend/`) featuring a Split-Screen "AI vs. Legacy" Traffic Duel, 60fps Canvas mixed-traffic flow, Animated Haldwani City Map, Team #54 Page, Light & Dark modes, 5-Axis Controller Radar, and BPR Stress-Tester.
  - [x] Green AI carbon emissions and economic benefit analysis (₹2.48+ Crores annual commuter savings).
  - [x] Google Colab cloud GPU training notebook with pretrained weights auto-detection.
- [ ] **Phase 6 (Future Hardware Roadmap): Edge Computer Vision Deployment**
  - [ ] Physical pole-mounted CCTV RTSP ingestion via TensorRT YOLOv8 (`scripts/yolo_traffic_detector.py` prototype ready for later hardware integration).

---

## 👥 Team #54

| Name | University Roll No. (URN) | Section | Project Role |
| :--- | :---: | :---: | :--- |
| **Piyush Karnatak** *(Lead)* | 2361393 | B | Deep RL Architecture, SUMO Modeling & Colab Pipeline |
| **Rahul Bhakuni** | 2361432 | B | Microscopic Traffic Simulation & Network Optimization |
| **Vishal Joshi** | 2361588 | B | Empirical Evaluation, Statistical Rigor & Data Science |
| **Lalit Joshi** | 2361296 | F | Edge YOLOv8 Vision Integration & System Documentation |

*B.Tech Final Year Capstone Project · Computer Science & Engineering (AI/ML) · Project Code: CSP-701 / MPP-I (2026–27)*

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Eclipse SUMO (Simulation of Urban MObility)](https://eclipse.dev/sumo/)
- [Stable-Baselines3](https://github.com/DLR-RM/stable-baselines3)
- [OpenStreetMap Contributors](https://www.openstreetmap.org/)
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- *IntelliLight* (Wei et al., KDD 2018) & *MPLight* (Chen et al., AAAI 2020)
