"""
Update build_colab_notebook.py to include Brijlal, Krishna, and Kathgodam hospitals and gully roads.
"""
from pathlib import Path

script_path = Path("D:/final year/project/scripts/build_colab_notebook.py")
code = script_path.read_text(encoding="utf-8")

old_step_2_end = """# 6. Master SUMO Configuration with Sublane Physics (0.5m lateral resolution)
sumocfg_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <input>
        <net-file value="mukhani.net.xml"/>
        <route-files value="mukhani.rou.xml"/>
    </input>"""

new_step_2_end = """# 6. Define Landmark POIs for Major Hospitals & Emergency Gully Approaches
landmarks_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <!-- 🏥 Kathgodam & Upper Nainital Road Hospitals -->
    <poi id="HOSP_BRIJLAL" type="hospital" color="1.0,0.1,0.1" layer="150" x="0.0" y="200.0" width="60" height="60" name="🏥 BRIJLAL HOSPITAL &amp; RESEARCH CENTRE (Kathgodam/Nainital Rd - Cardiac &amp; Neuro Trauma)"/>
    <poi id="HOSP_KRISHNA" type="hospital" color="1.0,0.1,0.1" layer="150" x="30.0" y="160.0" width="50" height="50" name="🏥 KRISHNA HOSPITAL &amp; RESEARCH CENTRE (Trauma Centre)"/>
    <poi id="HOSP_KATHGODAM" type="hospital" color="1.0,0.1,0.1" layer="150" x="0.0" y="250.0" width="50" height="50" name="🏥 KATHGODAM RAILWAY HOSPITAL &amp; UPHC"/>

    <!-- 🏥 Rampur Road & Western Corridor Hospitals -->
    <poi id="HOSP_STH" type="hospital" color="1.0,0.0,0.0" layer="150" x="0.0" y="-200.0" width="70" height="70" name="🏥 DR. SUSHEELA TIWARI GOVT. HOSPITAL (STH) &amp; GMC (1000-Bed Trauma Hub)"/>
    <poi id="HOSP_BASE" type="hospital" color="1.0,0.2,0.2" layer="150" x="180.0" y="20.0" width="50" height="50" name="🏥 SOBAN SINGH JEENA BASE HOSPITAL (Civil Hospital)"/>

    <!-- ⚡ Gully Road Access Paths & Shortcuts -->
    <poi id="GULLY_BRIJLAL" type="gully" color="0.2,0.9,0.9" layer="140" x="15.0" y="180.0" width="25" height="25" name="⚡ Gully Road: Brijlal Hospital Direct Emergency Gali"/>
    <poi id="GULLY_KRISHNA" type="gully" color="0.2,0.9,0.9" layer="140" x="40.0" y="150.0" width="25" height="25" name="⚡ Gully Road: Krishna Hospital Emergency Access Lane"/>
    <poi id="GULLY_CANAL" type="shortcut" color="0.2,1.0,0.4" layer="140" x="80.0" y="80.0" width="30" height="30" name="⚡ SHORTCUT: Canal Nahar Road - Bypass to Krishna &amp; Brijlal"/>
    <poi id="GULLY_GASGODAM" type="shortcut" color="0.2,1.0,0.4" layer="140" x="-80.0" y="-80.0" width="30" height="30" name="⚡ SHORTCUT: Gas Godam Bypass - Direct to STH Hospital"/>
</additional>
'''
with open(NET_DIR / "haldwani_landmarks.add.xml", "w") as f:
    f.write(landmarks_xml)

# 7. Master SUMO Configuration with Sublane Physics & Hospital Landmarks
sumocfg_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <input>
        <net-file value="mukhani.net.xml"/>
        <route-files value="mukhani.rou.xml"/>
        <additional-files value="haldwani_landmarks.add.xml"/>
    </input>"""

if old_step_2_end in code:
    code = code.replace(old_step_2_end, new_step_2_end)
    print("Successfully replaced step 2 in build_colab_notebook.py")

old_html_emerg = """    <div style="background: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;">
        <b style="color: #10b981;">🚑 Emergency Preemption Interlock: ACTIVE & READY</b><br>
        <span style="font-size: 13px; color: #cbd5e1;">Detectors continuously scanning 150m upstream for ambulances heading to Sushila Tiwari Hospital. Latency: &lt;100ms.</span>
    </div>"""

new_html_emerg = """    <div style="background: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin-top: 15px;">
        <b style="color: #10b981;">🚑 Emergency Preemption Interlock: ACTIVE & READY</b><br>
        <div style="font-size: 13px; color: #cbd5e1; margin-top: 6px; line-height: 1.6;">
            • <b>Kathgodam Side Corridor:</b> 🏥 <b>Brij Lal Hospital &amp; Research Centre</b> &amp; 🏥 <b>Krishna Hospital</b> (Nainital Rd) — Green Wave active via Canal Road Gully.<br>
            • <b>Rampur Road Corridor:</b> 🏥 <b>Dr. Susheela Tiwari Govt Hospital (STH)</b> — Preempted via Gas Godam shortcut.<br>
            • <b>Preemption Latency:</b> &lt;100ms with mandatory 3s safety yellow clearance.
        </div>
    </div>"""

if old_html_emerg in code:
    code = code.replace(old_html_emerg, new_html_emerg)
    print("Successfully replaced visualizer in build_colab_notebook.py")

script_path.write_text(code, encoding="utf-8")
print("Saved updated build_colab_notebook.py")
