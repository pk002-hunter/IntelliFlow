import * as React from "react";
import { CONTROLLER_BENCHMARKS, TELEMETRY_SERIES } from "@/data/telemetry";
import type { BaselineId, ControllerId, ModelCheckpointId } from "@/types/telemetry";

interface ControllerRaceArenaProps {
  stepIdx: number;
  baselineId: BaselineId;
  aiModelId: ModelCheckpointId;
}

const RADAR_METRICS: Record<
  ControllerId,
  { scores: [number, number, number, number, number]; color: string; label: string }
> = {
  // Axes: [Queue Suppression, Peak Stability, Corridor Velocity, Wait Efficiency, Flow Consistency]
  ppo: { scores: [97, 94, 92, 96, 95], color: "#10B981", label: "PPO Agent" },
  dqn: { scores: [97, 94, 92, 96, 95], color: "#3B82F6", label: "Double DQN" },
  fixed: { scores: [32, 38, 62, 42, 45], color: "#F59E0B", label: "Webster Fixed" },
  actuated: { scores: [18, 22, 58, 30, 28], color: "#EF4444", label: "Sensor-Actuated" },
};

const AXES = [
  "Queue Suppression",
  "Peak Stability",
  "Corridor Speed",
  "Wait Efficiency",
  "Flow Consistency",
];

function ControllerRadarSvg() {
  const [visible, setVisible] = React.useState<Record<ControllerId, boolean>>({
    ppo: true,
    dqn: false,
    fixed: true,
    actuated: true,
  });

  const cx = 155;
  const cy = 135;
  const rMax = 88;
  const angleAt = (i: number) => -Math.PI / 2 + (i * 2 * Math.PI) / 5;

  const pointAt = (i: number, pct: number) => {
    const rad = (pct / 100) * rMax;
    const a = angleAt(i);
    return `${(cx + rad * Math.cos(a)).toFixed(1)},${(cy + rad * Math.sin(a)).toFixed(1)}`;
  };

  return (
    <div className="rounded-md border border-border bg-card p-3.5">
      <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
        <div>
          <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-cyan-700 dark:text-cyan-400">
            5-Axis Controller Trade-Off
          </div>
          <div className="text-xs font-semibold text-foreground">
            Normalized Multi-Objective Profile (Outer = Better)
          </div>
        </div>
        <div className="flex flex-wrap gap-1.5">
          {(Object.keys(RADAR_METRICS) as ControllerId[]).map((cid) => {
            const m = RADAR_METRICS[cid];
            const active = visible[cid];
            return (
              <button
                key={cid}
                type="button"
                onClick={() => setVisible((v) => ({ ...v, [cid]: !v[cid] }))}
                className={`cursor-pointer rounded border px-2 py-0.5 font-mono text-[10px] font-semibold transition-opacity ${
                  active ? "border-border bg-secondary text-foreground opacity-100" : "border-border bg-background text-muted-foreground opacity-45"
                }`}
              >
                <span
                  className="mr-1 inline-block h-2 w-2 rounded-full"
                  style={{ backgroundColor: m.color }}
                />
                {m.label}
              </button>
            );
          })}
        </div>
      </div>

      <svg viewBox="0 0 310 270" className="mx-auto w-full max-w-[330px]">
        {[25, 50, 75, 100].map((ring) => (
          <polygon
            key={ring}
            points={AXES.map((_, i) => pointAt(i, ring)).join(" ")}
            fill="none"
            stroke="currentColor"
            strokeOpacity={0.14}
            strokeWidth={1}
          />
        ))}
        {AXES.map((label, i) => {
          const a = angleAt(i);
          const tx = cx + (rMax + 24) * Math.cos(a);
          const ty = cy + (rMax + 18) * Math.sin(a);
          return (
            <g key={label}>
              <line
                x1={cx}
                y1={cy}
                x2={cx + rMax * Math.cos(a)}
                y2={cy + rMax * Math.sin(a)}
                stroke="currentColor"
                strokeOpacity={0.14}
                strokeWidth={1}
              />
              <text
                x={tx}
                y={ty}
                textAnchor="middle"
                fill="currentColor"
                fillOpacity={0.72}
                fontSize={8.5}
                fontWeight={600}
                fontFamily="Inter, sans-serif"
              >
                {label}
              </text>
            </g>
          );
        })}

        {(Object.keys(RADAR_METRICS) as ControllerId[]).map((cid) => {
          if (!visible[cid]) return null;
          const m = RADAR_METRICS[cid];
          const pts = m.scores.map((s, i) => pointAt(i, s)).join(" ");
          return (
            <polygon
              key={cid}
              points={pts}
              fill={m.color}
              fillOpacity={0.18}
              stroke={m.color}
              strokeWidth={2}
            />
          );
        })}
      </svg>

      <div className="mt-1 grid grid-cols-2 gap-1.5 font-mono text-[10px] tabular-nums text-muted-foreground sm:grid-cols-4">
        {Object.values(CONTROLLER_BENCHMARKS).map((b) => (
          <div key={b.id} className="rounded border border-border bg-background px-2 py-1">
            <div className="truncate font-semibold text-foreground">{b.label}</div>
            <div>Q: {b.meanQueue} · σ={b.stdQueue}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function ControllerRaceArena({
  stepIdx,
  baselineId,
  aiModelId,
}: ControllerRaceArenaProps) {
  const safeIdx = Math.min(stepIdx, TELEMETRY_SERIES.fixed.length - 1);
  const currentSimStep = TELEMETRY_SERIES.fixed[safeIdx].step;

  const racers = [
    {
      name: "Sensor-Actuated (Gap-Out)",
      series: TELEMETRY_SERIES.actuated,
      color: "#EF4444",
      textCls: "text-red-600 dark:text-red-400",
    },
    {
      name: "Webster Fixed-Time",
      series: TELEMETRY_SERIES.fixed,
      color: "#F59E0B",
      textCls: "text-amber-600 dark:text-amber-400",
    },
    {
      name: "Double DQN Agent",
      series: TELEMETRY_SERIES.bench_dqn,
      color: "#3B82F6",
      textCls: "text-blue-600 dark:text-blue-400",
    },
    {
      name: aiModelId === "ppo_mukhani" ? "PPO Agent (Benchmark)" : "PPO Agent",
      series: TELEMETRY_SERIES.bench_ppo,
      color: "#10B981",
      textCls: "text-emerald-600 dark:text-emerald-400",
    },
  ];

  // Cumulative vehicle-seconds halted up to current playhead step
  const cumScores = racers.map((r) => {
    let sum = 0;
    for (let i = 0; i <= safeIdx; i++) {
      sum += (r.series[i]?.halting_vehicles ?? 0) * 10;
    }
    const nowQ = r.series[safeIdx]?.halting_vehicles ?? 0;
    const nowSpd = (r.series[safeIdx]?.mean_speed ?? 0) * 3.6;
    return { ...r, cumVehSec: Math.round(sum), nowQ, nowSpd };
  });
  const maxCum = Math.max(100, ...cumScores.map((c) => c.cumVehSec));

  // SVG trajectory chart (0..300s) comparing active Baseline vs PPO & DQN
  const W = 540;
  const H = 135;
  const padX = 28;
  const padY = 14;
  const maxY = 30;
  const toX = (i: number) => padX + (i / 29) * (W - padX * 2);
  const toY = (q: number) => padY + (H - padY * 2) - (Math.min(maxY, q) / maxY) * (H - padY * 2);

  const buildPath = (rows: typeof TELEMETRY_SERIES.fixed) =>
    rows
      .slice(0, 30)
      .map((r, i) => `${i === 0 ? "M" : "L"} ${toX(i).toFixed(1)} ${toY(r.halting_vehicles).toFixed(1)}`)
      .join(" ");

  const activeBaseSeries = baselineId === "fixed" ? TELEMETRY_SERIES.fixed : TELEMETRY_SERIES.actuated;

  return (
    <section className="grid grid-cols-1 gap-3 lg:grid-cols-12">
      <div className="rounded-md border border-border bg-card p-3.5 lg:col-span-7">
        <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
          <div>
            <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-cyan-700 dark:text-cyan-400">
              Empirical Delay Race · Aligned 10s &ndash; 300s Window
            </div>
            <div className="text-xs font-semibold text-foreground">
              Cumulative Vehicle-Seconds Halted (Lower = Better)
            </div>
          </div>
          <span className="rounded border border-border bg-secondary px-2 py-0.5 font-mono text-[11px] font-semibold tabular-nums text-foreground">
            T+{currentSimStep}s
          </span>
        </div>

        <div className="space-y-2.5">
          {cumScores.map((r) => {
            const pct = Math.max(2, Math.round((r.cumVehSec / maxCum) * 100));
            return (
              <div key={r.name} className="space-y-1">
                <div className="flex items-center justify-between font-mono text-[11px] tabular-nums">
                  <span className="font-semibold text-foreground">{r.name}</span>
                  <span className={r.textCls}>
                    {r.cumVehSec.toLocaleString()} veh·s · Q={r.nowQ.toFixed(0)} · {r.nowSpd.toFixed(1)} km/h
                  </span>
                </div>
                <div className="h-2.5 w-full overflow-hidden rounded-sm bg-secondary">
                  <div
                    className="h-full rounded-sm transition-all duration-300"
                    style={{ width: `${pct}%`, backgroundColor: r.color }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        {/* Synchronized Queue Trajectory Chart */}
        <div className="mt-4 rounded-md border border-border bg-background p-2.5">
          <div className="mb-1 flex items-center justify-between font-mono text-[10px] text-muted-foreground">
            <span>QUEUE SPIKE TRAJECTORY (0 &ndash; 300s)</span>
            <span>
              {baselineId === "fixed" ? "Amber: Webster Fixed" : "Red: Sensor-Actuated"} vs Emerald: PPO
            </span>
          </div>
          <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
            {[10, 20, 30].map((tick) => (
              <g key={tick}>
                <line
                  x1={padX}
                  y1={toY(tick)}
                  x2={W - padX}
                  y2={toY(tick)}
                  stroke="currentColor"
                  strokeOpacity={0.12}
                  strokeDasharray="3 4"
                />
                <text
                  x={4}
                  y={toY(tick) + 3}
                  fill="currentColor"
                  fillOpacity={0.5}
                  fontSize={8.5}
                  fontFamily="JetBrains Mono, monospace"
                >
                  {tick}
                </text>
              </g>
            ))}
            <path
              d={buildPath(activeBaseSeries)}
              fill="none"
              stroke={baselineId === "fixed" ? "#F59E0B" : "#EF4444"}
              strokeWidth={1.8}
            />
            <path
              d={buildPath(TELEMETRY_SERIES.bench_ppo)}
              fill="none"
              stroke="#10B981"
              strokeWidth={2}
            />
            <line
              x1={toX(safeIdx)}
              y1={padY - 4}
              x2={toX(safeIdx)}
              y2={H - padY + 4}
              stroke="#2563EB"
              strokeWidth={1.5}
              strokeDasharray="3 3"
            />
          </svg>
        </div>
      </div>

      <div className="lg:col-span-5">
        <ControllerRadarSvg />
      </div>
    </section>
  );
}
