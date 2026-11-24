import urllib.request
import urllib.parse
import os

query = """
[out:xml][timeout:60];
(
  way["highway"~"motorway|trunk|primary|secondary|tertiary|residential|unclassified"](29.15,79.46,29.26,79.56);
);
(._;>;);
out body;
"""

servers = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 IntelliFlow/1.0"
}
data = urllib.parse.urlencode({"data": query}).encode("utf-8")

success = False
for server in servers:
    print(f"Trying {server}...")
    try:
        req = urllib.request.Request(server, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            print(f"Success from {server}! Bytes: {len(content):,}")
            if len(content) > 1000:
                with open("d:/final year/sumo/networks/haldwani_real_osm.osm", "wb") as f:
                    f.write(content)
                print("Saved to d:/final year/sumo/networks/haldwani_real_osm.osm")
                success = True
                break
    except Exception as e:
        print(f"Failed with {server}: {e}")

if not success:
    print("All direct Overpass attempts failed.")
