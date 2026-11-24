import * as React from "react";
import type {
  JunctionFrameState,
  NetworkId,
  SignalState,
  ThemeMode,
} from "@/types/telemetry";

interface MukhaniFlowCanvasProps {
  frame: JunctionFrameState;
  networkId: NetworkId;
  theme: ThemeMode;
  preemption: boolean;
  isAiSide: boolean;
  isPlaying: boolean;
}

type VehicleKind = "2w" | "auto" | "car" | "bus";

interface Sprite {
  approach: "W" | "E" | "N" | "S";
  kind: VehicleKind;
  progress: number; // 0 (edge entry) -> 1 (stop line) -> 1.65 (cleared exit)
  laneIdx: number;
  lateralOffset: number;
  baseSpeed: number;
}

const FLEET_TYPES: VehicleKind[] = [
  "2w", "2w", "2w", "2w",
  "auto", "auto", "auto",
  "car", "car",
  "bus",
];

function createInitialPool(): Sprite[] {
  const approaches: Array<"W" | "E" | "N" | "S"> = ["W", "E", "N", "S"];
  const pool: Sprite[] = [];
  for (let i = 0; i < 40; i++) {
    const app = approaches[i % 4];
    const kind = FLEET_TYPES[i % FLEET_TYPES.length];
    pool.push({
      approach: app,
      kind,
      progress: ((i * 0.13) % 1.45),
      laneIdx: i % 2,
      lateralOffset: ((i % 3) - 1) * 4,
      baseSpeed: kind === "2w" ? 1.18 : kind === "auto" ? 0.92 : kind === "bus" ? 0.78 : 1.0,
    });
  }
  return pool;
}

function drawSignalPod(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  state: SignalState,
) {
  ctx.save();
  ctx.fillStyle = "#0B0E14";
  ctx.strokeStyle = "#334155";
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.roundRect(x, y, 18, 44, 4);
  ctx.fill();
  ctx.stroke();

  const bulbs: Array<[number, boolean, string, string]> = [
    [y + 9, state === "RED", "#EF4444", "#3B1317"],
    [y + 22, state === "AMBER", "#F59E0B", "#3A270B"],
    [y + 35, state === "GREEN", "#10B981", "#0D2B22"],
  ];

  for (const [cy, on, onColor, offColor] of bulbs) {
    if (on) {
      ctx.shadowColor = onColor;
      ctx.shadowBlur = 10;
    } else {
      ctx.shadowBlur = 0;
    }
    ctx.fillStyle = on ? onColor : offColor;
    ctx.beginPath();
    ctx.arc(x + 9, cy, 4.2, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();
}

export function MukhaniFlowCanvas({
  frame,
  networkId,
  theme,
  preemption,
  isAiSide,
  isPlaying,
}: MukhaniFlowCanvasProps) {
  const canvasRef = React.useRef<HTMLCanvasElement | null>(null);
  const poolRef = React.useRef<Sprite[]>(createInitialPool());
  const ambProgressRef = React.useRef(0.15);
  const frameRef = React.useRef(frame);
  const propsRef = React.useRef({ networkId, theme, preemption, isAiSide, isPlaying });

  frameRef.current = frame;
  propsRef.current = { networkId, theme, preemption, isAiSide, isPlaying };

  React.useEffect(() => {
    let rafId = 0;
    let lastTime = performance.now();

    const render = (now: number) => {
      const dt = Math.min(0.05, (now - lastTime) / 1000);
      lastTime = now;

      const canvas = canvasRef.current;
      if (!canvas) {
        rafId = requestAnimationFrame(render);
        return;
      }

      const W = 540;
      const H = 320;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      if (canvas.width !== W * dpr || canvas.height !== H * dpr) {
        canvas.width = W * dpr;
        canvas.height = H * dpr;
      }

      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      const cur = frameRef.current;
      const { networkId: net, theme: th, preemption: pre, isAiSide: ai, isPlaying: playing } = propsRef.current;

      const isDark = th === "dark";
      const bgCanvas = isDark ? "#080B10" : "#E8EEF5";
      const roadColor = isDark ? "#151B26" : "#334155";
      const jctColor = isDark ? "#1A2232" : "#1E293B";
      const curbColor = isDark ? "#283347" : "#64748B";
      const labelColor = isDark ? "#94A3B8" : "#334155";

      ctx.fillStyle = bgCanvas;
      ctx.fillRect(0, 0, W, H);

      const cx = W / 2;
      const cy = H / 2;
      const hRoadH = net === "single" ? 84 : 100;
      const vRoadW = 88;
      const xL = cx - vRoadW / 2;
      const xR = cx + vRoadW / 2;
      const yT = cy - hRoadH / 2;
      const yB = cy + hRoadH / 2;

      // Roads
      ctx.fillStyle = roadColor;
      ctx.fillRect(0, yT, W, hRoadH);
      ctx.fillRect(xL, 0, vRoadW, H);
      ctx.fillStyle = jctColor;
      ctx.fillRect(xL, yT, vRoadW, hRoadH);

      // Curbs
      ctx.strokeStyle = curbColor;
      ctx.lineWidth = 1.2;
      ctx.strokeRect(0, yT, xL, 0.5);
      ctx.strokeRect(xR, yT, W - xR, 0.5);
      ctx.strokeRect(0, yB, xL, 0.5);
      ctx.strokeRect(xR, yB, W - xR, 0.5);

      // Medians (amber centerline)
      ctx.strokeStyle = "rgba(245, 158, 11, 0.72)";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(0, cy); ctx.lineTo(xL - 6, cy);
      ctx.moveTo(xR + 6, cy); ctx.lineTo(W, cy);
      ctx.moveTo(cx, 0); ctx.lineTo(cx, yT - 6);
      ctx.moveTo(cx, yB + 6); ctx.lineTo(cx, H);
      ctx.stroke();

      // Sublane dashed markings
      ctx.strokeStyle = "rgba(148, 163, 184, 0.3)";
      ctx.setLineDash([5, 6]);
      ctx.lineWidth = 1;
      ctx.beginPath();
      const laneOffsets = net === "single" ? [21] : [16, 33];
      for (const off of laneOffsets) {
        ctx.moveTo(0, cy + off); ctx.lineTo(xL - 6, cy + off);
        ctx.moveTo(0, cy - off); ctx.lineTo(xL - 6, cy - off);
        ctx.moveTo(xR + 6, cy + off); ctx.lineTo(W, cy + off);
        ctx.moveTo(xR + 6, cy - off); ctx.lineTo(W, cy - off);
      }
      ctx.moveTo(cx - 22, 0); ctx.lineTo(cx - 22, yT - 6);
      ctx.moveTo(cx + 22, 0); ctx.lineTo(cx + 22, yT - 6);
      ctx.moveTo(cx - 22, yB + 6); ctx.lineTo(cx - 22, H);
      ctx.moveTo(cx + 22, yB + 6); ctx.lineTo(cx + 22, H);
      ctx.stroke();
      ctx.setLineDash([]);

      // Stop lines
      ctx.strokeStyle = "#E2E8F0";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(xL - 3, cy + 2); ctx.lineTo(xL - 3, yB - 2);
      ctx.moveTo(xR + 3, yT + 2); ctx.lineTo(xR + 3, cy - 2);
      ctx.moveTo(xL + 2, yT - 3); ctx.lineTo(cx - 2, yT - 3);
      ctx.moveTo(cx + 2, yB + 3); ctx.lineTo(xR - 2, yB + 3);
      ctx.stroke();

      // Emergency Green-Wave Path Vector
      if (pre && ai) {
        ctx.save();
        ctx.strokeStyle = "#F43F5E";
        ctx.lineWidth = 3;
        ctx.setLineDash([7, 5]);
        ctx.lineDashOffset = -(now * 0.04);
        ctx.beginPath();
        ctx.moveTo(12, cy + 26);
        ctx.lineTo(cx - 10, cy + 26);
        ctx.quadraticCurveTo(cx + 20, cy + 26, cx + 20, cy + 56);
        ctx.lineTo(cx + 20, H - 8);
        ctx.stroke();
        ctx.restore();
      }

      // Update and render vehicles proportional to real CSV halting_vehicles + speed
      const speedNorm = Math.max(0.35, Math.min(1.3, cur.speedKmh / 38));
      const queueNorm = Math.min(1, cur.totalQueue / 20);
      const activeSpritesPerApproach = ai
        ? Math.max(2, Math.min(8, Math.round(3 + queueNorm * 4)))
        : Math.max(4, Math.min(10, Math.round(4 + queueNorm * 6)));

      const counts: Record<"W" | "E" | "N" | "S", number> = { W: 0, E: 0, N: 0, S: 0 };

      for (const s of poolRef.current) {
        counts[s.approach]++;
        if (counts[s.approach] > activeSpritesPerApproach) continue;

        const isEW = s.approach === "W" || s.approach === "E";
        const sig = isEW ? cur.ewSignal : cur.nsSignal;
        const stopPos = 0.88 - ((counts[s.approach] - 1) * (ai ? 0.05 : 0.075));

        if (playing) {
          if (sig === "GREEN" || s.progress > 0.94) {
            s.progress += dt * 0.34 * s.baseSpeed * speedNorm;
          } else {
            // Approach queue creep; two-wheelers filter closer toward stop line
            const filterBonus = s.kind === "2w" ? 0.08 : s.kind === "auto" ? 0.03 : 0;
            const targetStop = Math.min(0.92, stopPos + filterBonus);
            if (s.progress < targetStop) {
              s.progress = Math.min(targetStop, s.progress + dt * 0.25 * s.baseSpeed);
            }
          }
          if (s.progress > 1.72) {
            s.progress = 0.02;
          }
        }

        // Convert progress into canvas (x, y)
        let vx = 0;
        let vy = 0;
        let horiz = true;
        const laneShift = s.laneIdx === 0 ? 15 : 32;
        const sublaneWeave = s.kind === "2w" && sig === "RED" ? Math.sin(now * 0.004 + s.laneIdx) * 3 : 0;

        if (s.approach === "W") {
          horiz = true;
          vx = s.progress <= 1 ? s.progress * (xL - 8) : (xL - 8) + (s.progress - 1) * (W - xL + 40);
          vy = cy + laneShift + sublaneWeave;
        } else if (s.approach === "E") {
          horiz = true;
          vx = s.progress <= 1 ? W - s.progress * (W - xR - 8) : (xR + 8) - (s.progress - 1) * (xR + 40);
          vy = cy - laneShift - sublaneWeave;
        } else if (s.approach === "N") {
          horiz = false;
          vx = cx - (s.laneIdx === 0 ? 14 : 30) - sublaneWeave;
          vy = s.progress <= 1 ? s.progress * (yT - 8) : (yT - 8) + (s.progress - 1) * (H - yT + 40);
        } else {
          horiz = false;
          vx = cx + (s.laneIdx === 0 ? 14 : 30) + sublaneWeave;
          vy = s.progress <= 1 ? H - s.progress * (H - yB - 8) : (yB + 8) - (s.progress - 1) * (yB + 40);
        }

        // Vehicle dimensions & colors from mukhani.rou.xml
        let len = 13;
        let wid = 6.5;
        let col = "#3B82F6";
        if (s.kind === "2w") {
          len = 7; wid = 3.5; col = "#10B981";
        } else if (s.kind === "auto") {
          len = 10; wid = 5.5; col = "#F59E0B";
        } else if (s.kind === "bus") {
          len = 22; wid = 8.5; col = "#8B5CF6";
        }

        ctx.fillStyle = col;
        ctx.strokeStyle = "#0B0E14";
        ctx.lineWidth = 0.8;
        ctx.beginPath();
        const rw = horiz ? len : wid;
        const rh = horiz ? wid : len;
        ctx.roundRect(vx - rw / 2, vy - rh / 2, rw, rh, 1.8);
        ctx.fill();
        ctx.stroke();

        // Red brake lights when queued at RED
        if (sig === "RED" && s.progress > 0.25 && s.progress < 0.95) {
          ctx.fillStyle = "#EF4444";
          ctx.fillRect(vx - 1.5, vy - 1.5, 2.5, 2.5);
        }
      }

      // Emergency Ambulance Sprite
      if (pre) {
        if (playing) {
          if (ai) {
            ambProgressRef.current += dt * 0.42;
            if (ambProgressRef.current > 1.7) ambProgressRef.current = 0.05;
          } else {
            // Stalled behind Legacy red-phase spillback
            const target = cur.ewSignal === "GREEN" ? 1.5 : 0.62;
            if (ambProgressRef.current < target) {
              ambProgressRef.current += dt * 0.22;
            }
            if (ambProgressRef.current > 1.7) ambProgressRef.current = 0.05;
          }
        }
        const ap = ambProgressRef.current;
        const ax = ap <= 1 ? ap * (xL + 10) : cx + 20;
        const ay = ap <= 1 ? cy + 25 : cy + 25 + (ap - 1) * 180;

        const flash = Math.sin(now * 0.015) > 0;
        ctx.save();
        ctx.shadowColor = "#F43F5E";
        ctx.shadowBlur = 12;
        ctx.fillStyle = "#FFFFFF";
        ctx.strokeStyle = "#F43F5E";
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.roundRect(ax - 10, ay - 5, 20, 10, 2.5);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = flash ? "#F43F5E" : "#3B82F6";
        ctx.fillRect(ax - 2, ay - 3, 4, 6);
        ctx.restore();
      }

      // 4 Signal Pods
      drawSignalPod(ctx, xL - 26, yB + 6, cur.ewSignal);
      drawSignalPod(ctx, xR + 8, yT - 50, cur.ewSignal);
      drawSignalPod(ctx, xL - 26, yT - 50, cur.nsSignal);
      drawSignalPod(ctx, xR + 8, yB + 6, cur.nsSignal);

      // Center Junction Phase Readout
      ctx.fillStyle = isDark ? "rgba(11, 14, 20, 0.92)" : "rgba(15, 23, 42, 0.92)";
      ctx.strokeStyle = pre && ai ? "#F43F5E" : cur.ewSignal === "GREEN" || cur.nsSignal === "GREEN" ? "#10B981" : "#F59E0B";
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.roundRect(cx - 48, cy - 22, 96, 44, 5);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "#94A3B8";
      ctx.font = "600 8.5px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(pre && ai ? "PREEMPT" : cur.phaseLabel.slice(0, 11), cx, cy - 5);

      ctx.fillStyle = "#F8FAFC";
      ctx.font = "700 10px 'JetBrains Mono', monospace";
      ctx.fillText(`Q:${cur.totalQueue.toFixed(1)} | ${cur.speedKmh}k`, cx, cy + 12);

      // Road axis labels
      ctx.fillStyle = labelColor;
      ctx.font = "600 9px 'Inter', sans-serif";
      ctx.textAlign = "left";
      ctx.fillText(net === "single" ? "WEST (2L)" : "KALADHUNGI W (3L)", 10, yT - 8);
      ctx.textAlign = "right";
      ctx.fillText(net === "single" ? "EAST (2L)" : "KALADHUNGI E (3L)", W - 10, yT - 8);

      rafId = requestAnimationFrame(render);
    };

    rafId = requestAnimationFrame(render);
    return () => cancelAnimationFrame(rafId);
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="block h-auto w-full rounded-md border border-border"
      style={{ aspectRatio: "540 / 320" }}
    />
  );
}
