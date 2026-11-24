import { Award, Code2, Cpu, Database, FileCode2, Layers, ShieldCheck, UserCheck } from "lucide-react";

export interface TeamMemberProfile {
  id: string;
  name: string;
  urn: string;
  section: string;
  badge: string;
  role: string;
  accentColor: string;
  summary: string;
  ownedFiles: string[];
  contributions: string[];
  vivaFocus: Array<{ q: string; a: string }>;
}

export const TEAM_MEMBERS: TeamMemberProfile[] = [
  {
    id: "piyush",
    name: "Piyush Karnatak",
    urn: "2361393",
    section: "B",
    badge: "TEAM LEAD · DEEP RL",
    role: "Deep RL Architecture, MDP Design & Colab Pipeline",
    accentColor: "#2563EB",
    summary:
      "Designed the custom Gymnasium SUMO environment, multi-objective reward shaping, TraCI socket communication, and PPO/DQN training pipelines.",
    ownedFiles: [
      "src/environment/sumo_env.py",
      "src/agents/ppo/train_ppo.py",
      "src/agents/dqn/train_dqn.py",
      "notebooks/IntelliFlow_Google_Colab_Haldwani_PPO.ipynb",
    ],
    contributions: [
      "Formulated the 43D (Mukhani 10-lane) and 35D (Single 4-way) normalized Box observation spaces and discrete phase action wrapper.",
      "Engineered multi-objective reward shaping balancing halting queues, waiting time, HBEFA3 CO2 emissions, velocity bonus, switch penalty (1.5), starvation guard (120s), and 5.0x ambulance priority.",
      "Implemented hardware-safe phase transitions enforcing 5s minimum green floor and mandatory 3s yellow clearance intervals.",
      "Built the automated Google Colab GPU training & evaluation notebook with pretrained weight auto-detection.",
    ],
    vivaFocus: [
      {
        q: "Why PPO over DQN for adaptive signal control?",
        a: "PPO's clipped surrogate objective (ε = 0.2) with GAE bounds policy updates inside a trust region, avoiding DQN Q-value overestimation bias during sudden peak surges.",
      },
      {
        q: "How is side-street starvation prevented?",
        a: "Vehicles waiting past 120s trigger explicit starvation penalties alongside quadratic queue weighting, forcing the policy to serve minor approaches.",
      },
    ],
  },
  {
    id: "rahul",
    name: "Rahul Bhakuni",
    urn: "2361432",
    section: "B",
    badge: "SIMULATION · SUMO",
    role: "Microscopic Traffic Simulation & Haldwani Network Modeling",
    accentColor: "#10B981",
    summary:
      "Modeled the Mukhani Chauraha 10-lane arterial junction, extracted the full Haldwani OpenStreetMap network, and calibrated Indian mixed-traffic physics.",
    ownedFiles: [
      "sumo/networks/mukhani_chauraha/*",
      "sumo/networks/haldwani_full/*",
      "scripts/google_maps_24h_traffic.py",
      "scripts/build_real_haldwani_osm.py",
    ],
    contributions: [
      "Compiled Mukhani Chauraha (.nod.xml, .edg.xml, .tll.xml) with 3-lane Kaladhungi approaches, 2-lane Canal/Rampur approaches, and turn bays.",
      "Calibrated Krauss car-following & 0.8m sublane filtering dynamics for Indian mixed traffic (40% 2W, 30% Auto, 22% Car, 8% Bus + Emergency Ambulance).",
      "Extracted the 37,000+ street Haldwani OSM network (Kathgodam to Motahaldu) plus 8 signalized junctions, 5 strategic bypass shortcuts, and 8 trauma hospital hubs.",
      "Built the 24-hour Google Maps probe congestion generator using inverse BPR capacity-delay formulation (216–2,700 veh/hr).",
    ],
    vivaFocus: [
      {
        q: "Why enable SUMO's sublane lateral resolution?",
        a: "Indian two-wheelers and auto-rickshaws filter laterally between stationary cars rather than obeying strict 1D lanes; 0.8m sublane modeling reproduces real stop-line creep.",
      },
      {
        q: "How were Morning and Evening peaks calibrated?",
        a: "Inverse BPR equations convert Google Maps delay ratios (2.95x morning inbound, 3.15x evening outbound) into directional hourly SUMO vehicle flows.",
      },
    ],
  },
  {
    id: "vishal",
    name: "Vishal Joshi",
    urn: "2361588",
    section: "B",
    badge: "EVALUATION · STATS",
    role: "Empirical Evaluation, Baselines & Statistical Rigor",
    accentColor: "#06B6D4",
    summary:
      "Implemented classical traffic control baselines, ran paired multi-controller benchmarks, and proved RL significance via non-parametric and parametric hypothesis tests.",
    ownedFiles: [
      "src/baselines/fixed_time.py",
      "src/baselines/actuated.py",
      "src/evaluation/evaluate.py",
      "results/metrics/*",
    ],
    contributions: [
      "Implemented Webster's Optimal Fixed-Time controller (81s Mukhani cycle: 45s EW / 3s Y / 30s NS / 3s Y) and Inductive Loop Gap-Out Actuated baseline.",
      "Diagnosed why Sensor-Actuated control performed 23.9% worse than Fixed-Time (9.67 vs. 7.80 mean queue) due to sublane two-wheeler detector tripping.",
      "Executed Mann-Whitney U (U = 822.5, p = 5.78e-21) and Welch's two-sample t-test (t = -7.14, p = 7.27e-08) confirming -95.9% queue reduction and +16.1% speed gain.",
      "Quantified HBEFA3 CO2 reductions (16.34 kg/hr benchmark) and projected ₹2.48+ Crore annual commuter idling fuel savings for Haldwani corridors.",
    ],
    vivaFocus: [
      {
        q: "Why use Mann-Whitney U instead of only a Student's t-test?",
        a: "Traffic queue lengths are heavily right-skewed and non-Gaussian; Mann-Whitney U validates rank-order superiority without normality assumptions, backed by Welch's t-test.",
      },
      {
        q: "Why did Sensor-Actuated fail in mixed Indian traffic?",
        a: "Continuous motorcycle filtering keeps tripping inductive loops inside the 3s passage gap, locking phases up to max green and causing upstream spillback.",
      },
    ],
  },
  {
    id: "lalit",
    name: "Lalit Joshi",
    urn: "2361296",
    section: "F",
    badge: "SYSTEMS · UI & ROADMAP",
    role: "Full-Stack Operations UI, Testing & Phase 2 Vision Bridge",
    accentColor: "#F59E0B",
    summary:
      "Built the interactive React & Streamlit operations dashboards, one-click Windows automation, automated pytest verification suite, and Phase 2 edge vision prototype.",
    ownedFiles: [
      "frontend/src/*",
      "src/dashboard/*",
      "scripts/demo.py",
      "tests/test_*.py",
      "run.bat / stop.bat",
      "scripts/yolo_traffic_detector.py",
    ],
    contributions: [
      "Built the React 19 + TypeScript Operations Console featuring the 60fps Split-Screen AI vs. Legacy Duel, Haldwani live traffic flow map, Light/Dark themes, and 5-Axis Radar.",
      "Architected the modular 5-tab Streamlit TOC Dashboard (styles, data_loader, components, charts, app) wired into run.bat Option 10.",
      "Authored the 4/4 automated pytest compliance suite validating Gymnasium spaces, Mukhani 10-lane geometry, and full Haldwani network loading.",
      "Engineered the Phase 2 Edge YOLOv8 camera-to-PCU bridge prototype (deferred for physical CCTV deployment) and clean Windows process lifecycle scripts (run.bat / stop.bat).",
    ],
    vivaFocus: [
      {
        q: "How do run.bat and stop.bat prevent orphaned SUMO ports?",
        a: "sumo_env.py requests free ephemeral ports dynamically and stop.bat cleans lingering sumo.exe / sumo-gui.exe processes safely.",
      },
      {
        q: "How is Edge YOLO integrated without blocking Phase 1?",
        a: "Phase 1 runs deterministically over SUMO/TraCI telemetry; yolo_traffic_detector.py implements the PCU-weighted camera-to-43D-vector adapter ready for Phase 2 Jetson deployment.",
      },
    ],
  },
];

export function TeamContributionsPage() {
  const icons = [Cpu, Database, ShieldCheck, Layers];

  return (
    <section className="space-y-4">
      {/* Team Header Banner */}
      <div className="rounded-md border border-border bg-card p-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 font-mono text-[10.5px] font-semibold uppercase tracking-wider text-cyan-700 dark:text-cyan-400">
              <UserCheck className="h-3.5 w-3.5" />
              Team #54 · CSP-701 / MPP-I Major Project (2026&ndash;27)
            </div>
            <h1 className="mt-1 text-lg font-bold tracking-tight text-foreground">
              Individual Member Contributions & Owned Subsystems
            </h1>
            <p className="mt-0.5 text-xs text-muted-foreground">
              B.Tech Computer Science & Engineering (AI & ML) · Verified subsystem ownership across RL, SUMO Simulation, Statistical Evaluation, and UI/Tooling.
            </p>
          </div>

          <div className="flex flex-wrap gap-2 font-mono text-[10.5px]">
            <span className="rounded border border-emerald-500/40 bg-emerald-500/10 px-2.5 py-1 font-semibold text-emerald-700 dark:text-emerald-400">
              4/4 PYTEST PASSING
            </span>
            <span className="rounded border border-blue-500/40 bg-blue-500/10 px-2.5 py-1 font-semibold text-blue-700 dark:text-blue-400">
              4 CORE SUBSYSTEMS
            </span>
          </div>
        </div>
      </div>

      {/* 4 Member Cards */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {TEAM_MEMBERS.map((m, idx) => {
          const Icon = icons[idx % icons.length];
          return (
            <article
              key={m.id}
              className="flex flex-col justify-between rounded-md border border-border bg-card p-4"
              style={{ borderTopWidth: 3, borderTopColor: m.accentColor }}
            >
              <div className="space-y-3">
                {/* Identity Header */}
                <div className="flex flex-wrap items-start justify-between gap-2 border-b border-border pb-3">
                  <div className="flex items-start gap-2.5">
                    <div
                      className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-border bg-background"
                      style={{ color: m.accentColor }}
                    >
                      <Icon className="h-4.5 w-4.5" />
                    </div>
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <h2 className="text-sm font-bold text-foreground">
                          {m.name}
                        </h2>
                        <span className="rounded bg-secondary px-1.5 py-0.5 font-mono text-[10px] font-semibold text-muted-foreground">
                          URN {m.urn} · SEC {m.section}
                        </span>
                      </div>
                      <div className="mt-0.5 text-xs font-medium text-foreground/90">
                        {m.role}
                      </div>
                    </div>
                  </div>

                  <span
                    className="rounded border px-2 py-0.5 font-mono text-[9.5px] font-semibold"
                    style={{
                      borderColor: `${m.accentColor}55`,
                      backgroundColor: `${m.accentColor}15`,
                      color: m.accentColor,
                    }}
                  >
                    {m.badge}
                  </span>
                </div>

                {/* Summary */}
                <p className="text-xs leading-relaxed text-muted-foreground">
                  {m.summary}
                </p>

                {/* Contributions List */}
                <div>
                  <div className="mb-1.5 flex items-center gap-1.5 font-mono text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                    <Award className="h-3 w-3" /> Key Deliverables
                  </div>
                  <ul className="space-y-1.5 text-xs leading-relaxed text-foreground/90">
                    {m.contributions.map((c, i) => (
                      <li key={i} className="flex gap-2">
                        <span
                          className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full"
                          style={{ backgroundColor: m.accentColor }}
                        />
                        <span>{c}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Owned Modules */}
                <div>
                  <div className="mb-1.5 flex items-center gap-1.5 font-mono text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                    <FileCode2 className="h-3 w-3" /> Owned Modules & Files
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {m.ownedFiles.map((f) => (
                      <code
                        key={f}
                        className="rounded border border-border bg-background px-2 py-0.5 font-mono text-[10.5px] text-cyan-700 dark:text-cyan-400"
                      >
                        {f}
                      </code>
                    ))}
                  </div>
                </div>
              </div>

              {/* Viva Defense Q&A Snippets */}
              <div className="mt-4 space-y-2 border-t border-border pt-3">
                <div className="flex items-center gap-1.5 font-mono text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                  <Code2 className="h-3 w-3" /> Examiner Viva Defense Focus
                </div>
                {m.vivaFocus.map((qa, i) => (
                  <div
                    key={i}
                    className="rounded border border-border bg-background p-2.5 text-xs"
                  >
                    <div className="font-semibold text-foreground">{qa.q}</div>
                    <div className="mt-1 leading-relaxed text-muted-foreground">
                      {qa.a}
                    </div>
                  </div>
                ))}
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
