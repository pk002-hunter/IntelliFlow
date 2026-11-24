"""
IntelliFlow Operations HUD HTML & SVG Visual Components.
Designed for strict DOMPurify compatibility via st.html without Markdown parsing quirks.
"""
from __future__ import annotations

import textwrap
from typing import Any, Dict, List


def _compact_html(raw: str) -> str:
    """Strips blank lines and leading indentation so Markdown passes HTML/SVG untouched."""
    return "\n".join(line.strip() for line in raw.splitlines() if line.strip())


def _signal_colors(state: str) -> Dict[str, str]:
    """Returns recessed housing + optical glow gradient stop colors per bulb."""
    return {
        "red_core": "#EF4444" if state == "RED" else "#311216",
        "red_glow": "rgba(239, 68, 68, 0.55)" if state == "RED" else "rgba(0,0,0,0)",
        "amber_core": "#F59E0B" if state == "AMBER" else "#30220D",
        "amber_glow": "rgba(245, 158, 11, 0.55)" if state == "AMBER" else "rgba(0,0,0,0)",
        "green_core": "#10B981" if state == "GREEN" else "#0D2B22",
        "green_glow": "rgba(16, 185, 129, 0.55)" if state == "GREEN" else "rgba(0,0,0,0)",
    }


def render_command_header(
    controller_label: str,
    sim_step: int,
    diurnal_hour: int,
    emergency_active: bool,
    is_playing: bool,
) -> str:
    """Renders the top precision TOC status header bar."""
    if emergency_active:
        mode_pill = "<span class='toc-pill toc-pill-emergency'>PREEMPTION ACTIVE · STH CORRIDOR</span>"
    elif "PPO" in controller_label or "DQN" in controller_label:
        mode_pill = f"<span class='toc-pill toc-pill-ai'>AI AUTONOMOUS · {controller_label.upper()}</span>"
    elif "Fixed" in controller_label:
        mode_pill = "<span class='toc-pill toc-pill-amber'>BASELINE · WEBSTER FIXED-TIME</span>"
    else:
        mode_pill = "<span class='toc-pill toc-pill-red'>BASELINE · SENSOR-ACTUATED</span>"

    stream_pill = (
        "<span class='toc-pill toc-pill-green'>STREAM: PLAYING</span>"
        if is_playing
        else "<span class='toc-pill'>STREAM: PAUSED</span>"
    )

    return textwrap.dedent(f"""
    <div class="toc-header-bar">
        <div class="toc-brand-group">
            <div class="toc-brand-mark"></div>
            <div>
                <div class="toc-brand-title">INTELLIFLOW // TOC-HALDWANI</div>
                <div class="toc-brand-sub">Mukhani Chauraha 10-Lane Digital Twin · Eclipse SUMO + TraCI Telemetry · Sublane 0.5m</div>
            </div>
        </div>
        <div class="toc-status-cluster">
            {mode_pill}
            {stream_pill}
            <span class="toc-pill">CLOCK: {diurnal_hour:02d}:00 IST</span>
            <span class="toc-pill">STEP: T+{sim_step:04d}s</span>
        </div>
    </div>
    """).strip()


def render_kpi_strip(items: List[Dict[str, str]]) -> str:
    """Renders a 4-column industrial KPI strip with tabular monospace figures."""
    cards = []
    for item in items:
        accent_color = item.get("accent", "#94A3B8")
        cards.append(
            f"<div class='toc-kpi-card'>"
            f"  <div class='toc-micro-label'>{item['label']}</div>"
            f"  <div class='toc-kpi-val'>{item['value']}</div>"
            f"  <div class='toc-kpi-delta' style='color:{accent_color};'>{item['delta']}</div>"
            f"</div>"
        )
    return f"<div class='toc-kpi-grid'>{''.join(cards)}</div>"


def render_emergency_banner(emergency_active: bool) -> str:
    """Renders an active hospital preemption HUD alert when emergency mode is toggled."""
    if not emergency_active:
        return ""
    return textwrap.dedent("""
    <div class="emergency-banner">
        <div>
            <div class="toc-micro-label" style="color:#FDA4AF;">EMERGENCY CORRIDOR PREEMPTION ACTIVE</div>
            <div style="font-size:13px; font-weight:600; color:#F8FAFC; margin-top:2px;">
                Ambulance Priority Vector: Kaladhungi Rd (West) &rarr; Mukhani Junction &rarr; Rampur Rd (SH-49) &rarr; Dr. Susheela Tiwari Hospital (STH)
            </div>
        </div>
        <div class="toc-pill toc-pill-emergency">PHASE LOCK: EW GREEN · 0s AMBULANCE DELAY</div>
    </div>
    """).strip()


def _svg_signal_pod(x: int, y: int, state: str, label: str, grad_prefix: str) -> str:
    """Builds a realistic dark-housed 3-bulb traffic signal pod in SVG."""
    c = _signal_colors(state)
    # Use radial gradients for optical bloom without SVG <filter>
    defs = ""
    bloom = ""
    if state == "RED":
        defs = f"<radialGradient id='{grad_prefix}_rg'><stop offset='0%' stop-color='#EF4444' stop-opacity='0.75'/><stop offset='100%' stop-color='#EF4444' stop-opacity='0'/></radialGradient>"
        bloom = f"<circle cx='{x+12}' cy='{y+13}' r='14' fill='url(#{grad_prefix}_rg)'/>"
    elif state == "AMBER":
        defs = f"<radialGradient id='{grad_prefix}_ag'><stop offset='0%' stop-color='#F59E0B' stop-opacity='0.75'/><stop offset='100%' stop-color='#F59E0B' stop-opacity='0'/></radialGradient>"
        bloom = f"<circle cx='{x+12}' cy='{y+29}' r='14' fill='url(#{grad_prefix}_ag)'/>"
    elif state == "GREEN":
        defs = f"<radialGradient id='{grad_prefix}_gg'><stop offset='0%' stop-color='#10B981' stop-opacity='0.75'/><stop offset='100%' stop-color='#10B981' stop-opacity='0'/></radialGradient>"
        bloom = f"<circle cx='{x+12}' cy='{y+45}' r='14' fill='url(#{grad_prefix}_gg)'/>"

    return f"""
    <defs>{defs}</defs>
    <g>
        <rect x="{x}" y="{y}" width="24" height="58" rx="5" fill="#0B0E14" stroke="#2E3A52" stroke-width="1.2"/>
        {bloom}
        <circle cx="{x+12}" cy="{y+13}" r="5.2" fill="{c['red_core']}"/>
        <circle cx="{x+12}" cy="{y+29}" r="5.2" fill="{c['amber_core']}"/>
        <circle cx="{x+12}" cy="{y+45}" r="5.2" fill="{c['green_core']}"/>
        <text x="{x+12}" y="{y+70}" text-anchor="middle" fill="#64748B" font-family="JetBrains Mono, monospace" font-size="9" font-weight="600">{label}</text>
    </g>
    """


def _svg_queue_vehicles(approach: str, count: int, signal: str, emergency_active: bool) -> str:
    """Draws deterministic vehicle capsules queued or flowing along each Mukhani approach."""
    n_vis = min(max(0, count), 8)
    elems: List[str] = []
    # Mix colors representing Indian mixed traffic: 2W emerald/slate, Auto amber, Car cobalt
    fleet_palette = ["#94A3B8", "#3B82F6", "#F59E0B", "#94A3B8", "#3B82F6", "#8B5CF6", "#94A3B8", "#F59E0B"]
    edge_offset = 10 if signal == "GREEN" else 0

    for i in range(n_vis):
        color = fleet_palette[i % len(fleet_palette)]
        lane_slot = i % 2
        rank = i // 2
        if approach == "KW2M":
            # Entering from West on lower half of horizontal road (y=245..285)
            vx = 232 - (rank * 28) + edge_offset
            vy = 248 + (lane_slot * 18) + (6 if i % 3 == 2 else 0)
            elems.append(f"<rect x='{vx}' y='{vy}' width='16' height='8' rx='2' fill='{color}' stroke='#0B0E14' stroke-width='0.8'/>")
        elif approach == "KE2M":
            # Entering from East on upper half of horizontal road (y=170..215)
            vx = 472 + (rank * 28) - edge_offset
            vy = 180 + (lane_slot * 18)
            elems.append(f"<rect x='{vx}' y='{vy}' width='16' height='8' rx='2' fill='{color}' stroke='#0B0E14' stroke-width='0.8'/>")
        elif approach == "CN2M":
            # Entering from North on left half of vertical road (x=305..345)
            vx = 308 + (lane_slot * 20)
            vy = 135 - (rank * 26) + edge_offset
            elems.append(f"<rect x='{vx}' y='{vy}' width='8' height='16' rx='2' fill='{color}' stroke='#0B0E14' stroke-width='0.8'/>")
        elif approach == "CS2M":
            # Entering from South on right half of vertical road (x=372..412)
            vx = 374 + (lane_slot * 20)
            vy = 308 + (rank * 26) - edge_offset
            elems.append(f"<rect x='{vx}' y='{vy}' width='8' height='16' rx='2' fill='{color}' stroke='#0B0E14' stroke-width='0.8'/>")

    if emergency_active and approach == "KW2M":
        # Priority ambulance unit with Rose highlight
        elems.append("<rect x='256' y='262' width='22' height='10' rx='2.5' fill='#F43F5E' stroke='#FFFFFF' stroke-width='1.2'/>")
        elems.append("<text x='267' y='257' text-anchor='middle' fill='#FDA4AF' font-family='JetBrains Mono, monospace' font-size='8.5' font-weight='700'>AMB-01</text>")

    return "\n".join(elems)


def render_mukhani_digital_twin(state: Dict[str, Any]) -> str:
    """
    Renders a crisp, coordinate-grounded SVG schematic of Mukhani Chauraha (10-Lane Junction):
    - Kaladhungi Rd (E-W): 3 incoming lanes each side, 2 outgoing lanes each side
    - Canal Rd (N) & Rampur Rd (S): 2 incoming lanes, 2 outgoing lanes
    """
    apps = state["approaches"]
    ew_sig = state["ew_signal"]
    ns_sig = state["ns_signal"]
    emerg = state["emergency_active"]

    pod_kw = _svg_signal_pod(234, 304, ew_sig, "KW2M", "kw")
    pod_ke = _svg_signal_pod(462, 92, ew_sig, "KE2M", "ke")
    pod_cn = _svg_signal_pod(248, 92, ns_sig, "CN2M", "cn")
    pod_cs = _svg_signal_pod(448, 304, ns_sig, "CS2M", "cs")

    vehs_kw = _svg_queue_vehicles("KW2M", apps["KW2M"]["queue_int"], ew_sig, emerg)
    vehs_ke = _svg_queue_vehicles("KE2M", apps["KE2M"]["queue_int"], ew_sig, emerg)
    vehs_cn = _svg_queue_vehicles("CN2M", apps["CN2M"]["queue_int"], ns_sig, emerg)
    vehs_cs = _svg_queue_vehicles("CS2M", apps["CS2M"]["queue_int"], ns_sig, emerg)

    # Center status color
    box_border = "#F43F5E" if emerg else ("#10B981" if ew_sig == "GREEN" or ns_sig == "GREEN" else "#F59E0B")
    phase_short = "STH PREEMPT" if emerg else f"PHASE {state['phase_code']}"
    active_axis = "EW + STH TURN" if emerg else ("EW KALADHUNGI" if ew_sig in ("GREEN", "AMBER") else "NS CANAL/RAMPUR")

    # Active flow corridors inside intersection box
    flow_overlay = ""
    if emerg:
        flow_overlay = """
        <path d="M 30 267 L 330 267 Q 375 267 375 315 L 375 442" fill="none" stroke="#F43F5E" stroke-width="3.5" stroke-dasharray="8 5" opacity="0.9"/>
        <polygon points="375,448 369,436 381,436" fill="#F43F5E"/>
        <rect x="405" y="388" width="166" height="22" rx="4" fill="#2A0E16" stroke="#F43F5E" stroke-width="1"/>
        <text x="488" y="402" text-anchor="middle" fill="#FDA4AF" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700">STH HOSPITAL ROUTE (1.8km)</text>
        """
    elif ew_sig == "GREEN":
        flow_overlay = """
        <path d="M 60 256 L 660 256" stroke="#10B981" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.5"/>
        <path d="M 660 198 L 60 198" stroke="#10B981" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.5"/>
        """
    elif ns_sig == "GREEN":
        flow_overlay = """
        <path d="M 326 40 L 326 420" stroke="#10B981" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.5"/>
        <path d="M 392 420 L 392 40" stroke="#10B981" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.5"/>
        """

    svg = f"""
    <div class="toc-panel" style="padding:12px 14px;">
        <div class="toc-panel-header" style="margin-bottom:8px;">
            <span class="toc-panel-title">INTERSECTION DIGITAL TWIN // MUKHANI CHAURAHA (4-WAY · 10 INBOUND LANES)</span>
            <span class="toc-mono" style="font-size:11px; color:#94A3B8;">DWELL: {state['dwell_sec']:02d}s · {state['safety_note']}</span>
        </div>
        <svg viewBox="0 0 720 460" width="100%" style="display:block; background:#090C12; border-radius:5px; border:1px solid #1E2638;">
            <!-- Quadrant Urban Blocks -->
            <rect x="0" y="0" width="290" height="165" fill="#0D1119"/>
            <rect x="430" y="0" width="290" height="165" fill="#0D1119"/>
            <rect x="0" y="295" width="290" height="165" fill="#0D1119"/>
            <rect x="430" y="295" width="290" height="165" fill="#0D1119"/>

            <!-- Road Surfaces (Kaladhungi E-W & Canal/Rampur N-S) -->
            <rect x="0" y="165" width="720" height="130" fill="#151B26"/>
            <rect x="290" y="0" width="140" height="460" fill="#151B26"/>
            <rect x="290" y="165" width="140" height="130" fill="#18202E"/>

            <!-- Road Edge Curbs -->
            <line x1="0" y1="165" x2="290" y2="165" stroke="#2D3A52" stroke-width="1.5"/>
            <line x1="430" y1="165" x2="720" y2="165" stroke="#2D3A52" stroke-width="1.5"/>
            <line x1="0" y1="295" x2="290" y2="295" stroke="#2D3A52" stroke-width="1.5"/>
            <line x1="430" y1="295" x2="720" y2="295" stroke="#2D3A52" stroke-width="1.5"/>
            <line x1="290" y1="0" x2="290" y2="165" stroke="#2D3A52" stroke-width="1.5"/>
            <line x1="290" y1="295" x2="290" y2="460" stroke="#2D3A52" stroke-width="1.5"/>
            <line x1="430" y1="0" x2="430" y2="165" stroke="#2D3A52" stroke-width="1.5"/>
            <line x1="430" y1="295" x2="430" y2="460" stroke="#2D3A52" stroke-width="1.5"/>

            <!-- Median Dividers -->
            <line x1="0" y1="230" x2="285" y2="230" stroke="#F59E0B" stroke-width="1.5" stroke-opacity="0.65"/>
            <line x1="435" y1="230" x2="720" y2="230" stroke="#F59E0B" stroke-width="1.5" stroke-opacity="0.65"/>
            <line x1="360" y1="0" x2="360" y2="160" stroke="#F59E0B" stroke-width="1.5" stroke-opacity="0.65"/>
            <line x1="360" y1="300" x2="360" y2="460" stroke="#F59E0B" stroke-width="1.5" stroke-opacity="0.65"/>

            <!-- Dashed Lane Markings (3 incoming lanes on EW, 2 on NS) -->
            <line x1="0" y1="196" x2="280" y2="196" stroke="#334155" stroke-width="1" stroke-dasharray="7 7"/>
            <line x1="0" y1="252" x2="280" y2="252" stroke="#334155" stroke-width="1" stroke-dasharray="7 7"/>
            <line x1="0" y1="274" x2="280" y2="274" stroke="#334155" stroke-width="1" stroke-dasharray="7 7"/>
            <line x1="440" y1="186" x2="720" y2="186" stroke="#334155" stroke-width="1" stroke-dasharray="7 7"/>
            <line x1="440" y1="208" x2="720" y2="208" stroke="#334155" stroke-width="1" stroke-dasharray="7 7"/>
            <line x1="440" y1="262" x2="720" y2="262" stroke="#334155" stroke-width="1" stroke-dasharray="7 7"/>
            <line x1="325" y1="0" x2="325" y2="155" stroke="#334155" stroke-width="1" stroke-dasharray="7 7"/>
            <line x1="395" y1="0" x2="395" y2="155" stroke="#334155" stroke-width="1" stroke-dasharray="7 7"/>
            <line x1="325" y1="305" x2="325" y2="460" stroke="#334155" stroke-width="1" stroke-dasharray="7 7"/>
            <line x1="395" y1="305" x2="395" y2="460" stroke="#334155" stroke-width="1" stroke-dasharray="7 7"/>

            <!-- Stop Lines -->
            <line x1="286" y1="232" x2="286" y2="293" stroke="#E2E8F0" stroke-width="2.5"/>
            <line x1="434" y1="167" x2="434" y2="228" stroke="#E2E8F0" stroke-width="2.5"/>
            <line x1="292" y1="161" x2="358" y2="161" stroke="#E2E8F0" stroke-width="2.5"/>
            <line x1="362" y1="299" x2="428" y2="299" stroke="#E2E8F0" stroke-width="2.5"/>

            <!-- Flow & Emergency Vector Overlay -->
            {flow_overlay}

            <!-- Live Vehicle Queues -->
            {vehs_kw}
            {vehs_ke}
            {vehs_cn}
            {vehs_cs}

            <!-- Center Junction Controller Box -->
            <rect x="307" y="196" width="106" height="68" rx="5" fill="#0B0E14" stroke="{box_border}" stroke-width="1.5"/>
            <text x="360" y="216" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9" font-weight="600">{phase_short}</text>
            <text x="360" y="233" text-anchor="middle" fill="#F8FAFC" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="700">{active_axis}</text>
            <text x="360" y="250" text-anchor="middle" fill="{box_border}" font-family="JetBrains Mono, monospace" font-size="10" font-weight="600">Q: {state['total_halting']:.1f} | {state['mean_speed_kmh']:.1f} km/h</text>

            <!-- 4 Realistic Signal Pods -->
            {pod_kw}
            {pod_ke}
            {pod_cn}
            {pod_cs}

            <!-- Approach Labels & Queue Readouts -->
            <text x="16" y="152" fill="#94A3B8" font-family="Inter, sans-serif" font-size="10.5" font-weight="600">KALADHUNGI RD (WEST · SH-41)</text>
            <text x="16" y="314" fill="#64748B" font-family="JetBrains Mono, monospace" font-size="10">IN: 3 LANES · Q={apps['KW2M']['queue']:.1f} VEH · {apps['KW2M']['speed_kmh']:.1f} KM/H</text>

            <text x="704" y="152" text-anchor="end" fill="#94A3B8" font-family="Inter, sans-serif" font-size="10.5" font-weight="600">KALADHUNGI RD (EAST · TIKONIA)</text>
            <text x="704" y="314" text-anchor="end" fill="#64748B" font-family="JetBrains Mono, monospace" font-size="10">IN: 3 LANES · Q={apps['KE2M']['queue']:.1f} VEH · {apps['KE2M']['speed_kmh']:.1f} KM/H</text>

            <text x="360" y="22" text-anchor="middle" fill="#94A3B8" font-family="Inter, sans-serif" font-size="10.5" font-weight="600">CANAL RD / HEERA NAGAR (NORTH · 2L)</text>
            <text x="360" y="446" text-anchor="middle" fill="#94A3B8" font-family="Inter, sans-serif" font-size="10.5" font-weight="600">CHHOTI MUKHANI / RAMPUR RD &rarr; STH HOSPITAL (SOUTH · 2L)</text>
        </svg>
    </div>
    """
    return _compact_html(svg)


def render_led_queue_panel(state: Dict[str, Any]) -> str:
    """Renders 10-segment LED VU bars for all 4 approaches with tabular readouts."""
    rows_html: List[str] = []
    for aid in ["KW2M", "KE2M", "CN2M", "CS2M"]:
        app = state["approaches"][aid]
        sat = float(app["sat_pct"])
        lit_count = int(round(sat / 10.0))
        sig = app["signal"]
        sig_pill = (
            "toc-pill-green" if sig == "GREEN" else ("toc-pill-amber" if sig == "AMBER" else "toc-pill-red")
        )

        segs = []
        for idx in range(1, 11):
            if idx <= lit_count:
                if idx <= 3:
                    cls = "led-seg on-green"
                elif idx <= 7:
                    cls = "led-seg on-amber"
                else:
                    cls = "led-seg on-red"
            else:
                cls = "led-seg"
            segs.append(f"<div class='{cls}'></div>")

        rows_html.append(f"""
        <div class="led-row">
            <div class="led-row-head">
                <div>
                    <span class="led-approach-name">{app['name']}</span>
                    <span class="led-approach-sub"> · {aid}</span>
                </div>
                <span class="toc-pill {sig_pill}" style="padding:2px 7px; font-size:10px;">{sig}</span>
            </div>
            <div class="led-bar-track">{''.join(segs)}</div>
            <div class="led-telemetry-line">
                <span>QUEUE: <strong style="color:#F8FAFC;">{app['queue']:.1f}</strong> veh</span>
                <span>SPD: <strong style="color:#F8FAFC;">{app['speed_kmh']:.1f}</strong> km/h</span>
                <span>SAT: <strong style="color:#F8FAFC;">{int(sat)}%</strong></span>
            </div>
        </div>
        """)

    return textwrap.dedent(f"""
    <div class="toc-panel">
        <div class="toc-panel-header">
            <span class="toc-panel-title">APPROACH SATURATION & LED QUEUE METERS</span>
            <span class="toc-mono" style="font-size:10.5px; color:#64748B;">10-SEG VU</span>
        </div>
        {''.join(rows_html)}
        <div style="font-size:10.5px; color:#64748B; margin-top:6px;">
            Junction totals from SUMO step trace; approach splits weighted by calibrated directional demand.
        </div>
    </div>
    """).strip()


def render_phase_interlock_strip(state: Dict[str, Any]) -> str:
    """Renders hardware safety interlocks and phase dwell verification strip."""
    min_green_cls = "toc-pill-green" if state["min_green_ok"] else "toc-pill-amber"
    min_green_txt = "SATISFIED (>= 5s)" if state["min_green_ok"] else f"LOCKED ({state['dwell_sec']}s / 5s)"
    starvation_txt = "NOMINAL (< 120s)" if state["waiting_time"] < 120 else "PENALTY ACTIVE"
    starvation_cls = "toc-pill-green" if state["waiting_time"] < 120 else "toc-pill-amber"

    return textwrap.dedent(f"""
    <div class="toc-panel" style="margin-top:10px;">
        <div class="toc-panel-header" style="margin-bottom:8px;">
            <span class="toc-panel-title">SIGNAL SAFETY INTERLOCK & PHASE ENFORCEMENT</span>
            <span class="toc-mono" style="font-size:11px; color:#22D3EE;">{state['phase_name']}</span>
        </div>
        <div class="interlock-grid">
            <div class="interlock-cell">
                <div class="toc-micro-label">MIN GREEN FLOOR</div>
                <div style="margin-top:5px;"><span class="toc-pill {min_green_cls}" style="font-size:10px;">{min_green_txt}</span></div>
            </div>
            <div class="interlock-cell">
                <div class="toc-micro-label">YELLOW CLEARANCE</div>
                <div style="margin-top:5px;"><span class="toc-pill toc-pill-amber" style="font-size:10px;">3.0s ARMED</span></div>
            </div>
            <div class="interlock-cell">
                <div class="toc-micro-label">STARVATION GUARD</div>
                <div style="margin-top:5px;"><span class="toc-pill {starvation_cls}" style="font-size:10px;">{starvation_txt}</span></div>
            </div>
        </div>
    </div>
    """).strip()


def render_architecture_svg() -> str:
    """Renders closed-loop SUMO + Gymnasium + PPO control architecture schematic."""
    return _compact_html("""
    <div class="toc-panel">
        <div class="toc-panel-header">
            <span class="toc-panel-title">CLOSED-LOOP CONTROL ARCHITECTURE // TRACI &harr; GYMNASIUM &harr; PPO</span>
            <span class="toc-pill toc-pill-ai" style="font-size:10px;">PHASE 1 CORE OPERATIONAL</span>
        </div>
        <svg viewBox="0 0 860 210" width="100%" style="display:block; background:#090C12; border-radius:5px; border:1px solid #1E2638;">
            <!-- Block 1: SUMO Simulation -->
            <rect x="24" y="42" width="185" height="120" rx="6" fill="#121721" stroke="#2563EB" stroke-width="1.5"/>
            <text x="116" y="68" text-anchor="middle" fill="#60A5FA" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="700">ECLIPSE SUMO ENGINE</text>
            <text x="116" y="88" text-anchor="middle" fill="#E2E8F0" font-family="Inter, sans-serif" font-size="11" font-weight="600">Microscopic Sublane Physics</text>
            <text x="116" y="108" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9.5">Mukhani 10L / Haldwani City</text>
            <text x="116" y="124" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9.5">Krauss 0.5m Lateral Res</text>
            <text x="116" y="142" text-anchor="middle" fill="#10B981" font-family="JetBrains Mono, monospace" font-size="9.5">HBEFA3 Emissions + TraCI</text>

            <!-- Arrow 1 -> 2 -->
            <line x1="209" y1="84" x2="275" y2="84" stroke="#3B82F6" stroke-width="1.8"/>
            <polygon points="282,84 272,79 272,89" fill="#3B82F6"/>
            <text x="245" y="74" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9">Lane State</text>

            <!-- Block 2: Gymnasium Env -->
            <rect x="282" y="42" width="185" height="120" rx="6" fill="#121721" stroke="#2E3A52" stroke-width="1.5"/>
            <text x="374" y="68" text-anchor="middle" fill="#22D3EE" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="700">GYMNASIUM ENV</text>
            <text x="374" y="88" text-anchor="middle" fill="#E2E8F0" font-family="Inter, sans-serif" font-size="11" font-weight="600">SumoTrafficEnv Wrapper</text>
            <text x="374" y="108" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9.5">Obs: Box(43,) in [0, 1]</text>
            <text x="374" y="124" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9.5">Act: Discrete(2) Phases</text>
            <text x="374" y="142" text-anchor="middle" fill="#F59E0B" font-family="JetBrains Mono, monospace" font-size="9.5">Delta Step: 5s | Yellow: 3s</text>

            <!-- Arrow 2 -> 3 -->
            <line x1="467" y1="84" x2="533" y2="84" stroke="#06B6D4" stroke-width="1.8"/>
            <polygon points="540,84 530,79 530,89" fill="#06B6D4"/>
            <text x="503" y="74" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9">43D Vector</text>

            <!-- Block 3: PPO Actor-Critic -->
            <rect x="540" y="42" width="165" height="120" rx="6" fill="#121721" stroke="#10B981" stroke-width="1.5"/>
            <text x="622" y="68" text-anchor="middle" fill="#34D399" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="700">PPO ACTOR-CRITIC</text>
            <text x="622" y="88" text-anchor="middle" fill="#E2E8F0" font-family="Inter, sans-serif" font-size="11" font-weight="600">Policy Optimization</text>
            <text x="622" y="108" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9.5">Clipped Surrogate (0.2)</text>
            <text x="622" y="124" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9.5">GAE Advantage Estimator</text>
            <text x="622" y="142" text-anchor="middle" fill="#10B981" font-family="JetBrains Mono, monospace" font-size="9.5">Double DQN Benchmarked</text>

            <!-- Block 4: Safety Interlock -->
            <rect x="730" y="42" width="110" height="120" rx="6" fill="#121721" stroke="#F59E0B" stroke-width="1.5"/>
            <text x="785" y="68" text-anchor="middle" fill="#FBBF24" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700">INTERLOCK</text>
            <text x="785" y="92" text-anchor="middle" fill="#E2E8F0" font-family="Inter, sans-serif" font-size="10.5" font-weight="600">Safety Matrix</text>
            <text x="785" y="114" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9">Min Green 5s</text>
            <text x="785" y="130" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9">Yellow 3s</text>
            <text x="785" y="146" text-anchor="middle" fill="#F43F5E" font-family="JetBrains Mono, monospace" font-size="9">Amb Preempt</text>

            <!-- Arrow 3 -> 4 -->
            <line x1="705" y1="102" x2="723" y2="102" stroke="#10B981" stroke-width="1.8"/>
            <polygon points="730,102 720,97 720,107" fill="#10B981"/>

            <!-- Feedback Return Line 4 -> 1 -->
            <path d="M 785 162 L 785 188 L 116 188 L 116 168" fill="none" stroke="#64748B" stroke-width="1.5" stroke-dasharray="5 4"/>
            <polygon points="116,162 111,171 121,171" fill="#64748B"/>
            <text x="450" y="183" text-anchor="middle" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9.5">TraCI Actuation: setPhase(tls_id, green_or_yellow_idx)</text>
        </svg>
    </div>
    """)


def render_phase2_roadmap_card() -> str:
    """Renders non-blocking Phase 2 Edge Computer Vision / YOLO deployment roadmap."""
    return textwrap.dedent("""
    <div class="toc-panel" style="border-left: 3px solid #2563EB;">
        <div class="toc-panel-header">
            <span class="toc-panel-title">PHASE 2 HARDWARE ROADMAP // EDGE COMPUTER VISION & YOLO BRIDGE</span>
            <span class="toc-pill" style="border-color:rgba(37,99,235,0.45); background:rgba(37,99,235,0.14); color:#60A5FA;">FUTURE DEPLOYMENT PHASE</span>
        </div>
        <div style="font-size:12.5px; color:#94A3B8; line-height:1.55; margin-bottom:12px;">
            Physical CCTV integration via TensorRT YOLOv8/YOLOv11 is explicitly scheduled for <strong style="color:#F8FAFC;">Phase 2 Field Deployment</strong>.
            Phase 1 (current operations console) runs directly over calibrated Eclipse SUMO microscopic telemetry and TraCI IPC without requiring live camera streams.
        </div>
        <div style="display:grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap:8px;">
            <div class="interlock-cell">
                <div class="toc-micro-label">STAGE 01 · INGESTION</div>
                <div style="font-size:12px; font-weight:600; color:#F8FAFC; margin-top:4px;">1080p RTSP CCTV Feeds</div>
                <div class="toc-mono" style="font-size:10.5px; color:#64748B; margin-top:3px;">4 Approach Poles @ 30 FPS</div>
            </div>
            <div class="interlock-cell">
                <div class="toc-micro-label">STAGE 02 · PERCEPTION</div>
                <div style="font-size:12px; font-weight:600; color:#F8FAFC; margin-top:4px;">YOLOv8 TensorRT FP16</div>
                <div class="toc-mono" style="font-size:10.5px; color:#64748B; margin-top:3px;">Virtual 150m Polygon Zones</div>
            </div>
            <div class="interlock-cell">
                <div class="toc-micro-label">STAGE 03 · NORMALIZATION</div>
                <div style="font-size:12px; font-weight:600; color:#F8FAFC; margin-top:4px;">Indian PCU Weighting</div>
                <div class="toc-mono" style="font-size:10.5px; color:#64748B; margin-top:3px;">2W:0.5 | Auto:0.8 | Car:1 | Bus:3</div>
            </div>
            <div class="interlock-cell">
                <div class="toc-micro-label">STAGE 04 · EDGE INFERENCE</div>
                <div style="font-size:12px; font-weight:600; color:#F8FAFC; margin-top:4px;">Jetson Orin Nano</div>
                <div class="toc-mono" style="font-size:10.5px; color:#10B981; margin-top:3px;">&lt; 15ms End-to-End Target</div>
            </div>
        </div>
    </div>
    """).strip()
