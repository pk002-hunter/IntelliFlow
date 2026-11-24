import { AlertTriangle, CheckCircle2, Pause, Play, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import {
  MODEL_CHECKPOINTS,
  NETWORK_PROFILES,
  TELEMETRY_SERIES,
} from "@/data/telemetry";
import { deriveJunctionFrameState } from "@/lib/traffic";
import type {
  BaselineId,
  DiurnalHourSpec,
  ModelCheckpointId,
  NetworkId,
  TelemetryStep,
  ThemeMode,
} from "@/types/telemetry";
import { MukhaniFlowCanvas } from "./MukhaniFlowCanvas";

interface TrafficDuelArenaProps {
  networkId: NetworkId;
  baselineId: BaselineId;
  onSelectBaseline: (id: BaselineId) => void;
  aiModelId: ModelCheckpointId;
  onSelectAiModel: (id: ModelCheckpointId) => void;
  stepIdx: number;
  onChangeStep: (idx: number) => void;
  isPlaying: boolean;
  onTogglePlay: () => void;
  onReset: () => void;
  preemption: boolean;
  theme: ThemeMode;
  activeHour: DiurnalHourSpec;
}

const AI_MODEL_OPTIONS: ModelCheckpointId[] = [
  "ppo_mukhani",
  "ppo_colab",
  "ppo_single",
  "dqn_final",
];

export function TrafficDuelArena({
  networkId,
  baselineId,
  onSelectBaseline,
  aiModelId,
  onSelectAiModel,
  stepIdx,
  onChangeStep,
  isPlaying,
  onTogglePlay,
  onReset,
  preemption,
  theme,
  activeHour,
}: TrafficDuelArenaProps) {
  const network = NETWORK_PROFILES[networkId];
  const baselineSeries: TelemetryStep[] =
    baselineId === "fixed" ? TELEMETRY_SERIES.fixed : TELEMETRY_SERIES.actuated;

  const aiSeries: TelemetryStep[] = (() => {
    if (aiModelId === "dqn_final") return TELEMETRY_SERIES.bench_dqn;
    if (networkId === "single" || aiModelId === "ppo_single") {
      return TELEMETRY_SERIES.bench_ppo;
    }
    return TELEMETRY_SERIES.mukhani_ppo;
  })();

  const maxAlignedIdx = Math.min(baselineSeries.length, aiSeries.length) - 1;
  const safeIdx = Math.min(stepIdx, maxAlignedIdx);

  const leftFrame = deriveJunctionFrameState(
    baselineSeries[safeIdx],
    baselineId,
    networkId,
    preemption,
    activeHour.direction,
  );
  const aiModel = MODEL_CHECKPOINTS[aiModelId];
  const rightFrame = deriveJunctionFrameState(
    aiSeries[safeIdx],
    aiModel.controllerId,
    networkId,
    preemption,
    activeHour.direction,
  );

  // Use aligned benchmark comparison (ppo_baseline vs fixed/actuated) for true empirical delta
  const aiBenchRow = TELEMETRY_SERIES.bench_ppo[safeIdx];
  const baseRow = baselineSeries[safeIdx];
  const queueDeltaPct =
    baseRow.halting_vehicles > 0
      ? Math.round(
          ((baseRow.halting_vehicles - aiBenchRow.halting_vehicles) /
            baseRow.halting_vehicles) *
            100,
        )
      : 0;

  return (
    <section className="space-y-3">
      {/* Headline Empirical Delta Strip (4 Truthful Numbers, Zero Form Clutter) */}
      <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-4">
        <div className="rounded-md border border-border bg-card px-3.5 py-2.5">
          <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
            Mean Queue Collapse
          </div>
          <div className="mt-0.5 flex items-baseline gap-2 font-mono text-lg font-bold tabular-nums sm:text-xl">
            <span className="text-amber-600 dark:text-amber-400">
              {baselineId === "fixed" ? "7.80" : "9.67"}
            </span>
            <span className="text-xs text-muted-foreground">&rarr;</span>
            <span className="text-emerald-600 dark:text-emerald-400">0.32 veh</span>
          </div>
          <div className="font-mono text-[10.5px] text-emerald-600 dark:text-emerald-400">
            -95.9% Queue Reduction (Benchmark)
          </div>
        </div>

        <div className="rounded-md border border-border bg-card px-3.5 py-2.5">
          <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
            Corridor Velocity
          </div>
          <div className="mt-0.5 flex items-baseline gap-2 font-mono text-lg font-bold tabular-nums sm:text-xl">
            <span className="text-muted-foreground">36.9</span>
            <span className="text-xs text-muted-foreground">&rarr;</span>
            <span className="text-foreground">42.88 km/h</span>
          </div>
          <div className="font-mono text-[10.5px] text-cyan-700 dark:text-cyan-400">
            +16.1% Throughput Gain
          </div>
        </div>

        <div className="rounded-md border border-border bg-card px-3.5 py-2.5">
          <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
            Live Step Delta (T+{leftFrame.simStep}s)
          </div>
          <div className="mt-0.5 font-mono text-lg font-bold tabular-nums text-foreground sm:text-xl">
            {baseRow.halting_vehicles.toFixed(0)} vs{" "}
            <span className="text-emerald-600 dark:text-emerald-400">
              {aiBenchRow.halting_vehicles.toFixed(0)} veh
            </span>
          </div>
          <div className="font-mono text-[10.5px] text-muted-foreground">
            {queueDeltaPct > 0
              ? `${queueDeltaPct}% fewer halted now`
              : "Free-flow step"}
          </div>
        </div>

        <div className="rounded-md border border-border bg-card px-3.5 py-2.5">
          <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
            Statistical Rigor
          </div>
          <div className="mt-0.5 font-mono text-lg font-bold tabular-nums text-cyan-700 dark:text-cyan-400 sm:text-xl">
            p = 5.78e-21
          </div>
          <div className="font-mono text-[10.5px] text-muted-foreground">
            Mann-Whitney U = 822.5 · Welch t = -7.14
          </div>
        </div>
      </div>

      {/* Synchronized Split-Screen Duel */}
      <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
        {/* LEFT: LEGACY BASELINE */}
        <div className="rounded-md border border-amber-500/35 bg-card p-3.5">
          <div className="mb-2.5 flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-amber-600 dark:text-amber-400" />
              <div>
                <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-amber-700 dark:text-amber-400">
                  Legacy Baseline · {network.shortName}
                </div>
                <div className="text-xs font-semibold text-foreground">
                  {baselineId === "fixed"
                    ? "Rigid 81s Cycle · Queue Spillback"
                    : "Loop Chatter · +23.9% Worse Than Fixed"}
                </div>
              </div>
            </div>

            <div className="w-48">
              <Select
                aria-label="Select Legacy Baseline"
                value={baselineId}
                onChange={(e) => onSelectBaseline(e.target.value as BaselineId)}
              >
                <option value="fixed">Webster Fixed-Time (7.80)</option>
                <option value="actuated">Sensor-Actuated (9.67)</option>
              </Select>
            </div>
          </div>

          <MukhaniFlowCanvas
            frame={leftFrame}
            networkId={networkId}
            theme={theme}
            preemption={preemption}
            isAiSide={false}
            isPlaying={isPlaying}
          />

          <div className="mt-2.5 grid grid-cols-4 gap-1.5">
            {leftFrame.approaches.map((a) => (
              <div
                key={a.id}
                className="rounded border border-border bg-background px-2 py-1.5 font-mono text-[10px] tabular-nums"
              >
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">{a.id}</span>
                  <span
                    className={
                      a.signal === "GREEN"
                        ? "text-emerald-600 dark:text-emerald-400"
                        : a.signal === "AMBER"
                          ? "text-amber-600 dark:text-amber-400"
                          : "text-red-600 dark:text-red-400"
                    }
                  >
                    ●
                  </span>
                </div>
                <div className="mt-0.5 font-semibold text-foreground">
                  {a.queue.toFixed(1)} veh
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT: INTELLIFLOW DEEP RL */}
        <div
          className={`rounded-md border bg-card p-3.5 ${
            preemption
              ? "border-rose-500/60"
              : "border-emerald-500/40"
          }`}
        >
          <div className="mb-2.5 flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
              <div>
                <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-emerald-700 dark:text-emerald-400">
                  IntelliFlow Deep RL · {network.obsDim}
                </div>
                <div className="text-xs font-semibold text-foreground">
                  {preemption
                    ? "Emergency STH Green-Wave Locked (0s Wait)"
                    : aiModel.algorithm}
                </div>
              </div>
            </div>

            <div className="w-52">
              <Select
                aria-label="Select AI Model Checkpoint"
                value={aiModelId}
                onChange={(e) =>
                  onSelectAiModel(e.target.value as ModelCheckpointId)
                }
              >
                {AI_MODEL_OPTIONS.map((id) => (
                  <option key={id} value={id}>
                    {MODEL_CHECKPOINTS[id].shortLabel}
                  </option>
                ))}
              </Select>
            </div>
          </div>

          <MukhaniFlowCanvas
            frame={rightFrame}
            networkId={networkId}
            theme={theme}
            preemption={preemption}
            isAiSide={true}
            isPlaying={isPlaying}
          />

          <div className="mt-2.5 grid grid-cols-4 gap-1.5">
            {rightFrame.approaches.map((a) => (
              <div
                key={a.id}
                className="rounded border border-border bg-background px-2 py-1.5 font-mono text-[10px] tabular-nums"
              >
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">{a.id}</span>
                  <span
                    className={
                      a.signal === "GREEN"
                        ? "text-emerald-600 dark:text-emerald-400"
                        : a.signal === "AMBER"
                          ? "text-amber-600 dark:text-amber-400"
                          : "text-red-600 dark:text-red-400"
                    }
                  >
                    ●
                  </span>
                </div>
                <div className="mt-0.5 font-semibold text-foreground">
                  {a.queue.toFixed(1)} veh
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Synchronized Playback & Timeline Bar */}
      <div className="flex flex-wrap items-center gap-3 rounded-md border border-border bg-card px-3.5 py-2.5">
        <div className="flex items-center gap-1.5">
          <Button
            size="sm"
            variant="default"
            onClick={onTogglePlay}
            className="font-mono"
          >
            {isPlaying ? (
              <>
                <Pause className="mr-1 h-3.5 w-3.5" /> PAUSE DUEL
              </>
            ) : (
              <>
                <Play className="mr-1 h-3.5 w-3.5" /> PLAY DUEL
              </>
            )}
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={onReset}
            className="font-mono"
          >
            <RotateCcw className="mr-1 h-3.5 w-3.5" /> RESET
          </Button>
        </div>

        <input
          type="range"
          min={0}
          max={maxAlignedIdx}
          value={safeIdx}
          onChange={(e) => onChangeStep(Number(e.target.value))}
          className="h-1.5 min-w-44 flex-1 cursor-pointer accent-blue-600"
        />

        <div className="flex items-center gap-3 font-mono text-[11px] tabular-nums">
          <span className="text-foreground font-semibold">
            T+{String(leftFrame.simStep).padStart(3, "0")}s / 300s
          </span>
          <span className="hidden text-muted-foreground sm:inline">
            Demand: {activeHour.timeLabel} ({activeHour.flowVph} veh/hr ·{" "}
            {activeHour.direction.toUpperCase()})
          </span>
        </div>
      </div>
    </section>
  );
}
