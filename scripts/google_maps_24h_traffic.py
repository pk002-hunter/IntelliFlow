"""
IntelliFlow: 24-Hour Google Maps Traffic Ingestion & SUMO Demand Calibration.
Translates 24-hour Google Maps congestion ratios (duration_in_traffic / duration)
into microscopic SUMO vehicle inflow rates using the Bureau of Public Roads (BPR) function.
"""
import os
import sys
import argparse
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "sumo" / "networks" / "mukhani_chauraha"

# ==============================================================================
# 1. 24-HOUR GOOGLE MAPS PROBE SPEED & CONGESTION PROFILE (MUKHANI CHAURAHA)
# Extracted from typical weekday Google Maps traffic index (Wednesday baseline):
#   - Delay Index: T_traffic / T_free (1.0 = Free flow, >2.5 = Dark Red Standstill)
# ==============================================================================
HOURLY_GOOGLE_MAPS_PROFILE = {
    # Hour: (Delay_Ratio, Dominant_Direction, Description)
    0:  (1.00, "balanced", "Midnight Lull: Bareilly Freight Trucks"),
    1:  (1.00, "balanced", "Night Quiet: Long-distance Intercity Cabs"),
    2:  (1.00, "balanced", "Night Freight Transfer to Transport Nagar"),
    3:  (1.00, "balanced", "Early Morning Agricultural Supply to Mandi"),
    4:  (1.05, "balanced", "Pre-Dawn Milk & Produce Supply Pickups"),
    5:  (1.10, "balanced", "Kathgodam Morning Railway Arrivals (Ranikhet Exp)"),
    6:  (1.20, "inbound",  "Early Commute & School Bus Departures"),
    7:  (1.45, "inbound",  "Morning Rush Buildup: Kusumkhera to Center"),
    8:  (2.65, "inbound",  "🌅 MORNING PEAK HOUR: Severe Office/College Rush"),
    9:  (2.95, "inbound",  "🌅 MORNING PEAK PEAK: Nainital Rd & Kaladhungi Standstill"),
    10: (2.30, "inbound",  "Late Morning Administrative Inflow"),
    11: (1.50, "balanced", "Midday Commercial & Banking Transit"),
    12: (1.40, "balanced", "Afternoon Local Shopping & Business"),
    13: (1.30, "balanced", "Lunch Hour Slump: Moderate Traffic"),
    14: (1.45, "outbound", "School Dismissal Peak: Buses & Autos"),
    15: (1.35, "balanced", "Afternoon Inter-City Transit to Kathgodam"),
    16: (1.70, "outbound", "Early Evening Dispersal Begins"),
    17: (2.40, "outbound", "🌆 EVENING PEAK BUILDUP: Commercial Center Exits"),
    18: (3.15, "outbound", "🌆 EVENING PEAK MAX: Severe Gridlock at Chauraha"),
    19: (3.10, "outbound", "🌆 EVENING PEAK: Suburb Dispersal & Canal Rd Backup"),
    20: (2.20, "outbound", "Market Shopping & Dinner Rush"),
    21: (1.60, "balanced", "Market Shop Closures & Bareilly Rd Freight Entry"),
    22: (1.25, "balanced", "Night Long-distance Buses (Uttarakhand Roadways)"),
    23: (1.10, "balanced", "Late Night Easing: Regional Highway Transit")
}


def bpr_delay_to_flow(delay_ratio, capacity=1800, alpha=0.15, beta=4.0):
    """
    Inverse Bureau of Public Roads (BPR) volume-delay formulation:
    T / T0 = 1 + alpha * (V / C)^beta
    => V = C * ((T / T0 - 1) / alpha)^(1 / beta)
    """
    if delay_ratio <= 1.0:
        return int(capacity * 0.12)  # Baseline minimum midnight flow
    
    over_ratio = max(0.0, (delay_ratio - 1.0) / alpha)
    flow = capacity * (over_ratio ** (1.0 / beta))
    return int(np.clip(flow, 150, 2700))


def generate_24h_sumo_routes(output_path=None):
    """Generates a complete 24-hour microscopic SUMO route file."""
    if output_path is None:
        output_path = OUTPUT_DIR / "mukhani_24h.rou.xml"

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!-- ============================================================== -->',
        '<!-- 24-HOUR CALIBRATED TRAFFIC DEMAND: MUKHANI CHAURAHA, HALDWANI -->',
        '<!-- Sourced from 24-Hour Google Maps Typical Probe Congestion Data -->',
        '<!-- ============================================================== -->',
        '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">',
        '    <!-- Indian PCU Vehicle Fleet (UK-04 Haldwani RTO Calibrated) -->',
        '    <vType id="two_wheeler" accel="3.2" decel="4.5" length="2.2" width="0.8" maxSpeed="13.89" minGap="0.8" color="yellow" carFollowModel="Krauss"/>',
        '    <vType id="car" accel="2.6" decel="4.5" length="4.5" width="1.8" maxSpeed="13.89" minGap="1.5" color="blue" carFollowModel="Krauss"/>',
        '    <vType id="auto" accel="2.0" decel="3.5" length="2.8" width="1.3" maxSpeed="11.11" minGap="1.0" color="green" carFollowModel="Krauss"/>',
        '    <vType id="bus" accel="1.5" decel="3.0" length="10.5" width="2.5" maxSpeed="10.0" minGap="2.5" color="red" carFollowModel="Krauss"/>',
        '    <vType id="truck" accel="1.2" decel="2.5" length="9.0" width="2.4" maxSpeed="9.0" minGap="3.0" color="orange" carFollowModel="Krauss"/>',
        '    <vType id="emergency" vClass="emergency" accel="3.5" decel="5.0" length="5.5" width="2.0" maxSpeed="16.67" color="white" carFollowModel="Krauss"/>',
        '',
        '    <!-- Mukhani Chauraha Approach Routes -->',
        '    <route id="r_KW2KE" edges="KW2M M2KE"/>',
        '    <route id="r_KE2KW" edges="KE2M M2KW"/>',
        '    <route id="r_CN2CS" edges="CN2M M2CS"/>',
        '    <route id="r_CS2CN" edges="CS2M M2CN"/>',
        '    <route id="r_CN2KW" edges="CN2M M2KW"/>',
        '    <route id="r_KW2CS" edges="KW2M M2CS"/>',
        ''
    ]

    for hour, (delay, direction, desc) in HOURLY_GOOGLE_MAPS_PROFILE.items():
        start_sec = hour * 3600
        end_sec = (hour + 1) * 3600
        base_flow = bpr_delay_to_flow(delay)

        # Directional split adjustment (D-factor)
        if direction == "inbound":
            flow_north = int(base_flow * 0.45)
            flow_west = int(base_flow * 0.35)
            flow_south = int(base_flow * 0.10)
            flow_east = int(base_flow * 0.10)
        elif direction == "outbound":
            flow_north = int(base_flow * 0.12)
            flow_west = int(base_flow * 0.13)
            flow_south = int(base_flow * 0.35)
            flow_east = int(base_flow * 0.40)
        else:
            flow_north = int(base_flow * 0.28)
            flow_west = int(base_flow * 0.27)
            flow_south = int(base_flow * 0.23)
            flow_east = int(base_flow * 0.22)

        xml_lines.append(f'    <!-- HOUR {hour:02d}:00 - {hour+1:02d}:00 | {desc} (Total: ~{base_flow} veh/hr) -->')
        # Inflows by mode
        xml_lines.append(f'    <flow id="h{hour:02d}_N_bike" type="two_wheeler" route="r_CN2CS" begin="{start_sec}" end="{end_sec}" vehsPerHour="{max(10, int(flow_north*0.58))}"/>')
        xml_lines.append(f'    <flow id="h{hour:02d}_N_car"  type="car" route="r_CN2CS" begin="{start_sec}" end="{end_sec}" vehsPerHour="{max(5, int(flow_north*0.28))}"/>')
        xml_lines.append(f'    <flow id="h{hour:02d}_W_bike" type="two_wheeler" route="r_KW2KE" begin="{start_sec}" end="{end_sec}" vehsPerHour="{max(10, int(flow_west*0.58))}"/>')
        xml_lines.append(f'    <flow id="h{hour:02d}_W_car"  type="car" route="r_KW2KE" begin="{start_sec}" end="{end_sec}" vehsPerHour="{max(5, int(flow_west*0.28))}"/>')
        xml_lines.append(f'    <flow id="h{hour:02d}_S_car"  type="car" route="r_CS2CN" begin="{start_sec}" end="{end_sec}" vehsPerHour="{max(5, int(flow_south*0.35))}"/>')
        xml_lines.append(f'    <flow id="h{hour:02d}_E_bike" type="two_wheeler" route="r_KE2KW" begin="{start_sec}" end="{end_sec}" vehsPerHour="{max(10, int(flow_east*0.60))}"/>')

        # Add ambulances during busy daytime and peak hours
        if 8 <= hour <= 21:
            xml_lines.append(f'    <flow id="h{hour:02d}_amb" type="emergency" route="r_CN2CS" begin="{start_sec+120}" end="{end_sec}" period="450"/>')

    xml_lines.append('</routes>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))
    
    print(f"✅ Generated 24-Hour Google Maps Calibrated Route Schedule:")
    print(f"   • Path: {output_path} ({os.path.getsize(output_path):,} bytes)")
    return output_path


def print_24h_summary():
    """Prints tabular summary of the 24-hour Google Maps profile."""
    print("\n" + "=" * 90)
    print("📍 24-HOUR GOOGLE MAPS TRAFFIC DIURNAL PROFILE: MUKHANI CHAURAHA, HALDWANI")
    print("=" * 90)
    print(f"{'Hour':<6} | {'Time Window':<15} | {'Google Delay Ratio':<20} | {'Derived Flow':<16} | {'Traffic Nature'}")
    print("-" * 90)
    for hour, (delay, direction, desc) in HOURLY_GOOGLE_MAPS_PROFILE.items():
        flow = bpr_delay_to_flow(delay)
        color_tag = "🔴 [Peak]" if delay > 2.5 else ("🟠 [Medium]" if delay > 1.4 else "🟢 [Free]")
        time_str = f"{hour:02d}:00 - {hour+1:02d}:00"
        print(f"{hour:<6} | {time_str:<15} | {delay:>5.2f}x ({color_tag:<10}) | {flow:>5d} veh/hr    | {desc}")
    print("=" * 90)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="24-Hour Google Maps Traffic Ingestion for Mukhani Chauraha")
    parser.add_argument("--summary", action="store_true", help="Print 24-hour tabular profile")
    parser.add_argument("--generate", action="store_true", default=True, help="Generate 24-hour SUMO route XML")
    args = parser.parse_args()

    print_24h_summary()
    if args.generate:
        generate_24h_sumo_routes()
