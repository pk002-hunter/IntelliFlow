import os
import requests
import subprocess
from pathlib import Path

OUT_DIR = Path("D:/final year/project/sumo/networks/haldwani_full")
SLICES_DIR = OUT_DIR / "osm_slices"
SLICES_DIR.mkdir(parents=True, exist_ok=True)

boxes = [
    ("central", "79.48,29.19,79.54,29.24"),
    ("north",   "79.50,29.24,79.55,29.28"),
    ("south",   "79.49,29.15,79.54,29.19"),
    ("west",    "79.44,29.19,79.48,29.24")
]

downloaded_files = []

for name, bbox in boxes:
    osm_file = SLICES_DIR / f"haldwani_{name}.osm"
    if osm_file.exists() and osm_file.stat().st_size > 100000:
        print(f"Already have {name}: {osm_file.stat().st_size:,} bytes")
        downloaded_files.append(str(osm_file))
        continue
        
    url = f"https://api.openstreetmap.org/api/0.6/map?bbox={bbox}"
    headers = {"User-Agent": f"IntelliFlowResearch_{name}/1.0 (Mozilla/5.0)"}
    print(f"Downloading {name} ({bbox})...")
    try:
        r = requests.get(url, headers=headers, timeout=45)
        print(f"  Status: {r.status_code}, Size: {len(r.content):,} bytes")
        if r.status_code == 200 and len(r.content) > 1000:
            with open(osm_file, "wb") as f:
                f.write(r.content)
            downloaded_files.append(str(osm_file))
        else:
            print(f"  Error downloading {name}: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"  Exception on {name}: {e}")

print(f"\nDownloaded {len(downloaded_files)} OSM files.")

if downloaded_files:
    sumo_home = os.environ.get("SUMO_HOME", r"C:\Program Files (x86)\Eclipse\Sumo")
    netconvert = os.path.join(sumo_home, "bin", "netconvert.exe")
    if not os.path.exists(netconvert):
        netconvert = "netconvert"

    output_net = OUT_DIR / "haldwani_osm_real.net.xml"
    
    cmd = [
        netconvert,
        "--osm-files", ",".join(downloaded_files),
        "-o", str(output_net),
        "--geometry.remove",
        "--roundabouts.guess",
        "--ramps.guess",
        "--junctions.join",
        "--tls.guess-signals",
        "--tls.discard-simple",
        "--tls.join",
        "--output.street-names", "true",
        "--remove-edges.isolated", "true"
    ]
    print(f"Running netconvert to generate {output_net}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Netconvert exit code:", res.returncode)
    if output_net.exists():
        print(f"Successfully generated real Haldwani road network! Size: {output_net.stat().st_size:,} bytes")
    else:
        print("Netconvert errors:\n", res.stderr[:1000])
