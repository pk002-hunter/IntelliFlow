import rawTelemetry from "./telemetry.json";
import type {
  ControllerBenchmark,
  ControllerId,
  DiurnalHourSpec,
  HaldwaniEdge,
  HaldwaniNode,
  LandmarkPOI,
  ModelCheckpoint,
  ModelCheckpointId,
  NetworkId,
  NetworkProfile,
  TelemetryStep,
} from "@/types/telemetry";

export const NETWORK_PROFILES: Record<NetworkId, NetworkProfile> = {
  mukhani: {
    id: "mukhani",
    name: "Mukhani Chauraha (10-Lane)",
    shortName: "Mukhani 10L",
    tlsId: "Mukhani",
    obsDim: "43D Box",
    inboundLanes: 10,
    description: "Kaladhungi Rd (SH-41) × Canal/Rampur Rd · Sublane 0.8m",
    configPath: "sumo/networks/mukhani_chauraha/mukhani.sumocfg",
  },
  haldwani: {
    id: "haldwani",
    name: "Full Haldwani City Network",
    shortName: "Haldwani City",
    tlsId: "8 Signalized Junctions",
    obsDim: "43D Arterial",
    inboundLanes: 10,
    description: "Kathgodam to Motahaldu · 8 TLS Nodes · 8 Hospital Hubs",
    configPath: "sumo/networks/haldwani_full/haldwani.sumocfg",
  },
  single: {
    id: "single",
    name: "Single 4-Way Benchmark",
    shortName: "Single 4-Way",
    tlsId: "C",
    obsDim: "35D Box",
    inboundLanes: 8,
    description: "Synthetic 4-Way Junction (2L × 4 Approaches)",
    configPath: "sumo/networks/single_intersection/single_intersection.sumocfg",
  },
};

export const MODEL_CHECKPOINTS: Record<ModelCheckpointId, ModelCheckpoint> = {
  ppo_mukhani: {
    id: "ppo_mukhani",
    label: "PPO · Mukhani Final (ppo_final.zip)",
    shortLabel: "PPO Mukhani",
    controllerId: "ppo",
    artifactPath: "results/models/ppo/mukhani/ppo_final.zip",
    algorithm: "PPO Clipped Surrogate (ε=0.2, GAE)",
  },
  ppo_colab: {
    id: "ppo_colab",
    label: "PPO · Haldwani Colab (intelliflow_ppo_colab.zip)",
    shortLabel: "PPO Colab",
    controllerId: "ppo",
    artifactPath: "results/models/ppo/intelliflow_ppo_colab.zip",
    algorithm: "PPO Multi-Scenario Policy",
  },
  ppo_single: {
    id: "ppo_single",
    label: "PPO · Single Benchmark (ppo_final.zip)",
    shortLabel: "PPO Benchmark",
    controllerId: "ppo",
    artifactPath: "results/models/ppo/ppo_final.zip",
    algorithm: "PPO Clipped Surrogate (35D)",
  },
  dqn_final: {
    id: "dqn_final",
    label: "Double DQN · Final (dqn_final.zip)",
    shortLabel: "Double DQN",
    controllerId: "dqn",
    artifactPath: "results/models/dqn/dqn_final.zip",
    algorithm: "Double DQN + Target Network + Huber",
  },
  fixed: {
    id: "fixed",
    label: "Webster Fixed-Time Controller",
    shortLabel: "Webster Fixed",
    controllerId: "fixed",
    artifactPath: "src/baselines/fixed_time.py",
    algorithm: "Static 81s Cycle (45s EW / 30s NS / 3s Yellow)",
  },
  actuated: {
    id: "actuated",
    label: "Sensor-Actuated Gap-Out",
    shortLabel: "Sensor-Actuated",
    controllerId: "actuated",
    artifactPath: "src/baselines/actuated.py",
    algorithm: "Inductive Loop (10s Min / 50s Max Green)",
  },
};

export const CONTROLLER_BENCHMARKS: Record<ControllerId, ControllerBenchmark> = {
  ppo: {
    id: "ppo",
    label: "PPO Agent",
    meanQueue: 0.32,
    stdQueue: 0.55,
    maxQueue: 2,
    speedKmh: 42.88,
    deltaVsFixed: "-95.9% vs Fixed",
    pValue: "p = 5.78e-21",
    accentClass: "text-emerald-600 dark:text-emerald-400",
  },
  dqn: {
    id: "dqn",
    label: "Double DQN",
    meanQueue: 0.32,
    stdQueue: 0.55,
    maxQueue: 2,
    speedKmh: 42.88,
    deltaVsFixed: "-95.9% vs Fixed",
    pValue: "p = 5.78e-21",
    accentClass: "text-blue-600 dark:text-blue-400",
  },
  fixed: {
    id: "fixed",
    label: "Webster Fixed-Time",
    meanQueue: 7.8,
    stdQueue: 5.73,
    maxQueue: 20,
    speedKmh: 36.92,
    deltaVsFixed: "Baseline (0.0%)",
    pValue: "Reference",
    accentClass: "text-amber-600 dark:text-amber-400",
  },
  actuated: {
    id: "actuated",
    label: "Sensor-Actuated",
    meanQueue: 9.67,
    stdQueue: 7.42,
    maxQueue: 29,
    speedKmh: 36.33,
    deltaVsFixed: "+23.9% worse",
    pValue: "N.S. (loop chatter)",
    accentClass: "text-red-600 dark:text-red-400",
  },
};

export const TELEMETRY_SERIES = {
  mukhani_ppo: rawTelemetry.mukhani_ppo as TelemetryStep[],
  bench_ppo: rawTelemetry.bench_ppo as TelemetryStep[],
  bench_dqn: rawTelemetry.bench_dqn as TelemetryStep[],
  fixed: rawTelemetry.fixed as TelemetryStep[],
  actuated: rawTelemetry.actuated as TelemetryStep[],
};

export const HALDWANI_TOPOLOGY = {
  nodes: rawTelemetry.haldwani.nodes as HaldwaniNode[],
  edges: rawTelemetry.haldwani.edges as HaldwaniEdge[],
  landmarks: rawTelemetry.haldwani.landmarks as LandmarkPOI[],
};

export const EMERGENCY_CORRIDORS: Record<
  string,
  { label: string; routeNodes: string[]; distanceLabel: string; targetHospital: string }
> = {
  sth_rampur: {
    label: "Kaladhungi (W) → Mukhani → STH Hospital (Rampur SH-49)",
    routeNodes: [
      "KW_Out",
      "Kusumkhera",
      "Unchapul_Jct",
      "Mukhani",
      "ChhotiMukhani",
      "Mandi_Chauraha",
      "TransportNagar",
      "STH_Hospital_Jct",
      "STH_Gully_End",
    ],
    distanceLabel: "4.05 km · 4 Signalized Intersections",
    targetHospital: "HOSP_STH",
  },
  sth_gasgodam: {
    label: "Kusumkhera → Gas Godam Bypass → STH Hospital",
    routeNodes: [
      "KW_Out",
      "Kusumkhera",
      "GasGodam_Mid",
      "STH_Hospital_Jct",
      "STH_Gully_End",
    ],
    distanceLabel: "3.35 km · Bypasses Mukhani Grid",
    targetHospital: "HOSP_STH",
  },
  base_nh109: {
    label: "Kathgodam → Brijlal → Krishna → Tikonia → Base Hospital",
    routeNodes: [
      "Kathgodam_Out",
      "KathgodamHospital_Jct",
      "BrijlalHospital_Jct",
      "Sheeshmahal",
      "KrishnaHospital_Jct",
      "JudgeFarm",
      "Tikonia",
      "BaseHospital_Jct",
    ],
    distanceLabel: "2.80 km · NH-109 Hospital Spine",
    targetHospital: "HOSP_BASE",
  },
};

function bprDelayToFlow(delayRatio: number): number {
  const capacity = 1800;
  if (delayRatio <= 1.0) return Math.round(capacity * 0.12);
  const over = Math.max(0, (delayRatio - 1.0) / 0.15);
  const flow = capacity * Math.pow(over, 0.25);
  return Math.round(Math.min(2700, Math.max(150, flow)));
}

const RAW_HOURLY_BPR: Array<
  [number, number, "inbound" | "outbound" | "balanced", string]
> = [
  [0, 1.0, "balanced", "Midnight Lull: Bareilly Freight Corridor"],
  [1, 1.0, "balanced", "Night Quiet: Intercity Highway Transit"],
  [2, 1.0, "balanced", "Night Freight Transfer to Transport Nagar"],
  [3, 1.0, "balanced", "Early Agricultural Supply to Mandi"],
  [4, 1.05, "balanced", "Pre-Dawn Milk & Produce Supply Pickups"],
  [5, 1.1, "balanced", "Kathgodam Morning Railway Arrivals"],
  [6, 1.2, "inbound", "Early Commute & School Bus Departures"],
  [7, 1.45, "inbound", "Morning Rush Buildup: Kusumkhera to Center"],
  [8, 2.65, "inbound", "Morning Peak: Office & College Inbound Surge"],
  [9, 2.95, "inbound", "Morning Peak Max: Nainital & Kaladhungi Inbound"],
  [10, 2.3, "inbound", "Late Morning Administrative Inflow"],
  [11, 1.5, "balanced", "Midday Commercial & Banking Transit"],
  [12, 1.4, "balanced", "Afternoon Local Commercial Transit"],
  [13, 1.3, "balanced", "Midday Lull: Moderate Mixed Flow"],
  [14, 1.45, "outbound", "School Dismissal Peak: Buses & Autos"],
  [15, 1.35, "balanced", "Afternoon Inter-City Transit to Kathgodam"],
  [16, 1.7, "outbound", "Early Evening Outbound Dispersal"],
  [17, 2.4, "outbound", "Evening Peak Buildup: Commercial Exits"],
  [18, 3.15, "outbound", "Evening Peak Max: Chauraha Outbound Surge"],
  [19, 3.1, "outbound", "Evening Peak: Suburb Dispersal & Canal Rd"],
  [20, 2.2, "outbound", "Market Closing & Evening Retail Traffic"],
  [21, 1.6, "balanced", "Late Evening Retail & Freight Entry"],
  [22, 1.25, "balanced", "Night Long-Distance Bus Departures"],
  [23, 1.1, "balanced", "Late Night Highway Easing"],
];

export const DIURNAL_BPR_HOURS: DiurnalHourSpec[] = RAW_HOURLY_BPR.map(
  ([hour, delayRatio, direction, description]) => ({
    hour,
    timeLabel: `${String(hour).padStart(2, "0")}:00`,
    delayRatio,
    direction,
    flowVph: bprDelayToFlow(delayRatio),
    description,
  }),
);

export const FLEET_COMPOSITION = [
  { id: "2w", label: "Two-Wheelers", sharePct: 40, pcu: 0.5, color: "#10B981" },
  { id: "auto", label: "Auto-Rickshaws", sharePct: 30, pcu: 0.8, color: "#F59E0B" },
  { id: "car", label: "Passenger Cars", sharePct: 22, pcu: 1.0, color: "#3B82F6" },
  { id: "bus", label: "Buses & Freight", sharePct: 8, pcu: 3.0, color: "#8B5CF6" },
] as const;
