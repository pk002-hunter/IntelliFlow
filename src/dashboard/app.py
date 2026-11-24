"""
IntelliFlow // Traffic Operations Center (TOC) & Digital Twin Dashboard.
Run via: streamlit run src/dashboard/app.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Ensure project root is resolvable regardless of launch directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.dashboard.styles import GLOBAL_CSS
from src.dashboard.data_loader import (
    FLEET_COMPOSITION,
    compute_bpr_stress_analysis,
    compute_digital_twin_state,
    compute_hypothesis_tests,
    get_diurnal_curve_df,
    load_benchmark_comparison,
    load_controller_timeseries,
    parse_haldwani_topology,
    parse_mukhani_tll,
)
from src.dashboard.components import (
    render_architecture_svg,
    render_command_header,
    render_emergency_banner,
    render_kpi_strip,
    render_led_queue_panel,
    render_mukhani_digital_twin,
    render_phase2_roadmap_card,
    render_phase_interlock_strip,
)
from src.dashboard.charts import (
    CORRIDOR_ROUTES,
    _apply_obsidian_layout,
    build_benchmark_overlay_chart,
    build_bpr_stress_chart,
    build_diurnal_profile_chart,
    build_haldwani_network_figure,
    build_live_telemetry_chart,
    build_queue_distribution_boxplot,
)

# ─── Page Config & Design Tokens ──────────────────────────────────────────────
st.set_page_config(
    page_title="IntelliFlow // Traffic Operations Center",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.html(GLOBAL_CSS)

# ─── Session State Initialization ─────────────────────────────────────────────
if "step_idx" not in st.session_state:
    st.session_state.step_idx = 12
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False
if "emergency_active" not in st.session_state:
    st.session_state.emergency_active = False
if "ctrl_selector" not in st.session_state:
    st.session_state.ctrl_selector = None
if "diurnal_preset" not in st.session_state:
    st.session_state.diurnal_preset = "09:00 · Morning Peak (Inbound)"

PRESET_HOURS = {
    "09:00 · Morning Peak (Inbound)": 9,
    "18:00 · Evening Peak (Outbound)": 18,
    "13:00 · Midday Commercial": 13,
    "21:00 · Late Evening Freight": 21,
    "03:00 · Night Baseline": 3,
}

# ─── Load Real Data & Topology ────────────────────────────────────────────────
ts_data = load_controller_timeseries()
bench_df = load_benchmark_comparison()
stats_df = compute_hypothesis_tests()
diurnal_df = get_diurnal_curve_df()
topology = parse_haldwani_topology()
mukhani_phases = parse_mukhani_tll()

available_controllers = list(ts_data.keys())
if not available_controllers:
    st.error("No simulation CSV telemetry found in results/metrics/. Run evaluation first.")
    st.stop()

if st.session_state.ctrl_selector not in available_controllers:
    st.session_state.ctrl_selector = available_controllers[0]

active_controller_hdr = st.session_state.ctrl_selector
active_hour_hdr = PRESET_HOURS.get(st.session_state.diurnal_preset, 9)
active_df_hdr = ts_data[active_controller_hdr]
safe_hdr_idx = min(int(st.session_state.step_idx), max(0, len(active_df_hdr) - 1))
hdr_sim_step = int(active_df_hdr.iloc[safe_hdr_idx].get("step", (safe_hdr_idx + 1) * 10))

# ─── Sidebar: Operations Reference & System Health ────────────────────────────
with st.sidebar:
    st.markdown("### INTELLIFLOW // OPS SPEC")
    st.caption("Team #54 · CSP-701 Major Project · B.Tech CSE (AI & ML)")
    st.markdown("---")
    st.markdown("**Active Testbed:** Mukhani Chauraha, Haldwani")
    st.markdown(
        "- Topology: 4-Way, 10 Inbound Lanes\n"
        "- Physics: SUMO Sublane (`0.5m` lateral)\n"
        "- Primary Corridor: Kaladhungi Rd (SH-41)\n"
        "- Trauma Target: STH Hospital (Rampur Rd)"
    )
    st.markdown("---")
    st.markdown("**Loaded Telemetry Traces**")
    for label, df in ts_data.items():
        st.caption(f"• {label}: `{len(df)}` steps")
    st.markdown("---")
    st.markdown("**Phase Status**")
    st.caption("• Phase 1: Simulation & RL Core [ACTIVE]")
    st.caption("• Phase 2: Edge CCTV / YOLO [ROADMAP]")

# ─── Global Top Command Bar ───────────────────────────────────────────────────
st.html(
    render_command_header(
        controller_label=active_controller_hdr,
        sim_step=hdr_sim_step,
        diurnal_hour=active_hour_hdr,
        emergency_active=st.session_state.emergency_active,
        is_playing=st.session_state.is_playing,
    )
)

# ─── Primary Workspace Navigation Tabs ────────────────────────────────────────
tab_ops, tab_bench, tab_map, tab_green, tab_arch = st.tabs([
    "01 · Operations HUD & Digital Twin",
    "02 · Benchmark Arena & Statistics",
    "03 · Haldwani Corridors & Green Wave",
    "04 · Green AI & Economic Ledger",
    "05 · Architecture, Safety & Phase 2 Roadmap",
])


# ==============================================================================
# TAB 1: OPERATIONS HUD & DIGITAL TWIN
# ==============================================================================
def _render_live_hud(controller_label: str, diurnal_hour: int) -> None:
    """Renders Tab 1 Live Digital Twin, LED Queues, and Synchronized Telemetry."""
    active_df = ts_data[controller_label]
    max_idx = max(0, len(active_df) - 1)

    if st.session_state.is_playing:
        st.session_state.step_idx = (st.session_state.step_idx + 1) % (max_idx + 1)
    elif st.session_state.step_idx > max_idx:
        st.session_state.step_idx = max_idx

    twin_state = compute_digital_twin_state(
        controller_label=controller_label,
        df=active_df,
        row_idx=st.session_state.step_idx,
        diurnal_hour=diurnal_hour,
        emergency_active=st.session_state.emergency_active,
    )

    # Emergency Preemption HUD Alert
    emerg_html = render_emergency_banner(st.session_state.emergency_active)
    if emerg_html:
        st.html(emerg_html)

    # Top 4 KPI Cards (Step-Live + Verified Benchmark Context)
    q_color = "#10B981" if twin_state["total_halting"] <= 3.0 else ("#F59E0B" if twin_state["total_halting"] <= 10.0 else "#EF4444")
    spd_color = "#10B981" if twin_state["mean_speed_kmh"] >= 38.0 else "#F59E0B"
    kpi_items = [
        {
            "label": "LIVE JUNCTION QUEUE (STEP)",
            "value": f"{twin_state['total_halting']:.1f} veh",
            "delta": "Benchmark PPO Avg: 0.32 vs 7.80 Fixed (-95.9%)",
            "accent": q_color,
        },
        {
            "label": "MEAN CORRIDOR VELOCITY",
            "value": f"{twin_state['mean_speed_kmh']:.1f} km/h",
            "delta": "Benchmark PPO Avg: 42.88 km/h (+16.1%)",
            "accent": spd_color,
        },
        {
            "label": "ACCUMULATED WAIT (STEP)",
            "value": f"{twin_state['waiting_time']:.1f} s",
            "delta": f"Diurnal Load: {twin_state['diurnal_flow_vph']} veh/hr ({diurnal_hour:02d}:00)",
            "accent": "#94A3B8",
        },
        {
            "label": "STATISTICAL RIGOR (BENCHMARK)",
            "value": "p = 5.78e-21",
            "delta": "Mann-Whitney U = 822.5 · Welch t = -7.14",
            "accent": "#22D3EE",
        },
    ]
    st.html(render_kpi_strip(kpi_items))

    # Main Split HUD: 62% Digital Twin SVG | 38% LED Queue Gauges & Step Readout
    col_twin, col_hud = st.columns([1.55, 1.0], gap="medium")

    with col_twin:
        st.markdown(render_mukhani_digital_twin(twin_state), unsafe_allow_html=True)
        st.html(render_phase_interlock_strip(twin_state))

    with col_hud:
        st.html(render_led_queue_panel(twin_state))

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.session_state.is_playing:
            pct = int((st.session_state.step_idx / max(1, max_idx)) * 100)
            st.html(f"""
            <div class="toc-panel" style="padding:10px 12px; margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span class="toc-micro-label">AUTO-STREAMING TELEMETRY</span>
                    <span class="toc-mono" style="font-size:11px; color:#22D3EE;">T+{twin_state['sim_step']:04d}s ({pct}%)</span>
                </div>
                <div style="height:6px; background:#1A2232; border-radius:3px; overflow:hidden;">
                    <div style="width:{pct}%; height:100%; background:#2563EB;"></div>
                </div>
            </div>
            """)
        else:
            st.slider(
                "SIMULATION TIMELINE SCRUBBER (STEP INDEX)",
                min_value=0,
                max_value=max_idx,
                key="step_idx",
            )

        reward_str = f"{twin_state['reward']:.3f}" if twin_state["reward"] is not None else "N/A (Baseline)"
        co2_str = f"{twin_state['co2_mg_s'] / 1000.0:.1f} g/s" if twin_state["co2_mg_s"] > 0 else "N/A"
        st.html(f"""
        <div class="toc-panel" style="padding:10px 12px;">
            <div class="toc-micro-label" style="margin-bottom:6px;">ACTIVE PROFILE & STEP DIAGNOSTICS</div>
            <div class="led-telemetry-line" style="margin-bottom:4px;">
                <span>SIMULATION CLOCK:</span><strong style="color:#F8FAFC;">T+{twin_state['sim_step']:04d}s</strong>
            </div>
            <div class="led-telemetry-line" style="margin-bottom:4px;">
                <span>REWARD SIGNAL:</span><strong style="color:#F8FAFC;">{reward_str}</strong>
            </div>
            <div class="led-telemetry-line" style="margin-bottom:4px;">
                <span>HBEFA3 CO2 RATE:</span><strong style="color:#F8FAFC;">{co2_str}</strong>
            </div>
            <div class="led-telemetry-line">
                <span>BPR REGIME:</span><strong style="color:#60A5FA;">{twin_state['diurnal_desc'][:34]}</strong>
            </div>
        </div>
        """)

    # Synchronized Dual-Trace Chart
    fig_live = build_live_telemetry_chart(active_df, twin_state["sim_step"], controller_label)
    st.plotly_chart(fig_live, width="stretch", config={"displayModeBar": False})


@st.fragment(run_every=0.9)
def _live_hud_polling_fragment(controller_label: str, diurnal_hour: int) -> None:
    _render_live_hud(controller_label, diurnal_hour)


with tab_ops:
    # Inline Tactical Control Strip
    ctrl1, ctrl2, ctrl3, ctrl4, ctrl5 = st.columns([2.0, 1.4, 0.85, 0.85, 1.4], gap="small")
    with ctrl1:
        selected_ctrl = st.selectbox(
            "ACTIVE SIGNAL CONTROLLER",
            options=available_controllers,
            key="ctrl_selector",
        )
    with ctrl2:
        selected_preset = st.selectbox(
            "DIURNAL DEMAND PROFILE (BPR)",
            options=list(PRESET_HOURS.keys()),
            key="diurnal_preset",
        )
        active_hour = PRESET_HOURS[selected_preset]
    with ctrl3:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        play_label = "PAUSE" if st.session_state.is_playing else "PLAY"
        if st.button(play_label, type="primary", width="stretch", key="btn_play"):
            st.session_state.is_playing = not st.session_state.is_playing
            st.rerun()
    with ctrl4:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        if st.button("RESET", width="stretch", key="btn_reset"):
            st.session_state.is_playing = False
            st.session_state.step_idx = 0
            st.rerun()
    with ctrl5:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        emerg_label = "CLEAR AMBULANCE" if st.session_state.emergency_active else "DISPATCH AMBULANCE"
        if st.button(emerg_label, width="stretch", key="btn_emergency"):
            st.session_state.emergency_active = not st.session_state.emergency_active
            st.rerun()

    if st.session_state.is_playing:
        _live_hud_polling_fragment(selected_ctrl, active_hour)
    else:
        _render_live_hud(selected_ctrl, active_hour)


# ==============================================================================
# TAB 2: BENCHMARK ARENA & STATISTICAL RIGOR
# ==============================================================================
with tab_bench:
    st.html(
        render_kpi_strip([
            {"label": "PPO QUEUE REDUCTION", "value": "-95.9%", "delta": "0.32 vs 7.80 veh (Webster)", "accent": "#10B981"},
            {"label": "MEAN SPEED GAIN", "value": "+16.1%", "delta": "42.88 vs 36.92 km/h", "accent": "#10B981"},
            {"label": "ACTUATED FAILURE DELTA", "value": "+23.9% WORSE", "delta": "9.67 veh queue (non-lane tripping)", "accent": "#EF4444"},
            {"label": "MANN-WHITNEY U TEST", "value": "p = 5.78e-21", "delta": "Welch t = -7.14 (p = 7.27e-08)", "accent": "#22D3EE"},
        ])
    )

    b_col1, b_col2 = st.columns([1.2, 1.0], gap="medium")
    with b_col1:
        st.markdown("##### Empirical Benchmark Ledger (`benchmark_comparison.csv`)")
        if bench_df is not None:
            st.dataframe(bench_df, width="stretch", hide_index=True)
        else:
            st.warning("benchmark_comparison.csv not found in results/metrics/.")

    with b_col2:
        st.markdown("##### Hypothesis Significance Matrix (vs Webster Fixed-Time)")
        if not stats_df.empty:
            st.dataframe(stats_df, width="stretch", hide_index=True)

    st.markdown("---")
    ctrl_filter = st.multiselect(
        "CONTROLLERS TO OVERLAY",
        options=available_controllers,
        default=[c for c in ["Fixed-Time (Webster)", "Sensor-Actuated (Gap-Out)", "DQN Agent (Benchmark)", "PPO Agent (Benchmark)"] if c in available_controllers],
        key="bench_multi",
    )

    c_chart1, c_chart2 = st.columns(2, gap="medium")
    with c_chart1:
        if ctrl_filter:
            fig_q = build_benchmark_overlay_chart(
                ts_data,
                ctrl_filter,
                metric_col="halting_vehicles",
                y_label="Halting Queue (veh)",
                title="HALTING QUEUE TRAJECTORY (0 - 300s ALIGNED WINDOW)",
                max_step=300,
            )
            st.plotly_chart(fig_q, width="stretch", config={"displayModeBar": False})

    with c_chart2:
        if ctrl_filter:
            fig_box = build_queue_distribution_boxplot(ts_data, ctrl_filter)
            st.plotly_chart(fig_box, width="stretch", config={"displayModeBar": False})

    c_speed, c_stress = st.columns(2, gap="medium")
    with c_speed:
        if ctrl_filter:
            fig_s = build_benchmark_overlay_chart(
                ts_data,
                ctrl_filter,
                metric_col="mean_speed",
                y_label="Mean Speed (km/h)",
                title="CORRIDOR VELOCITY COMPARISON (0 - 300s ALIGNED WINDOW)",
                max_step=300,
            )
            st.plotly_chart(fig_s, width="stretch", config={"displayModeBar": False})

    with c_stress:
        demand_vph = st.slider(
            "ANALYTICAL BPR DEMAND STRESS-TESTER (VEH/HR)",
            min_value=500,
            max_value=3500,
            value=2400,
            step=100,
            key="stress_slider",
        )
        stress_df = compute_bpr_stress_analysis(demand_vph)
        fig_stress = build_bpr_stress_chart(stress_df, demand_vph)
        st.plotly_chart(fig_stress, width="stretch", config={"displayModeBar": False})
        st.caption("Note: Stress curve uses analytical BPR capacity-delay response; top charts reflect empirical SUMO simulation logs.")


# ==============================================================================
# TAB 3: HALDWANI CORRIDORS & GREEN WAVE
# ==============================================================================
with tab_map:
    m_ctrl1, m_ctrl2, m_ctrl3, m_ctrl4 = st.columns([1.8, 0.8, 0.8, 0.8], gap="small")
    with m_ctrl1:
        selected_corridor = st.selectbox(
            "EMERGENCY GREEN WAVE VECTOR",
            options=["None"] + list(CORRIDOR_ROUTES.keys()),
            index=1,
            key="corridor_select",
        )
    with m_ctrl2:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        show_art = st.checkbox("Highway Arterials", value=True, key="chk_art")
    with m_ctrl3:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        show_short = st.checkbox("City Shortcuts", value=True, key="chk_short")
    with m_ctrl4:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        show_hosp = st.checkbox("Hospital Hubs", value=True, key="chk_hosp")

    fig_map = build_haldwani_network_figure(
        topology=topology,
        show_arterials=show_art,
        show_shortcuts=show_short,
        show_hospitals=show_hosp,
        corridor_key=selected_corridor,
    )
    st.plotly_chart(fig_map, width="stretch", config={"displayModeBar": True})

    # Bottom Directory & 24h Diurnal BPR Demand
    dir_col1, dir_col2 = st.columns([1.15, 1.0], gap="medium")
    with dir_col1:
        st.markdown("##### Hospital Trauma Hubs & Strategic Bypass Nodes (Parsed from SUMO XML)")
        hosp_df = pd.DataFrame(topology["hospitals"])
        if not hosp_df.empty:
            hosp_view = hosp_df[["id", "name", "x", "y"]].rename(
                columns={"id": "Landmark ID", "name": "Hospital / Facility", "x": "X (m)", "y": "Y (m)"}
            )
            st.dataframe(hosp_view, width="stretch", hide_index=True, height=235)

    with dir_col2:
        fig_diurnal = build_diurnal_profile_chart(diurnal_df, active_hour)
        st.plotly_chart(fig_diurnal, width="stretch", config={"displayModeBar": False})


# ==============================================================================
# TAB 4: GREEN AI & ECONOMIC IMPACT LEDGER
# ==============================================================================
with tab_green:
    st.markdown("##### Environmental Accounting & Commuter Fuel Ledger")
    g_col1, g_col2 = st.columns([1.0, 1.35], gap="medium")

    with g_col1:
        st.markdown("###### Economic Projection Parameters (Haldwani Arterial Model)")
        corridor_vehicles = st.slider("Daily Arterial Vehicle Volume", 15000, 60000, 32000, step=1000, key="econ_vol")
        fuel_price = st.slider("Blended Fuel Price (INR / Liter)", 85, 120, 96, step=1, key="econ_fuel")
        idle_saved_sec = st.slider("Avg Idling Time Saved / Vehicle (sec)", 10, 45, 22, step=1, key="econ_idle")

        # Idling fuel burn rate ~ 0.85 L/hr average weighted across mixed Indian fleet (2W, Auto, Car, Bus)
        liters_saved_day = corridor_vehicles * (idle_saved_sec / 3600.0) * 0.85
        annual_savings_cr = (liters_saved_day * fuel_price * 365.0) / 1e7
        annual_co2_tonnes = (liters_saved_day * 2.31 * 365.0) / 1000.0

        st.html(
            render_kpi_strip([
                {"label": "ANNUAL FUEL SAVED", "value": f"₹{annual_savings_cr:.2f} Cr", "delta": "Baseline Ref: ₹2.48+ Cr/yr", "accent": "#10B981"},
                {"label": "CO2 ABATED / YEAR", "value": f"{annual_co2_tonnes:.1f} t", "delta": f"{liters_saved_day:.0f} L fuel saved/day", "accent": "#10B981"},
                {"label": "PPO BENCHMARK CO2", "value": "16.34 kg", "delta": "3,600s episode (HBEFA3)", "accent": "#22D3EE"},
                {"label": "MUKHANI PPO CO2", "value": "27.58 kg", "delta": "10-lane peak mixed traffic", "accent": "#94A3B8"},
            ])
        )

    with g_col2:
        # Indian Heterogeneous Fleet PCU & CO2 Breakdown
        fleet_df = pd.DataFrame(FLEET_COMPOSITION)
        fig_fleet = go.Figure()
        fig_fleet.add_trace(
            go.Bar(
                x=fleet_df["class"],
                y=fleet_df["share_pct"],
                name="Traffic Share (%)",
                marker_color=fleet_df["color"],
                text=[f"{p}% (PCU {u})" for p, u in zip(fleet_df["share_pct"], fleet_df["pcu"])],
                textposition="outside",
                textfont=dict(family="JetBrains Mono, monospace", size=10.5, color="#E2E8F0"),
            )
        )
        _apply_obsidian_layout(fig_fleet, title="CALIBRATED INDIAN HETEROGENEOUS FLEET MIX (MUKHANI.ROU.XML)", height=310)
        fig_fleet.update_yaxes(title_text="Volume Share (%)", range=[0, 52])
        st.plotly_chart(fig_fleet, width="stretch", config={"displayModeBar": False})

    # Empirical CO2 rate comparison across logged RL runs
    if "PPO Agent (Mukhani 10-Lane)" in ts_data and "PPO Agent (Benchmark)" in ts_data:
        m_df = ts_data["PPO Agent (Mukhani 10-Lane)"]
        p_df = ts_data["PPO Agent (Benchmark)"]
        fig_co2 = go.Figure()
        fig_co2.add_trace(
            go.Scatter(
                x=m_df["step"],
                y=m_df["co2_emissions"] / 1000.0,
                name="PPO Mukhani 10-Lane (g/s)",
                line=dict(color="#06B6D4", width=1.8),
            )
        )
        fig_co2.add_trace(
            go.Scatter(
                x=p_df["step"],
                y=p_df["co2_emissions"] / 1000.0,
                name="PPO Benchmark Single (g/s)",
                line=dict(color="#10B981", width=1.8),
            )
        )
        _apply_obsidian_layout(fig_co2, title="EMPIRICAL HBEFA3 CO2 EMISSIONS RATE OVER 3,600s EPISODE (g/s)", height=270)
        fig_co2.update_xaxes(title_text="Simulation Seconds (s)")
        fig_co2.update_yaxes(title_text="CO2 Rate (g/s)")
        st.plotly_chart(fig_co2, width="stretch", config={"displayModeBar": False})


# ==============================================================================
# TAB 5: ARCHITECTURE, SAFETY & PHASE 2 ROADMAP
# ==============================================================================
with tab_arch:
    st.markdown(render_architecture_svg(), unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    a_col1, a_col2 = st.columns(2, gap="medium")
    with a_col1:
        st.html("""
        <div class="toc-panel">
            <div class="toc-panel-header">
                <span class="toc-panel-title">OBSERVATION & MULTI-OBJECTIVE REWARD (SUMO_ENV.PY)</span>
                <span class="toc-mono" style="font-size:10.5px; color:#22D3EE;">43D / 35D BOX</span>
            </div>
            <div style="font-size:12.5px; color:#94A3B8; line-height:1.55;">
                <strong style="color:#F8FAFC;">Observation Vector:</strong> Continuous normalized Box in <code>[0, 1]</code>:<br/>
                • <strong>Mukhani (10 lanes &times; 4 features + 3):</strong> <code>43 dimensions</code><br/>
                • <strong>Single Intersection (8 lanes &times; 4 features + 3):</strong> <code>35 dimensions</code><br/>
                • Features per lane: halting ratio, normalized speed, waiting time, vehicle density + 2D one-hot phase + normalized phase dwell.
            </div>
        </div>
        """)
        st.latex(r"""
        R_t = -\left(1.0 \cdot Q_t + 0.02 \cdot \frac{W_t}{10} + 0.0001 \cdot \frac{E_t}{1000} + 0.05 \cdot S_t\right) + 0.5 \cdot \frac{V_t}{v_{\max}} - 1.5 \cdot \mathbf{1}_{\{\text{switch}\}} - 5.0 \cdot D_{\text{amb}}
        """)

    with a_col2:
        st.html("""
        <div class="toc-panel">
            <div class="toc-panel-header">
                <span class="toc-panel-title">3-TIER HARDWARE SAFETY & FAILSAFE INTERLOCK MATRIX</span>
                <span class="toc-pill toc-pill-green" style="font-size:10px;">VERIFIED IN CODE</span>
            </div>
            <div style="font-size:12.5px; color:#94A3B8; line-height:1.6;">
                1. <strong style="color:#F8FAFC;">Tier 1 — Physical Minimum Green & Yellow Lock:</strong> Environment blocks phase switches when <code>time_in_phase &lt; 5s</code> and inserts a mandatory <code>3s</code> amber clearance phase before switching axes.<br/>
                2. <strong style="color:#F8FAFC;">Tier 2 — Anti-Starvation Guardrail:</strong> Any vehicle waiting past <code>120.0s</code> triggers starvation penalties to guarantee minor approaches never lock indefinitely.<br/>
                3. <strong style="color:#F8FAFC;">Tier 3 — Emergency Ambulance Override:</strong> Vehicles with <code>vClass="emergency"</code> incur a <code>5.0x</code> delay penalty per halted second, driving rapid green-wave preemption.
            </div>
        </div>
        """)
        if mukhani_phases:
            st.markdown("##### Verified Signal Program (`mukhani.tll.xml`)")
            st.dataframe(pd.DataFrame(mukhani_phases), width="stretch", hide_index=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.html(render_phase2_roadmap_card())
