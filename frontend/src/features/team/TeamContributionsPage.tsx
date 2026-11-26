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
    badge: "TEAM LEAD · DL & RL",
    role: "Deep Learning & Reinforcement Learning (DL/RL) Architecture Lead",
    accentColor: "#2563EB",
    summary:
      "Owned the entire Deep Learning & Reinforcement Learning pipeline: custom Gymnasium MDP wrapper, multi-objective reward shaping, PPO (100k-step Colab policy), and Double DQN agents.",
    ownedFiles: [
      "src/environment/sumo_env.py",
      "src/agents/ppo/train_ppo.py",
      "src/agents/dqn/train_dqn.py",
      "notebooks/IntelliFlow_Google_Colab_Haldwani_PPO.ipynb",
      "results/models/*",
    ],
    contributions: [
      "Formulated the 43D (Mukhani 10-lane) and 35D (Single 4-way) normalized Box observation spaces and discrete phase action wrapper.",
      "Engineered multi-objective reward shaping balancing halting queues, waiting time, HBEFA3 CO2 emissions, velocity bonus, switch penalty (1.5), starvation guard (120s), and 5.0x ambulance priority.",
      "Implemented hardware-safe phase transitions enforcing 5s minimum green floor and mandatory 3s yellow clearance intervals.",
      "Built and executed the Google Colab cloud training notebook producing the converged 100,096-step PPO policy alongside the Double DQN baseline.",
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
    role: "SUMO Microscopic Traffic Simulation & Network Modeling Lead",
    accentColor: "#10B981",
    summary:
      "Owned the entire Eclipse SUMO simulation layer: Mukhani Chauraha 10-lane junction, 37,000+ street Haldwani OSM extraction, Indian mixed-traffic sublane physics, and classical SUMO baselines.",
    ownedFiles: [
      "sumo/networks/mukhani_chauraha/*",
      "sumo/networks/haldwani_full/*",
      "sumo/networks/single_intersection/*",
      "scripts/google_maps_24h_traffic.py",
      "scripts/build_real_haldwani_osm.py",
      "src/baselines/fixed_time.py / actuated.py",
    ],
    contributions: [
      "Compiled Mukhani Chauraha (.nod.xml, .edg.xml, .tll.xml) with 3-lane Kaladhungi approaches, 2-lane Canal/Rampur approaches, and turn bays.",
      "Calibrated Krauss car-following & 0.8m sublane filtering dynamics for Indian mixed traffic (40% 2W, 30% Auto, 22% Car, 8% Bus + Emergency Ambulance).",
      "Extracted the 37,000+ street Haldwani OSM network (Kathgodam to Motahaldu) plus 8 signalized junctions, 5 strategic bypass shortcuts, and 8 trauma hospital hubs.",
      "Built the 24-hour Google Maps probe congestion generator (inverse BPR) and implemented Webster Fixed-Time & Inductive Loop Actuated SUMO baselines.",
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
    badge: "VISION · YOLOV8 & EVAL",
    role: "Computer Vision (YOLOv8) & Empirical Evaluation Lead",
    accentColor: "#06B6D4",
    summary:
      "Owned the entire YOLOv8 computer vision detection pipeline for traffic state estimation alongside multi-controller statistical hypothesis testing and Green AI fuel impact modeling.",
    ownedFiles: [
      "scripts/yolo_traffic_detector.py",
      "src/evaluation/evaluate.py",
      "results/metrics/*",
      "results/plots/*",
    ],
    contributions: [
      "Engineered the end-to-end YOLOv8 computer vision detector transforming CCTV streams into multi-class bounding boxes (two-wheelers, Vikram autos, cars, buses, and ambulances).",
      "Implemented virtual 150m stop-line approach polygons and Indian PCU weighting (0.5 / 0.8 / 1.0 / 3.0) to construct live traffic state vectors ready for edge Jetson deployment.",
      "Executed Mann-Whitney U (U = 822.5, p = 5.78e-21) and Welch's two-sample t-test (t = -7.14, p = 7.27e-08) confirming -95.9% queue reduction and +16.1% speed gain.",
      "Quantified HBEFA3 CO2 reductions (16.34 kg/hr benchmark) and projected ₹2.48+ Crore annual commuter idling fuel savings for Haldwani corridors.",
    ],
    vivaFocus: [
      {
        q: "How does the YOLOv8 module handle Indian mixed traffic?",
        a: "YOLOv8 detects heterogeneous classes inside virtual approach polygons and scales counts by Indian PCU weights (0.5 for bikes, 0.8 for autos, 3.0 for buses) instead of naive raw counts.",
      },
      {
        q: "Why use Mann-Whitney U instead of only a Student's t-test?",
        a: "Traffic queue lengths are heavily right-skewed and non-Gaussian; Mann-Whitney U validates rank-order superiority without normality assumptions, backed by Welch's t-test.",
      },
    ],
  },
  {
    id: "lalit",
    name: "Lalit Joshi",
    urn: "2361296",
    section: "F",
    badge: "BRIDGE · TESTS & RUN.BAT",
    role: "Bridge Engineer, Automated Testing (tests/*.py) & Lifecycle Tooling (run.bat)",
    accentColor: "#F59E0B",
    summary:
      "Served as Bridge Engineer connecting SUMO, YOLO, and RL modules into a unified runtime, authored all pytest test files (tests/test_*.py), and built the run.bat / stop.bat automation and Operations UI.",
    ownedFiles: [
      "tests/test_sumo_env.py",
      "tests/test_mukhani_env.py",
      "tests/test_haldwani_env.py",
      "run.bat / stop.bat",
      "scripts/demo.py",
      "src/utils/sumo_utils.py",
      "frontend/src/*",
    ],
    contributions: [
      "Acted as Bridge Engineer authoring the TraCI runtime & utility bridge (scripts/demo.py, sumo_utils.py) linking Rahul's SUMO networks, Vishal's YOLO state estimation, and Piyush's PPO/DQN checkpoints.",
      "Created the complete automated pytest suite (test_sumo_env.py, test_mukhani_env.py, test_haldwani_env.py) passing 4/4 checks on Gymnasium spaces, bounds [0,1], Mukhani 10-lane, and Haldwani networks.",
      "Engineered the 12-option Windows master command launcher (run.bat) and cleanup script (stop.bat) orchestrating SUMO-GUI, live AI demos, YOLO detector, React UI, and pytest checks.",
      "Co-built and wired the React 19 + TypeScript Operations Console uniting telemetry CSVs, Split-Screen AI vs. Legacy Duel, and Haldwani interactive maps.",
    ],
    vivaFocus: [
      {
        q: "What does your pytest suite in tests/ verify?",
        a: "The 3 test files (test_sumo_env.py, test_mukhani_env.py, test_haldwani_env.py) enforce 4/4 checks on SB3/Gymnasium API compliance, [0, 1] observation bounds, and network asset loading.",
      },
      {
        q: "How do run.bat and stop.bat bridge the system cleanly?",
        a: "run.bat automates venv Python routing, TraCI live demos, YOLO estimation, and the Vite React UI, while stop.bat kills lingering sumo.exe/Node processes to prevent Windows port locks.",
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
              B.Tech Computer Science & Engineering (AI & ML) · Verified ownership across Deep RL (DL/RL), SUMO Simulation, YOLOv8 Vision & Evaluation, and Bridge/Tests/Tooling.
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
