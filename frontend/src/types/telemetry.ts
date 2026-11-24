export type ControllerId = "ppo" | "dqn" | "fixed" | "actuated";

export type BaselineId = "fixed" | "actuated";

export type NetworkId = "mukhani" | "haldwani" | "single";

export type ModelCheckpointId =
  | "ppo_mukhani"
  | "ppo_colab"
  | "ppo_single"
  | "dqn_final"
  | "fixed"
  | "actuated";

export type ThemeMode = "dark" | "light";

export type SignalState = "GREEN" | "AMBER" | "RED";

export interface TelemetryStep {
  step: number;
  halting_vehicles: number;
  mean_speed: number;
  waiting_time?: number;
  co2_emissions?: number;
}

export interface HaldwaniNode {
  id: string;
  x: number;
  y: number;
  type: "traffic_light" | "priority";
}

export interface HaldwaniEdge {
  id: string;
  from: string;
  to: string;
  category: "kaladhungi" | "nainital" | "rampur" | "shortcut" | "gully";
  lanes: number;
  speed_kmh: number;
}

export interface LandmarkPOI {
  id: string;
  type: "hospital" | "shortcut";
  name: string;
  x: number;
  y: number;
}

export interface DiurnalHourSpec {
  hour: number;
  timeLabel: string;
  delayRatio: number;
  direction: "inbound" | "outbound" | "balanced";
  flowVph: number;
  description: string;
}

export interface ControllerBenchmark {
  id: ControllerId;
  label: string;
  meanQueue: number;
  stdQueue: number;
  maxQueue: number;
  speedKmh: number;
  deltaVsFixed: string;
  pValue: string;
  accentClass: string;
}

export interface NetworkProfile {
  id: NetworkId;
  name: string;
  shortName: string;
  tlsId: string;
  obsDim: string;
  inboundLanes: number;
  description: string;
  configPath: string;
}

export interface ModelCheckpoint {
  id: ModelCheckpointId;
  label: string;
  shortLabel: string;
  controllerId: ControllerId;
  artifactPath: string;
  algorithm: string;
}

export interface ApproachTelemetry {
  id: "KW2M" | "KE2M" | "CN2M" | "CS2M";
  name: string;
  lanes: number;
  signal: SignalState;
  queue: number;
  saturationPct: number;
}

export interface JunctionFrameState {
  simStep: number;
  totalQueue: number;
  speedKmh: number;
  ewSignal: SignalState;
  nsSignal: SignalState;
  phaseLabel: string;
  dwellSec: number;
  approaches: ApproachTelemetry[];
}
