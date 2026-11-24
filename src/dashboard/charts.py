"""
IntelliFlow Plotly Dark Telemetry & Geospatial Network Charts.
Implements strict dark-obsidian surface styling, 1.5px-2px strokes,
dotted #1E2638 gridlines, and JetBrains Mono hover tooltips.
"""
from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

CONTROLLER_COLORS = {
    "PPO Agent (Mukhani 10-Lane)": "#06B6D4",
    "PPO Agent (Benchmark)": "#10B981",
    "PPO Agent": "#10B981",
    "DQN Agent (Benchmark)": "#3B82F6",
    "DQN Agent": "#3B82F6",
    "Fixed-Time (Webster)": "#F59E0B",
    "Sensor-Actuated (Gap-Out)": "#EF4444",
    "Sensor-Actuated": "#EF4444",
}

CORRIDOR_ROUTES = {
    "Mukhani -> STH Hospital (Rampur Rd SH-49)": [
        "KW_Out", "Kusumkhera", "Unchapul_Jct", "Mukhani",
        "ChhotiMukhani", "Mandi_Chauraha", "TransportNagar", "STH_Hospital_Jct", "STH_Gully_End"
    ],
    "Kusumkhera -> STH Hospital (Gas Godam Bypass)": [
        "KW_Out", "Kusumkhera", "GasGodam_Mid", "STH_Hospital_Jct", "STH_Gully_End"
    ],
    "Kathgodam -> Base Hospital (Nainital Rd NH-109)": [
        "Kathgodam_Out", "KathgodamHospital_Jct", "BrijlalHospital_Jct",
        "Sheeshmahal", "KrishnaHospital_Jct", "JudgeFarm", "Tikonia", "BaseHospital_Jct"
    ],
}


def _apply_obsidian_layout(fig: go.Figure, title: str = "", height: int = 340) -> go.Figure:
    """Applies unified Obsidian TOC visual styling to any Plotly figure."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Inter, sans-serif", size=13, color="#E2E8F0"),
            x=0.01,
            y=0.96,
        ) if title else None,
        height=height,
        margin=dict(l=46, r=24, t=44 if title else 22, b=40),
        paper_bgcolor="#121721",
        plot_bgcolor="#0B0E14",
        font=dict(family="Inter, sans-serif", size=11, color="#94A3B8"),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#181F2E",
            bordercolor="#2E3A52",
            font=dict(family="JetBrains Mono, monospace", size=11, color="#F8FAFC"),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color="#CBD5E1"),
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#1E2638",
        griddash="dot",
        zeroline=False,
        linecolor="#252F42",
        tickfont=dict(family="JetBrains Mono, monospace", size=10, color="#64748B"),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#1E2638",
        griddash="dot",
        zeroline=False,
        linecolor="#252F42",
        tickfont=dict(family="JetBrains Mono, monospace", size=10, color="#64748B"),
    )
    return fig


def build_live_telemetry_chart(
    df: pd.DataFrame,
    current_step: int,
    controller_label: str,
) -> go.Figure:
    """Dual-trace chart tracking halting queue and mean speed up to full episode with cursor."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    steps = df["step"]
    queue = df["halting_vehicles"]
    speed_kmh = df["mean_speed"] * 3.6
    q_color = CONTROLLER_COLORS.get(controller_label, "#06B6D4")

    # Full background reference trace (dimmed)
    fig.add_trace(
        go.Scatter(
            x=steps,
            y=queue,
            name="Halting Queue (veh)",
            line=dict(color=q_color, width=2.0),
            fill="tozeroy",
            fillcolor="rgba(6, 182, 212, 0.10)" if q_color == "#06B6D4" else "rgba(37, 99, 235, 0.10)",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=steps,
            y=speed_kmh,
            name="Mean Speed (km/h)",
            line=dict(color="#10B981", width=1.6, dash="solid"),
        ),
        secondary_y=True,
    )

    # Playhead vertical cursor
    fig.add_vline(
        x=current_step,
        line_width=1.5,
        line_dash="dash",
        line_color="#F8FAFC",
        opacity=0.85,
    )

    _apply_obsidian_layout(fig, title=f"LIVE TELEMETRY TRACE // {controller_label.upper()}", height=300)
    fig.update_xaxes(title_text="Simulation Step (s)", title_font=dict(size=10.5, color="#64748B"))
    fig.update_yaxes(title_text="Halting Queue (veh)", secondary_y=False, title_font=dict(size=10.5, color=q_color))
    fig.update_yaxes(title_text="Speed (km/h)", secondary_y=True, showgrid=False, title_font=dict(size=10.5, color="#10B981"))
    return fig


def build_benchmark_overlay_chart(
    ts_dict: Dict[str, pd.DataFrame],
    selected_controllers: List[str],
    metric_col: str,
    y_label: str,
    title: str,
    max_step: int = 300,
) -> go.Figure:
    """Multi-controller time-series comparison over aligned simulation window."""
    fig = go.Figure()
    for label in selected_controllers:
        df = ts_dict.get(label)
        if df is None or metric_col not in df.columns:
            continue
        sub = df[df["step"] <= max_step]
        vals = sub[metric_col] * 3.6 if metric_col == "mean_speed" else sub[metric_col]
        fig.add_trace(
            go.Scatter(
                x=sub["step"],
                y=vals,
                name=label,
                mode="lines",
                line=dict(color=CONTROLLER_COLORS.get(label, "#94A3B8"), width=2.0),
            )
        )
    _apply_obsidian_layout(fig, title=title, height=320)
    fig.update_xaxes(title_text="Simulation Seconds (s)")
    fig.update_yaxes(title_text=y_label)
    return fig


def build_queue_distribution_boxplot(
    ts_dict: Dict[str, pd.DataFrame],
    selected_controllers: List[str],
) -> go.Figure:
    """Box plot revealing queue stability and variance spikes across controllers."""
    fig = go.Figure()
    for label in selected_controllers:
        df = ts_dict.get(label)
        if df is None:
            continue
        color = CONTROLLER_COLORS.get(label, "#94A3B8")
        fig.add_trace(
            go.Box(
                y=df["halting_vehicles"],
                name=label,
                marker_color=color,
                line=dict(width=1.5),
                boxmean="sd",
            )
        )
    _apply_obsidian_layout(fig, title="QUEUE DISTRIBUTION & TAIL VARIANCE (MEAN ± SD)", height=320)
    fig.update_yaxes(title_text="Halting Vehicles")
    return fig


def build_bpr_stress_chart(stress_df: pd.DataFrame, current_demand: int) -> go.Figure:
    """Plots analytical BPR saturation curve across traffic demand levels."""
    fig = go.Figure()
    series = [
        ("Fixed-Time (Webster)", "#F59E0B", "solid"),
        ("Sensor-Actuated", "#EF4444", "dot"),
        ("PPO AI Agent", "#10B981", "solid"),
    ]
    for col, color, dash in series:
        fig.add_trace(
            go.Scatter(
                x=stress_df["Demand (veh/hr)"],
                y=stress_df[col],
                name=col,
                line=dict(color=color, width=2.0, dash=dash),
            )
        )
    fig.add_vline(
        x=current_demand,
        line_width=1.5,
        line_dash="dash",
        line_color="#3B82F6",
    )
    _apply_obsidian_layout(fig, title="ANALYTICAL BPR DEMAND STRESS RESPONSE (500 - 3,500 VEH/HR)", height=310)
    fig.update_xaxes(title_text="Arrival Demand (veh/hr)")
    fig.update_yaxes(title_text="Projected Mean Queue (veh/lane)")
    return fig


def build_diurnal_profile_chart(diurnal_df: pd.DataFrame, active_hour: int) -> go.Figure:
    """Plots 24-hour BPR calibrated traffic demand curve for Mukhani Chauraha."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=diurnal_df["time_label"],
            y=diurnal_df["flow_vph"],
            name="BPR Flow (veh/hr)",
            line=dict(color="#2563EB", width=2.0),
            fill="tozeroy",
            fillcolor="rgba(37, 99, 235, 0.14)",
        )
    )
    fig.add_vline(x=f"{active_hour:02d}:00", line_color="#10B981", line_width=1.5, line_dash="dash")
    _apply_obsidian_layout(fig, title="24-HOUR DIURNAL GOOGLE MAPS BPR DEMAND PROFILE", height=240)
    fig.update_yaxes(title_text="Inflow (veh/hr)")
    return fig


def build_haldwani_network_figure(
    topology: Dict[str, Any],
    show_arterials: bool = True,
    show_shortcuts: bool = True,
    show_hospitals: bool = True,
    corridor_key: str = "None",
) -> go.Figure:
    """
    Renders a coordinate-accurate interactive Plotly map of Haldwani City parsed
    from haldwani.nod.xml, haldwani.edg.xml, and haldwani_landmarks.add.xml.
    """
    nodes = topology["nodes"]
    edges = topology["edges"]
    hospitals = topology["hospitals"]
    shortcuts = topology["shortcuts"]

    fig = go.Figure()

    corridor_styles = {
        "Kaladhungi Rd (SH-41)": ("#3B82F6", 2.8, "solid"),
        "Nainital Rd (NH-109)": ("#60A5FA", 2.8, "solid"),
        "Rampur Rd (SH-49)": ("#94A3B8", 2.6, "solid"),
        "Strategic Shortcut / Bypass": ("#10B981", 1.8, "dash"),
        "Hospital Emergency Gully": ("#F43F5E", 1.8, "dot"),
    }

    # Group edges by corridor to minimize trace count while keeping clean legend
    grouped_coords: Dict[str, Dict[str, List[Any]]] = {}
    for edge in edges:
        ctype = edge["corridor"]
        is_shortcut = ctype in ("Strategic Shortcut / Bypass", "Hospital Emergency Gully")
        if is_shortcut and not show_shortcuts:
            continue
        if not is_shortcut and not show_arterials:
            continue

        n1 = nodes[edge["from"]]
        n2 = nodes[edge["to"]]
        bucket = grouped_coords.setdefault(ctype, {"x": [], "y": []})
        bucket["x"].extend([n1["x"], n2["x"], None])
        bucket["y"].extend([n1["y"], n2["y"], None])

    for ctype, coords in grouped_coords.items():
        color, width, dash = corridor_styles.get(ctype, ("#475569", 1.8, "solid"))
        fig.add_trace(
            go.Scatter(
                x=coords["x"],
                y=coords["y"],
                mode="lines",
                name=ctype,
                line=dict(color=color, width=width, dash=dash),
                hoverinfo="skip",
            )
        )

    # Highlight selected emergency corridor route
    if corridor_key in CORRIDOR_ROUTES:
        seq = CORRIDOR_ROUTES[corridor_key]
        rx, ry = [], []
        for nid in seq:
            if nid in nodes:
                rx.append(nodes[nid]["x"])
                ry.append(nodes[nid]["y"])
        if rx:
            fig.add_trace(
                go.Scatter(
                    x=rx,
                    y=ry,
                    mode="lines+markers",
                    name="ACTIVE GREEN WAVE CORRIDOR",
                    line=dict(color="#F43F5E", width=4.5),
                    marker=dict(size=7, color="#FDA4AF"),
                )
            )

    # Plot signalized traffic light nodes
    tls_nodes = [n for n in nodes.values() if n["type"] == "traffic_light"]
    if tls_nodes:
        fig.add_trace(
            go.Scatter(
                x=[n["x"] for n in tls_nodes],
                y=[n["y"] for n in tls_nodes],
                mode="markers+text",
                name="RL Traffic Signal Junctions (8)",
                text=[n["id"].replace("_Jct", "").replace("_", " ") for n in tls_nodes],
                textposition="top center",
                textfont=dict(family="JetBrains Mono, monospace", size=9.5, color="#E2E8F0"),
                marker=dict(
                    symbol="diamond",
                    size=11,
                    color="#06B6D4",
                    line=dict(width=1.5, color="#0B0E14"),
                ),
                hovertemplate="<b>%{text}</b><br>Coord: (%{x:.0f}m, %{y:.0f}m)<extra>RL Signalized Node</extra>",
            )
        )

    # Plot shortcut nodes if enabled
    if show_shortcuts and shortcuts:
        fig.add_trace(
            go.Scatter(
                x=[s["x"] for s in shortcuts],
                y=[s["y"] for s in shortcuts],
                mode="markers",
                name="Bypass Checkpoints",
                text=[s["name"] for s in shortcuts],
                marker=dict(symbol="circle", size=7, color="#10B981"),
                hovertemplate="<b>%{text}</b><extra>Strategic Bypass</extra>",
            )
        )

    # Plot hospitals
    if show_hospitals and hospitals:
        fig.add_trace(
            go.Scatter(
                x=[h["x"] for h in hospitals],
                y=[h["y"] for h in hospitals],
                mode="markers+text",
                name="Hospital Trauma Centers (8)",
                text=[h["name"].split("(")[0].strip() for h in hospitals],
                textposition="middle right",
                textfont=dict(family="Inter, sans-serif", size=9.5, color="#FDA4AF"),
                marker=dict(
                    symbol="cross",
                    size=11,
                    color="#F43F5E",
                    line=dict(width=1.2, color="#FFFFFF"),
                ),
                hovertemplate="<b>%{text}</b><br>Coord: (%{x:.0f}m, %{y:.0f}m)<extra>Medical Facility</extra>",
            )
        )

    _apply_obsidian_layout(fig, title="HALDWANI CITY ARTERIAL TOPOLOGY & EMERGENCY GREEN CORRIDOR MAP (SUMO METERS)", height=520)
    fig.update_layout(hovermode="closest")
    fig.update_xaxes(title_text="East-West Coordinate (meters from Mukhani)")
    fig.update_yaxes(title_text="North-South Coordinate (meters from Mukhani)", scaleanchor="x", scaleratio=1)
    return fig
