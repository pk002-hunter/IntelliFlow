"""
Helper script to compile SUMO node (.nod.xml) and edge (.edg.xml) files into a .net.xml file using netconvert.
"""
import os
import subprocess
import sys

def build_network(node_file, edge_file, output_net_file):
    netconvert_paths = [
        "netconvert",
        r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
        r"C:\Program Files\Eclipse\Sumo\bin\netconvert.exe",
        r"C:\sumo\bin\netconvert.exe"
    ]
    
    netconvert_cmd = None
    for path in netconvert_paths:
        if path == "netconvert" or os.path.exists(path):
            netconvert_cmd = path
            break

    if not netconvert_cmd:
        print("Error: netconvert executable not found.")
        return

    cmd = [
        netconvert_cmd,
        "--node-files", node_file,
        "--edge-files", edge_file,
        "--output-file", output_net_file,
        "--no-turnarounds", "true"
    ]
    print(f"Running netconvert command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Successfully generated network: {output_net_file}")
    else:
        print(f"netconvert error output:\n{result.stderr}")

if __name__ == "__main__":
    net_dir = "sumo/networks/single_intersection"
    nod = os.path.join(net_dir, "single_intersection.nod.xml")
    edg = os.path.join(net_dir, "single_intersection.edg.xml")
    net = os.path.join(net_dir, "single_intersection.net.xml")
    build_network(nod, edg, net)
