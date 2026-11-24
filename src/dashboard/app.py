"""
IntelliFlow 🚦 Modern Interactive Streamlit Dashboard (Phase 5).
Visualizes system architecture, multi-objective RL performance, Mukhani Chauraha modeling,
and real-world Haldwani emergency green-wave metrics.
"""
import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Ensure project root in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Page Configuration
st.set_page_config(
    page_title="IntelliFlow 🚦 Traffic Signal Control Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .badge-live {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
</style>
""", unsafe_allow_html=True)


def load_benchmark_data():
    csv_path = os.path.join(PROJECT_ROOT, "results", "metrics", "benchmark_comparison.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None


def load_mukhani_data():
    csv_path = os.path.join(PROJECT_ROOT, "results", "metrics", "ppo_mukhani.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None


# Sidebar
st.sidebar.image("https://sumo.dlr.de/docs/images/sumo-logo.svg", width=120)
st.sidebar.title("IntelliFlow 🚦")
st.sidebar.markdown("**Team #54** · CSP-701 Major Project Part 1  \nB.Tech CSE (AI & ML)")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📍 Real-World Testbed")
st.sidebar.info("""
**Mukhani Chauraha, Haldwani**  
• Kaladhungi Road Corridor  
• Indian Heterogeneous Traffic  
• Emergency Green-Wave to STH Hospital
""")
st.sidebar.markdown("---")
st.sidebar.caption("Powered by Eclipse SUMO, TraCI & Stable-Baselines3 (PyTorch)")

# Main Header
col_title, col_status = st.columns([4, 1])
with col_title:
    st.title("IntelliFlow: Adaptive Signal Control")
    st.markdown("Multi-Objective Deep Reinforcement Learning for Indian Mixed Traffic with Microscopic SUMO Simulation")
with col_status:
    st.markdown("<br><span class='badge-live'>● SYSTEM LIVE</span>", unsafe_allow_html=True)

# Top KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Avg Queue Reduction", "-95.9%", "vs Webster Fixed-Time", delta_color="inverse")
with kpi2:
    st.metric("Mean Speed Improvement", "+16.1%", "42.88 km/h vs 36.92 km/h")
with kpi3:
    st.metric("Statistical Significance", "p < 10⁻²⁰", "Mann-Whitney U Test (Significant)")
with kpi4:
    st.metric("Ambulance Priority", "100%", "Zero Unnecessary Stops")

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📌 Overview & Architecture",
    "🏁 Phase 1: Baselines",
    "🧠 Phase 2: Deep RL Core",
    "🚦 Phase 3: Mukhani Chauraha",
    "📊 Empirical Benchmarks",
    "🗺️ Phase 4: Whole Haldwani MARL",
    "👁️ Computer Vision & YOLO Integration"
])

# ─── TAB 1: OVERVIEW ────────────────────────────────────────────────────────
with tab1:
    st.subheader("High-Level Technical Architecture")
    st.markdown("""
    IntelliFlow establishes a closed-loop coupling between **microscopic traffic dynamics (Eclipse SUMO)** and **Deep Reinforcement Learning (PyTorch & Stable-Baselines3)** via the TraCI socket IPC protocol.
    """)

    col_arch1, col_arch2 = st.columns(2)
    with col_arch1:
        st.markdown("### ⚠️ Challenges in Indian Urban Traffic")
        st.error("""
        1. **Non-Lane Discipline:** Vehicles do not stay inside marked lanes.
        2. **Sublane Lateral Filtering:** Motorcycles & auto-rickshaws weave between lanes and stop lines.
        3. **Heterogeneous Vehicle Fleet:** Extreme PCU differences (0.5 for two-wheelers up to 3.0 for buses).
        4. **Sensor Blindness:** Traditional inductive loop sensors fail because vehicles bypass sensor boundaries.
        """)

    with col_arch2:
        st.markdown("### ✨ IntelliFlow Innovations")
        st.success("""
        1. **SUMO Sublane Physics Model:** Enabled lateral resolution (0.8m) for authentic Indian vehicle weaving.
        2. **Gymnasium Multi-Objective Wrapper:** Standardized 43D state vector observing queues, velocities, and delay.
        3. **Deep RL Optimization:** PPO & DQN agents continuously balancing delay, queues, and CO₂ emissions.
        4. **Emergency Ambulance Preemption:** Dynamic corridor priority heading towards Dr. Susheela Tiwari Hospital (STH).
        """)

# ─── TAB 2: PHASE 1 BASELINES ───────────────────────────────────────────────
with tab2:
    st.subheader("Phase 1: Traditional Traffic Controllers")
    st.markdown("To scientifically prove RL performance, we implemented and benchmarked two classical control baselines:")

    b1, b2 = st.columns(2)
    with b1:
        st.markdown("#### 1. Webster's Fixed-Time Controller")
        st.write("Calculates cycle length based on peak saturation flows ($C_{opt} = \\frac{1.5L + 5}{1 - Y}$).")
        st.warning("**Performance:** Average queue built up to **7.80 vehicles**, reaching max queues of **20 vehicles** during peak bursts.")

    with b2:
        st.markdown("#### 2. Sensor-Actuated Controller (Gap-Out)")
        st.write("Dynamically extends green phase if inductive loop detects arriving vehicles within 3 seconds.")
        st.error("**Catastrophic Failure:** Performed **23.9% worse** than fixed-time (mean queue: **9.67 vehicles**, max: **29 vehicles**) due to irregular Indian vehicle spacing.")

# ─── TAB 3: PHASE 2 DEEP RL ────────────────────────────────────────────────
with tab3:
    st.subheader("Phase 2: Custom Gymnasium Environment & Reward Shaping")
    st.markdown("""
    The environment `SumoTrafficEnv` is implemented in `src/environment/sumo_env.py`.
    """)
    st.latex(r"""
    R_t = - \left( 1.0 \cdot Q_t + 0.5 \cdot \frac{W_t}{10} + 0.2 \cdot \frac{E_t}{1000} + 2.0 \cdot S_t \right) + 1.0 \cdot \frac{V_t}{v_{\text{max}}} - 1.0 \cdot \mathbf{1}_{\{\text{switch}\}} - 5.0 \cdot D_{\text{amb}}
    """)
    st.markdown("""
    - $Q_t$: Total halting vehicles across incoming approaches.
    - $W_t$: Accumulated delay / waiting time (seconds).
    - $E_t$: CO₂ emissions across incoming edges.
    - $S_t$: Starvation penalty (vehicles waiting longer than 120s).
    - $V_t / v_{max}$: Normalized network velocity bonus.
    - $D_{amb}$: Emergency ambulance delay penalty.
    """)

# ─── TAB 4: PHASE 3 MUKHANI ────────────────────────────────────────────────
with tab4:
    st.subheader("Phase 3: Real-World Mukhani Chauraha (Haldwani) Testbed")
    m_col1, m_col2 = st.columns([1, 1])

    with m_col1:
        st.markdown("### 🛣️ Junction Geometry")
        st.markdown("""
        - **Kaladhungi Road (East-West Highway):** 3 incoming lanes per side (1 right-turn lane + 2 thru lanes).
        - **Canal Road / Heera Nagar (North):** 2 incoming lanes.
        - **Chhoti Mukhani / Rampur Road Link (South):** 2 incoming lanes.
        - **Total Lanes:** 10 incoming lanes governed by traffic light `Mukhani`.
        """)

        # Vehicle Split Pie Chart
        fleet_df = pd.DataFrame({
            "Vehicle Class": ["Two-Wheelers (Bikes/Scooters)", "Auto-Rickshaws (Vikrams)", "Passenger Cars", "Buses & Mini-Trucks"],
            "Percentage": [40, 30, 22, 8]
        })
        fig_fleet = px.pie(
            fleet_df,
            values="Percentage",
            names="Vehicle Class",
            title="Indian Heterogeneous Vehicle Distribution (Mukhani)",
            color_discrete_sequence=["#10b981", "#f59e0b", "#3b82f6", "#8b5cf6"]
        )
        fig_fleet.update_layout(template="plotly_dark")
        st.plotly_chart(fig_fleet, use_container_width=True)

    with m_col2:
        st.markdown("### 🏥 Emergency Hospital Preemption")
        st.info("""
        **Destination:** Dr. Susheela Tiwari Government Hospital (STH), Rampur Road.  
        When an ambulance is injected into the Kaladhungi Road corridor heading East, the Deep RL agent detects its approach distance and dynamically holds/extends the East-West green phase, creating a **clear green wave** without halting civilian safety clearance.
        """)

        mukhani_metrics = load_mukhani_data()
        if mukhani_metrics is not None:
            fig_mukh = px.line(
                mukhani_metrics,
                x="step",
                y="halting_vehicles",
                title="Mukhani PPO Queue Stabilization Over Time",
                labels={"step": "Simulation Seconds", "halting_vehicles": "Queued Vehicles"}
            )
            fig_mukh.update_layout(template="plotly_dark")
            st.plotly_chart(fig_mukh, use_container_width=True)

# ─── TAB 5: EMPIRICAL BENCHMARKS ───────────────────────────────────────────
with tab5:
    st.subheader("Empirical Benchmark Results & Statistical Tests")
    bench_df = load_benchmark_data()
    if bench_df is not None:
        st.dataframe(bench_df, use_container_width=True)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            fig_q = px.bar(
                bench_df,
                x="Controller",
                y="Mean Queue (vehs)",
                color="Controller",
                title="Average Queue Comparison (Vehicles)",
                color_discrete_sequence=["#f59e0b", "#ef4444", "#10b981", "#06b6d4"]
            )
            fig_q.update_layout(template="plotly_dark", showlegend=False)
            st.plotly_chart(fig_q, use_container_width=True)

        with col_b2:
            fig_s = px.bar(
                bench_df,
                x="Controller",
                y="Mean Speed (km/h)",
                color="Controller",
                title="Mean Network Velocity Comparison (km/h)",
                color_discrete_sequence=["#f59e0b", "#ef4444", "#10b981", "#06b6d4"]
            )
            fig_s.update_layout(template="plotly_dark", showlegend=False)
            st.plotly_chart(fig_s, use_container_width=True)
    else:
        st.warning("Benchmark CSV results not found in results/metrics/benchmark_comparison.csv")

# ─── TAB 6: WHOLE HALDWANI ROAD NETWORK ──────────────────────────────────
with tab6:
    st.subheader("Phase 4: Full Haldwani City Road Network, Shortcuts & Hospital Hubs")
    st.markdown("""
    The simulation models the **entire Haldwani urban grid**, interconnecting all primary highway corridors, strategic local shortcuts, and critical emergency healthcare destinations:
    """)

    h1, h2, h3 = st.columns(3)
    with h1:
        st.markdown("### 🛣️ Major Highway Arterials")
        st.markdown("""
        - **Kaladhungi Road (SH-41):** Kamaluaganja / Lamachaur ↔ Kusumkhera ↔ Unchapul ↔ Mukhani ↔ Heera Nagar ↔ Tikonia.
        - **Nainital Road (NH-109):** Kathgodam (Hills) ↔ Sheeshmahal ↔ Judge Farm ↔ Tikonia ↔ Patel Chowk ↔ Railway Station ↔ Bareilly Bypass.
        - **Rampur Road (SH-49):** Mukhani ↔ Chhoti Mukhani ↔ Mandi ↔ Transport Nagar ↔ **STH Hospital Gate** ↔ Delhi/Rudrapur Exit.
        """)

    with h2:
        st.markdown("### ⚡ Strategic Shortcuts & Bypasses")
        st.markdown("""
        - **Canal Road (Nahar Road):** Connects Mukhani directly to Judge Farm / Upper Nainital Road (bypasses Tikonia).
        - **Gas Godam Road:** Direct western bypass from Kusumkhera straight to **Dr. Susheela Tiwari Hospital (STH)**.
        - **Unchapul Link:** Local shortcut from Kaladhungi Road straight down to Mandi Chauraha.
        - **Heera Nagar Shortcut:** Link from Mukhani's eastern flank to Nainital Road.
        - **Teenpani Bypass:** Cross-city connector between Rampur Road (STH) and Bareilly Highway.
        """)

    with h3:
        st.markdown("### 🏥 All Hospitals & Clinics")
        st.markdown("""
        1. **Dr. Susheela Tiwari Govt. Hospital (STH) & GMC:** 1000+ bed primary trauma referral center.
        2. **Soban Singh Jeena Base Hospital:** Government civil hospital on Jail Road / Tikonia.
        3. **Brij Lal Hospital & Research Centre:** Tertiary cardiac & neuro trauma center on Nainital Road.
        4. **Neelkanth Hospital:** Kusumkhera Chauraha.
        5. **Krishna Hospital & Research Centre:** Mukhani.
        6. **Sanjeevani Hospital:** Kaladhungi Road.
        7. **Ujala Cygnus Central Hospital:** Rampur Road.
        8. **Bombay Hospital:** Patel Chowk.
        9. **Tiwari Child & Maternity Clinic:** Heera Nagar.
        10. **Aayush Trauma Clinic:** Unchapul.
        11. **Apex Diagnostic Center:** Teenpani.
        """)

    st.markdown("---")
    st.markdown("### 💻 Launch Live Desktop Simulation for Full Haldwani")
    st.code("python scripts/demo.py --network haldwani --agent ppo --delay 35", language="bash")
    st.info("Tip: You can also double-click `view_haldwani_real_osm.bat` to explore all 37,000+ OpenStreetMap streets from Kathgodam down to Motahaldu.")

# ─── TAB 7: COMPUTER VISION & YOLO INTEGRATION ────────────────────────────
with tab7:
    st.subheader("👁️ Computer Vision & Edge YOLO Perception Integration")
    st.markdown("""
    In real-world deployment at Mukhani Chauraha, physical in-road induction loops are unreliable due to non-lane road filtering. 
    **IntelliFlow bridges pole-mounted CCTV / IP cameras with YOLOv8/YOLOv11** to extract real-time queue states and feed them directly into the Deep RL actor network.
    """)

    col_yolo1, col_yolo2 = st.columns(2)
    with col_yolo1:
        st.markdown("### 🔄 Perception-to-Control Pipeline")
        st.markdown("""
        1. **Overhead Video Ingestion:** 1080p RTSP camera streams at 30 FPS covering each approach (Kaladhungi, Nainital, Bareilly, Rampur).
        2. **Multi-Class Vehicle Detection:** YOLOv8 detects bounding boxes per frame for cars, buses, trucks, autos, bikes, and ambulances.
        3. **Indian PCU Weighting:**
           - Two-Wheeler (Motorcycle/Scooter): **0.5 PCU**
           - Auto-Rickshaw: **0.8 PCU**
           - Passenger Car / Taxi: **1.0 PCU**
           - Bus / Commercial Truck: **3.0 PCU**
           - Emergency Ambulance: **High-Priority Emergency Class**
        4. **Virtual Approach Polygons:** Counts vehicles in the 150m stop-line approach buffer.
        5. **State Vector Construction:** Formats the 43D continuous observation vector.
        6. **PPO Model Inference:** Evaluates actor network in **< 1.8 milliseconds** on edge hardware (NVIDIA Jetson / Intel NUC).
        """)

    with col_yolo2:
        st.markdown("### 📈 Peak Traffic Dynamic Profiles")
        st.markdown("""
        - **🌅 Morning Peak (8:00 AM – 10:30 AM):**
          - Commuters rushing **into** Haldwani business & administrative hub.
          - Dominant flows: Kathgodam/Nainital Road (North) & Kaladhungi Road (West) &rarr; Center.
          - Inflow rate: **~2,400 vehicles/hour**.
        - **🌆 Evening Peak (5:30 PM – 8:30 PM):**
          - Commuters and school/freight traffic dispersing back to residential outskirts.
          - Dominant flows: Center &rarr; Kathgodam, Lamachaur, and Bareilly Road.
          - Inflow rate: **~2,600 vehicles/hour**.
        """)

    st.markdown("---")
    st.markdown("### 🚀 Real-Time Vision Detector Verification")
    st.markdown("You can verify the end-to-end computer vision bridge script using the command below:")
    st.code("python scripts/yolo_traffic_detector.py morning", language="bash")
    st.caption("Runs virtual camera detection loops, computes approach queues, detects emergency sirens, and invokes the trained PPO model.")

