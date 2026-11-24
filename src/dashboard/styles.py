"""
IntelliFlow Design System Tokens & Obsidian Operations Console CSS.
Strict semantic isolation:
- Cobalt Blue (#2563EB) for navigation, controls, and interactive focus.
- Emerald (#10B981), Amber (#F59E0B), Red (#EF4444), Rose (#F43F5E) reserved
  strictly for signal states, queue saturation levels, and emergency preemption.
"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --bg-canvas: #0B0E14;
    --bg-surface: #121721;
    --bg-elevated: #181F2E;
    --border-subtle: #1E2638;
    --border-strong: #2E3A52;

    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;

    --accent-cobalt: #2563EB;
    --accent-cobalt-hover: #3B82F6;
    --accent-cobalt-tint: rgba(37, 99, 235, 0.14);

    --signal-green: #10B981;
    --signal-green-tint: rgba(16, 185, 129, 0.14);
    --signal-amber: #F59E0B;
    --signal-amber-tint: rgba(245, 158, 11, 0.14);
    --signal-red: #EF4444;
    --signal-red-tint: rgba(239, 68, 68, 0.14);
    --signal-emergency: #F43F5E;
    --signal-emergency-tint: rgba(244, 63, 94, 0.16);
    --ai-cyan: #06B6D4;
    --ai-cyan-tint: rgba(6, 182, 212, 0.14);
}

/* Global typography & canvas */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: var(--bg-canvas) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Compact high-density layout */
.block-container {
    padding-top: 1.1rem !important;
    padding-bottom: 1.5rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    max-width: 100% !important;
}

/* Hide default top Streamlit accent bar */
[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stHeader"] {
    background-color: rgba(11, 14, 20, 0.88) !important;
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border-subtle);
    height: 2.75rem !important;
}

/* Sidebar refinement */
[data-testid="stSidebar"] {
    background-color: #0D1119 !important;
    border-right: 1px solid var(--border-subtle) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-size: 0.84rem;
    color: var(--text-secondary);
}

/* Precision Tabs */
[data-testid="stTabs"] [role="tablist"] {
    gap: 0.35rem;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 0;
    margin-bottom: 0.9rem;
}

[data-testid="stTabs"] button[role="tab"] {
    background-color: transparent !important;
    border: 1px solid transparent !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 0.5rem 0.9rem !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
    color: var(--text-secondary) !important;
    transition: color 0.15s ease, background-color 0.15s ease;
}

[data-testid="stTabs"] button[role="tab"]:hover {
    color: var(--text-primary) !important;
    background-color: rgba(255, 255, 255, 0.03) !important;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--text-primary) !important;
    background-color: var(--bg-surface) !important;
    border-color: var(--border-subtle) var(--border-subtle) transparent var(--border-subtle) !important;
    border-bottom: 2px solid var(--accent-cobalt) !important;
}

/* Form controls & buttons */
[data-testid="stButton"] button {
    border-radius: 6px !important;
    border: 1px solid var(--border-strong) !important;
    background-color: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
    padding: 0.38rem 0.85rem !important;
    transition: border-color 0.15s ease, background-color 0.15s ease;
}

[data-testid="stButton"] button:hover {
    border-color: var(--accent-cobalt-hover) !important;
    background-color: #1F283B !important;
}

[data-testid="stButton"] button[kind="primary"] {
    background-color: var(--accent-cobalt) !important;
    border-color: var(--accent-cobalt-hover) !important;
    color: #FFFFFF !important;
}

[data-testid="stButton"] button[kind="primary"]:hover {
    background-color: var(--accent-cobalt-hover) !important;
}

/* Selectbox & Segmented Control */
[data-baseweb="select"] > div {
    background-color: var(--bg-surface) !important;
    border-color: var(--border-strong) !important;
    border-radius: 6px !important;
    font-size: 0.83rem !important;
}

/* Native Streamlit Metric Override (when used) */
[data-testid="stMetric"] {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 0.75rem 0.9rem;
}

[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-variant-numeric: tabular-nums !important;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    overflow: hidden;
}

/* Reusable HUD Classes */
.toc-mono {
    font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace !important;
    font-variant-numeric: tabular-nums !important;
}

.toc-micro-label {
    font-size: 10.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin: 0;
}

.toc-panel {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 14px 16px;
}

.toc-panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--border-subtle);
}

.toc-panel-title {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-secondary);
}

/* Top Operations Bar */
.toc-header-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    background-color: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 10px 16px;
    margin-bottom: 10px;
}

.toc-brand-group {
    display: flex;
    align-items: center;
    gap: 12px;
}

.toc-brand-mark {
    width: 10px;
    height: 28px;
    border-radius: 2px;
    background: linear-gradient(180deg, #10B981 0%, #2563EB 100%);
}

.toc-brand-title {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: var(--text-primary);
    line-height: 1.15;
}

.toc-brand-sub {
    font-size: 11.5px;
    color: var(--text-secondary);
    margin-top: 2px;
}

.toc-status-cluster {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
}

.toc-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-variant-numeric: tabular-nums;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.04em;
    border: 1px solid var(--border-strong);
    background-color: var(--bg-elevated);
    color: var(--text-secondary);
}

.toc-pill-ai {
    border-color: rgba(6, 182, 212, 0.35);
    background-color: var(--ai-cyan-tint);
    color: #22D3EE;
}

.toc-pill-green {
    border-color: rgba(16, 185, 129, 0.35);
    background-color: var(--signal-green-tint);
    color: #34D399;
}

.toc-pill-amber {
    border-color: rgba(245, 158, 11, 0.35);
    background-color: var(--signal-amber-tint);
    color: #FBBF24;
}

.toc-pill-red {
    border-color: rgba(239, 68, 68, 0.35);
    background-color: var(--signal-red-tint);
    color: #F87171;
}

.toc-pill-emergency {
    border-color: rgba(244, 63, 94, 0.65);
    background-color: var(--signal-emergency-tint);
    color: #FDA4AF;
    animation: tocPulse 1.4s ease-in-out infinite;
}

@keyframes tocPulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.4); }
    50% { box-shadow: 0 0 0 6px rgba(244, 63, 94, 0); }
}

/* KPI Grid */
.toc-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
    margin-bottom: 12px;
}

@media (max-width: 960px) {
    .toc-kpi-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

.toc-kpi-card {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.toc-kpi-val {
    font-family: 'JetBrains Mono', monospace;
    font-variant-numeric: tabular-nums;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin: 5px 0 4px 0;
    line-height: 1.1;
}

.toc-kpi-delta {
    font-family: 'JetBrains Mono', monospace;
    font-variant-numeric: tabular-nums;
    font-size: 11px;
    font-weight: 500;
    color: var(--text-secondary);
}

/* Segmented LED Queue Bar */
.led-row {
    background-color: #0E131D;
    border: 1px solid var(--border-subtle);
    border-radius: 5px;
    padding: 9px 11px;
    margin-bottom: 8px;
}

.led-row-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.led-approach-name {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-primary);
}

.led-approach-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    color: var(--text-muted);
}

.led-bar-track {
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 3px;
    margin-bottom: 6px;
}

.led-seg {
    height: 7px;
    border-radius: 1.5px;
    background-color: #1A2232;
}

.led-seg.on-green {
    background-color: #10B981;
    box-shadow: 0 0 6px rgba(16, 185, 129, 0.35);
}

.led-seg.on-amber {
    background-color: #F59E0B;
    box-shadow: 0 0 6px rgba(245, 158, 11, 0.35);
}

.led-seg.on-red {
    background-color: #EF4444;
    box-shadow: 0 0 6px rgba(239, 68, 68, 0.45);
}

.led-telemetry-line {
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-variant-numeric: tabular-nums;
    font-size: 11px;
    color: var(--text-secondary);
}

/* Phase Interlock Strip */
.interlock-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
    margin-top: 8px;
}

.interlock-cell {
    background-color: #0E131D;
    border: 1px solid var(--border-subtle);
    border-radius: 5px;
    padding: 8px 10px;
}

/* Emergency Banner */
.emergency-banner {
    background: linear-gradient(90deg, rgba(244, 63, 94, 0.16) 0%, rgba(239, 68, 68, 0.06) 100%);
    border: 1px solid rgba(244, 63, 94, 0.55);
    border-left: 4px solid #F43F5E;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

/* Custom subtle scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0B0E14;
}
::-webkit-scrollbar-thumb {
    background: #252F42;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #334155;
}
</style>
"""
