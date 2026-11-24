import type {
  ApproachTelemetry,
  ControllerId,
  JunctionFrameState,
  NetworkId,
  SignalState,
  TelemetryStep,
} from "@/types/telemetry";

export function deriveJunctionFrameState(
  row: TelemetryStep,
  controller: ControllerId,
  network: NetworkId,
  preemption: boolean,
  direction: "inbound" | "outbound" | "balanced" = "balanced",
): JunctionFrameState {
  const simStep = row.step;
  const speedKmh = Number((row.mean_speed * 3.6).toFixed(1));
  const totalQueue = row.halting_vehicles;

  let ewSignal: SignalState = "GREEN";
  let nsSignal: SignalState = "RED";
  let phaseLabel =
    network === "single"
      ? "PHASE 0 · EW BENCHMARK"
      : "PHASE 0 · EW KALADHUNGI";
  let dwellSec = 14;

  if (preemption && (controller === "ppo" || controller === "dqn")) {
    ewSignal = "GREEN";
    nsSignal = "RED";
    phaseLabel = "STH GREEN WAVE LOCK";
    dwellSec = 12;
  } else if (controller === "fixed") {
    const c = simStep % 81;
    if (c < 45) {
      ewSignal = "GREEN";
      nsSignal = "RED";
      phaseLabel = "STATIC EW (45s)";
      dwellSec = Math.max(1, c);
    } else if (c < 48) {
      ewSignal = "AMBER";
      nsSignal = "RED";
      phaseLabel = "EW YELLOW (3s)";
      dwellSec = c - 44;
    } else {
      ewSignal = "RED";
      nsSignal = "GREEN";
      phaseLabel = "STATIC NS (30s)";
      dwellSec = Math.max(1, c - 47);
    }
  } else if (controller === "actuated") {
    const c = simStep % 60;
    if (c < 35) {
      ewSignal = "GREEN";
      nsSignal = "RED";
      phaseLabel = "GAP-OUT EW";
      dwellSec = Math.max(1, c);
    } else {
      ewSignal = "RED";
      nsSignal = "GREEN";
      phaseLabel = "GAP-OUT NS";
      dwellSec = Math.max(1, c - 34);
    }
  } else {
    const c = simStep % 40;
    if (c < 22) {
      ewSignal = "GREEN";
      nsSignal = "RED";
      phaseLabel = "RL ADAPTIVE EW";
      dwellSec = Math.max(5, c);
    } else if (c < 25) {
      ewSignal = "AMBER";
      nsSignal = "RED";
      phaseLabel = "3s CLEARANCE";
      dwellSec = c - 21;
    } else {
      ewSignal = "RED";
      nsSignal = "GREEN";
      phaseLabel = "RL ADAPTIVE NS";
      dwellSec = Math.max(5, c - 24);
    }
  }

  const ewWeight = ewSignal === "GREEN" ? 0.55 : 1.45;
  const nsWeight = nsSignal === "GREEN" ? 0.55 : 1.45;
  const ewLanes = network === "single" ? 2 : 3;

  const shares =
    network === "single"
      ? { KW2M: 0.25, KE2M: 0.25, CN2M: 0.25, CS2M: 0.25 }
      : direction === "inbound"
        ? { KW2M: 0.4, KE2M: 0.16, CN2M: 0.3, CS2M: 0.14 }
        : direction === "outbound"
          ? { KW2M: 0.22, KE2M: 0.36, CN2M: 0.14, CS2M: 0.28 }
          : { KW2M: 0.35, KE2M: 0.35, CN2M: 0.15, CS2M: 0.15 };

  const weightSum =
    (shares.KW2M + shares.KE2M) * ewWeight +
    (shares.CN2M + shares.CS2M) * nsWeight;

  const specs: Array<{
    id: ApproachTelemetry["id"];
    name: string;
    lanes: number;
    signal: SignalState;
    share: number;
    weight: number;
  }> = [
    {
      id: "KW2M",
      name: network === "single" ? "West (W2C)" : "Kaladhungi W",
      lanes: ewLanes,
      signal: ewSignal,
      share: shares.KW2M,
      weight: ewWeight,
    },
    {
      id: "KE2M",
      name: network === "single" ? "East (E2C)" : "Kaladhungi E",
      lanes: ewLanes,
      signal: ewSignal,
      share: shares.KE2M,
      weight: ewWeight,
    },
    {
      id: "CN2M",
      name: network === "single" ? "North (N2C)" : "Canal Rd N",
      lanes: 2,
      signal: nsSignal,
      share: shares.CN2M,
      weight: nsWeight,
    },
    {
      id: "CS2M",
      name: network === "single" ? "South (S2C)" : "Rampur Rd S",
      lanes: 2,
      signal: nsSignal,
      share: shares.CS2M,
      weight: nsWeight,
    },
  ];

  const approaches: ApproachTelemetry[] = specs.map((spec) => {
    const rawQueue =
      preemption && (controller === "ppo" || controller === "dqn") && spec.id === "KW2M"
        ? Math.min(0.4, (totalQueue * spec.share * spec.weight) / weightSum)
        : (totalQueue * spec.share * spec.weight) / weightSum;
    const queue = Number(rawQueue.toFixed(1));
    const saturationPct = Math.min(
      100,
      Math.round((queue / (spec.lanes * 6)) * 100),
    );
    return {
      id: spec.id,
      name: spec.name,
      lanes: spec.lanes,
      signal: spec.signal,
      queue,
      saturationPct,
    };
  });

  return {
    simStep,
    totalQueue,
    speedKmh,
    ewSignal,
    nsSignal,
    phaseLabel,
    dwellSec,
    approaches,
  };
}

export function computeGreenAiSavings(
  dailyVehicles: number,
  fuelPriceInr: number,
  idleSavedSec: number,
) {
  const litersSavedPerDay = dailyVehicles * (idleSavedSec / 3600) * 0.85;
  const annualSavingsCr = (litersSavedPerDay * fuelPriceInr * 365) / 1e7;
  const annualCo2Tonnes = (litersSavedPerDay * 2.31 * 365) / 1000;
  return {
    litersSavedPerDay,
    annualSavingsCr,
    annualCo2Tonnes,
  };
}
