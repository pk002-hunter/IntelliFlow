import * as React from "react";
import { Ambulance, Hospital, Maximize2, Pause, Play, Route, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { EMERGENCY_CORRIDORS, HALDWANI_TOPOLOGY } from "@/data/telemetry";
import type { DiurnalHourSpec, ThemeMode } from "@/types/telemetry";

interface HaldwaniCorridorMapProps {
  preemption: boolean;
  heroMode?: boolean;
  theme?: ThemeMode;
  activeHour?: DiurnalHourSpec;
  isPlaying?: boolean;
  onTogglePlay?: () => void;
  speedMultiplier?: number;
  onZoomMukhani?: () => void;
}

const HOSPITAL_TO_CORRIDOR: Record<string, string> = {
  HOSP_STH: "sth_rampur",
  HOSP_UJALA: "sth_rampur",
  HOSP_NEELKANTH: "sth_gasgodam",
  HOSP_BASE: "base_nh109",
  HOSP_BRIJLAL: "base_nh109",
  HOSP_KRISHNA: "base_nh109",
  HOSP_KATHGODAM: "base_nh109",
  HOSP_BOMBAY: "base_nh109",
};

interface CityVehicle {
  edgeIdx: number;
  t: number;
  dir: 1 | -1;
  speed: number;
  kind: "2w" | "auto" | "car" | "bus";
}

export function HaldwaniCorridorMap({
  preemption,
  heroMode = false,
  theme = "dark",
  activeHour,
  isPlaying = true,
  onTogglePlay,
  speedMultiplier = 1,
  onZoomMukhani,
}: HaldwaniCorridorMapProps) {
  const [corridorKey, setCorridorKey] = React.useState("sth_rampur");
  const [showShortcuts, setShowShortcuts] = React.useState(true);
  const [query, setQuery] = React.useState("");
  const [selectedHospitalId, setSelectedHospitalId] = React.useState<string>("HOSP_STH");
  const [hoveredTls, setHoveredTls] = React.useState<string | null>(null);

  const canvasRef = React.useRef<HTMLCanvasElement | null>(null);

  const nodeMap = React.useMemo(
    () => Object.fromEntries(HALDWANI_TOPOLOGY.nodes.map((n) => [n.id, n])),
    [],
  );

  const corridor = EMERGENCY_CORRIDORS[corridorKey];

  const selectHospital = (hid: string) => {
    setSelectedHospitalId(hid);
    const matched = HOSPITAL_TO_CORRIDOR[hid];
    if (matched) setCorridorKey(matched);
  };

  const hospitals = HALDWANI_TOPOLOGY.landmarks.filter(
    (l) =>
      l.type === "hospital" &&
      `${l.id} ${l.name}`.toLowerCase().includes(query.trim().toLowerCase()),
  );

  // Live state refs for smooth 60fps Canvas loop
  const stateRef = React.useRef({
    preemption,
    heroMode,
    theme,
    corridorKey,
    showShortcuts,
    selectedHospitalId,
    isPlaying,
    speedMultiplier,
    flowVph: activeHour?.flowVph ?? 2400,
    direction: activeHour?.direction ?? "inbound",
  });
  stateRef.current = {
    preemption,
    heroMode,
    theme,
    corridorKey,
    showShortcuts,
    selectedHospitalId,
    isPlaying,
    speedMultiplier,
    flowVph: activeHour?.flowVph ?? 2400,
    direction: activeHour?.direction ?? "inbound",
  };

  // Seed city-wide vehicles across Haldwani edges
  const vehiclesRef = React.useRef<CityVehicle[] | null>(null);
  if (!vehiclesRef.current) {
    const kinds: Array<CityVehicle["kind"]> = ["2w", "2w", "2w", "2w", "auto", "auto", "auto", "car", "car", "bus"];
    const list: CityVehicle[] = [];
    for (let i = 0; i < 110; i++) {
      list.push({
        edgeIdx: i % HALDWANI_TOPOLOGY.edges.length,
        t: (i * 0.17) % 1,
        dir: i % 2 === 0 ? 1 : -1,
        speed: 0.18 + ((i % 5) * 0.04),
        kind: kinds[i % kinds.length],
      });
    }
    vehiclesRef.current = list;
  }

  const ambSweepRef = React.useRef(0);

  React.useEffect(() => {
    let rafId = 0;
    let lastTime = performance.now();

    const draw = (now: number) => {
      const dt = Math.min(0.05, (now - lastTime) / 1000);
      lastTime = now;

      const canvas = canvasRef.current;
      if (!canvas) {
        rafId = requestAnimationFrame(draw);
        return;
      }

      const st = stateRef.current;
      const W = st.heroMode ? 960 : 740;
      const H = st.heroMode ? 540 : 420;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);

      if (canvas.width !== W * dpr || canvas.height !== H * dpr) {
        canvas.width = W * dpr;
        canvas.height = H * dpr;
      }
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      const projX = (x: number) => ((x + 2150) / 4050) * (W - 70) + 35;
      const projY = (y: number) => (H - 35) - ((y + 2550) / 5100) * (H - 70);

      const isDark = st.theme === "dark";
      ctx.fillStyle = isDark ? "#080B10" : "#E8EEF5";
      ctx.fillRect(0, 0, W, H);

      // Subtle coordinate gridlines
      ctx.strokeStyle = isDark ? "rgba(255,255,255,0.035)" : "rgba(15,23,42,0.05)";
      ctx.lineWidth = 1;
      for (let gx = 80; gx < W; gx += 120) {
        ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, H); ctx.stroke();
      }
      for (let gy = 80; gy < H; gy += 120) {
        ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(W, gy); ctx.stroke();
      }

      const edgeColor = (cat: string) => {
        if (cat === "kaladhungi") return "#3B82F6";
        if (cat === "nainital") return "#06B6D4";
        if (cat === "rampur") return isDark ? "#64748B" : "#475569";
        if (cat === "shortcut") return "#10B981";
        return "#F43F5E";
      };

      // 1. Draw Road Corridors
      for (const edge of HALDWANI_TOPOLOGY.edges) {
        if (edge.category === "shortcut" && !st.showShortcuts) continue;
        const n1 = nodeMap[edge.from];
        const n2 = nodeMap[edge.to];
        if (!n1 || !n2) continue;

        ctx.save();
        ctx.strokeStyle = edgeColor(edge.category);
        ctx.globalAlpha = edge.category === "shortcut" ? 0.65 : 0.78;
        ctx.lineWidth = edge.category === "shortcut" || edge.category === "gully" ? 1.8 : st.heroMode ? 3.8 : 2.8;
        if (edge.category === "shortcut") ctx.setLineDash([6, 5]);
        ctx.beginPath();
        ctx.moveTo(projX(n1.x), projY(n1.y));
        ctx.lineTo(projX(n2.x), projY(n2.y));
        ctx.stroke();
        ctx.restore();
      }

      // 2. Highlight Selected Emergency Corridor Route
      const activeCorridor = EMERGENCY_CORRIDORS[st.corridorKey];
      const routeNodes = activeCorridor.routeNodes.map((id) => nodeMap[id]).filter(Boolean);
      if (routeNodes.length >= 2) {
        ctx.save();
        ctx.strokeStyle = st.preemption ? "#F43F5E" : "#10B981";
        ctx.lineWidth = st.preemption ? 5 : 3.5;
        ctx.lineJoin = "round";
        ctx.lineCap = "round";
        if (st.preemption) {
          ctx.setLineDash([10, 6]);
          ctx.lineDashOffset = -(now * 0.05 * st.speedMultiplier);
        }
        ctx.beginPath();
        routeNodes.forEach((n, idx) => {
          const px = projX(n.x);
          const py = projY(n.y);
          if (idx === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        });
        ctx.stroke();
        ctx.restore();
      }

      // 3. Animate City-Wide Mixed-Traffic Flow Particles Along Corridors
      const flowFraction = Math.min(1, Math.max(0.22, st.flowVph / 2700));
      const activeCount = Math.round((vehiclesRef.current?.length ?? 100) * flowFraction);
      const speedScale = st.flowVph > 2200 ? 0.72 : 1.15;

      const kindColor: Record<CityVehicle["kind"], string> = {
        "2w": "#10B981",
        auto: "#F59E0B",
        car: "#60A5FA",
        bus: "#A78BFA",
      };

      const vList = vehiclesRef.current ?? [];
      for (let i = 0; i < activeCount; i++) {
        const v = vList[i];
        const edge = HALDWANI_TOPOLOGY.edges[v.edgeIdx];
        if (!edge) continue;
        if (edge.category === "shortcut" && !st.showShortcuts) continue;

        const n1 = nodeMap[edge.from];
        const n2 = nodeMap[edge.to];
        if (!n1 || !n2) continue;

        if (st.isPlaying) {
          // Inbound bias moves particles faster toward city center during Morning Peak
          const dirBoost =
            st.direction === "inbound" && v.dir === 1
              ? 1.25
              : st.direction === "outbound" && v.dir === -1
                ? 1.25
                : 0.9;
          v.t += dt * v.speed * speedScale * dirBoost * Math.min(3, st.speedMultiplier) * v.dir;
          if (v.t > 1) v.t = 0;
          if (v.t < 0) v.t = 1;
        }

        const x1 = projX(n1.x);
        const y1 = projY(n1.y);
        const x2 = projX(n2.x);
        const y2 = projY(n2.y);

        // Slight lateral lane offset perpendicular to road vector
        const dx = x2 - x1;
        const dy = y2 - y1;
        const len = Math.hypot(dx, dy) || 1;
        const nx = (-dy / len) * (v.dir * 3);
        const ny = (dx / len) * (v.dir * 3);

        const px = x1 + dx * v.t + nx;
        const py = y1 + dy * v.t + ny;

        ctx.fillStyle = kindColor[v.kind];
        ctx.beginPath();
        ctx.arc(px, py, v.kind === "bus" ? 3.2 : v.kind === "2w" ? 1.9 : 2.4, 0, Math.PI * 2);
        ctx.fill();
      }

      // 4. Signalized Traffic Light Junctions (with live Green/Red phase pulses)
      const phaseFlip = Math.floor(now / 3200) % 2;
      let activeAmbSeg = -1;
      let ambPos: { x: number; y: number } | null = null;

      if (st.preemption && routeNodes.length >= 2) {
        if (st.isPlaying) {
          ambSweepRef.current = (ambSweepRef.current + dt * 0.22 * st.speedMultiplier) % 1;
        }
        const segCount = routeNodes.length - 1;
        const scaled = ambSweepRef.current * segCount;
        activeAmbSeg = Math.min(segCount - 1, Math.floor(scaled));
        const localT = scaled - activeAmbSeg;
        const a = routeNodes[activeAmbSeg];
        const b = routeNodes[activeAmbSeg + 1];
        ambPos = {
          x: projX(a.x + (b.x - a.x) * localT),
          y: projY(a.y + (b.y - a.y) * localT),
        };
      } else {
        ambSweepRef.current = 0;
      }

      HALDWANI_TOPOLOGY.nodes
        .filter((n) => n.type === "traffic_light")
        .forEach((n, idx) => {
          const px = projX(n.x);
          const py = projY(n.y);
          const routeIdx = activeCorridor.routeNodes.indexOf(n.id);
          const onRoute = routeIdx !== -1;
          const greenWave = st.preemption && onRoute && routeIdx <= activeAmbSeg + 1;
          const isGreen = greenWave || (idx + phaseFlip) % 2 === 0;

          if (greenWave) {
            ctx.fillStyle = "rgba(16, 185, 129, 0.25)";
            ctx.beginPath();
            ctx.arc(px, py, 14, 0, Math.PI * 2);
            ctx.fill();
          }

          ctx.fillStyle = greenWave ? "#10B981" : isGreen ? "#22D3EE" : "#F59E0B";
          ctx.strokeStyle = "#0B0E14";
          ctx.lineWidth = 1.6;
          ctx.beginPath();
          ctx.arc(px, py, n.id === "Mukhani" ? 7.5 : onRoute ? 6.5 : 5.2, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = isDark ? "#E2E8F0" : "#0F172A";
          ctx.font = n.id === "Mukhani" ? "700 10.5px 'JetBrains Mono', monospace" : "600 9px 'JetBrains Mono', monospace";
          ctx.textAlign = "left";
          ctx.fillText(n.id.replace("_Jct", "").replace("_", " "), px + 9, py - 5);
        });

      // 5. Hospital Markers
      for (const h of HALDWANI_TOPOLOGY.landmarks.filter((l) => l.type === "hospital")) {
        const px = projX(h.x);
        const py = projY(h.y);
        const sel = h.id === st.selectedHospitalId;
        const sz = sel ? 12 : 8.5;
        ctx.fillStyle = "#F43F5E";
        ctx.strokeStyle = "#FFFFFF";
        ctx.lineWidth = sel ? 2 : 1;
        ctx.beginPath();
        ctx.roundRect(px - sz / 2, py - sz / 2, sz, sz, 2);
        ctx.fill();
        ctx.stroke();
      }

      // 6. Animated Ambulance Unit on Preemption
      if (ambPos) {
        ctx.save();
        ctx.shadowColor = "#F43F5E";
        ctx.shadowBlur = 14;
        ctx.fillStyle = "rgba(244, 63, 94, 0.3)";
        ctx.beginPath();
        ctx.arc(ambPos.x, ambPos.y, 13, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#FFFFFF";
        ctx.strokeStyle = "#F43F5E";
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.arc(ambPos.x, ambPos.y, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        ctx.restore();
      }

      rafId = requestAnimationFrame(draw);
    };

    rafId = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(rafId);
  }, [nodeMap]);

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const W = heroMode ? 960 : 740;
    const H = heroMode ? 540 : 420;
    const cx = ((e.clientX - rect.left) / rect.width) * W;
    const cy = ((e.clientY - rect.top) / rect.height) * H;
    const projX = (x: number) => ((x + 2150) / 4050) * (W - 70) + 35;
    const projY = (y: number) => (H - 35) - ((y + 2550) / 5100) * (H - 70);

    // Check if user clicked Mukhani node in heroMode to zoom into 10-lane duel
    const mukhani = nodeMap["Mukhani"];
    if (heroMode && onZoomMukhani && mukhani) {
      if (Math.hypot(cx - projX(mukhani.x), cy - projY(mukhani.y)) < 20) {
        onZoomMukhani();
        return;
      }
    }

    // Check nearest hospital within 18px
    for (const h of HALDWANI_TOPOLOGY.landmarks.filter((l) => l.type === "hospital")) {
      if (Math.hypot(cx - projX(h.x), cy - projY(h.y)) < 18) {
        selectHospital(h.id);
        return;
      }
    }
  };

  const handleCanvasMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const W = heroMode ? 960 : 740;
    const H = heroMode ? 540 : 420;
    const cx = ((e.clientX - rect.left) / rect.width) * W;
    const cy = ((e.clientY - rect.top) / rect.height) * H;
    const projX = (x: number) => ((x + 2150) / 4050) * (W - 70) + 35;
    const projY = (y: number) => (H - 35) - ((y + 2550) / 5100) * (H - 70);

    let found: string | null = null;
    for (const n of HALDWANI_TOPOLOGY.nodes.filter((x) => x.type === "traffic_light")) {
      if (Math.hypot(cx - projX(n.x), cy - projY(n.y)) < 16) {
        found = n.id;
        break;
      }
    }
    setHoveredTls(found);
  };

  return (
    <section className="grid grid-cols-1 gap-3 lg:grid-cols-12">
      <div
        className={`rounded-md border bg-card p-3.5 ${
          heroMode ? "border-blue-500/45 lg:col-span-9" : "border-border lg:col-span-8"
        }`}
      >
        <div className="mb-2.5 flex flex-wrap items-center justify-between gap-2">
          <div>
            <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-cyan-700 dark:text-cyan-400">
              {heroMode
                ? "LIVE CITY-WIDE TRAFFIC FLOW // HALDWANI ARTERIAL NETWORK (8 TLS · 60 EDGES)"
                : "City-Scale Topology · Kathgodam to Rampur / Bareilly Corridors"}
            </div>
            <div className="text-xs font-semibold text-foreground sm:text-sm">
              Haldwani Traffic Flow, Strategic Bypasses & Emergency Green-Wave Map
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {heroMode && onTogglePlay && (
              <Button
                size="sm"
                variant="default"
                onClick={onTogglePlay}
                className="font-mono text-[11px]"
              >
                {isPlaying ? (
                  <>
                    <Pause className="mr-1 h-3.5 w-3.5" /> PAUSE FLOW
                  </>
                ) : (
                  <>
                    <Play className="mr-1 h-3.5 w-3.5" /> PLAY FLOW
                  </>
                )}
              </Button>
            )}

            {heroMode && onZoomMukhani && (
              <Button
                size="sm"
                variant="outline"
                onClick={onZoomMukhani}
                className="font-mono text-[11px]"
              >
                <Maximize2 className="mr-1 h-3.5 w-3.5" /> ZOOM MUKHANI 10L
              </Button>
            )}

            <div className="w-60">
              <Select
                aria-label="Select Emergency Corridor"
                value={corridorKey}
                onChange={(e) => {
                  const k = e.target.value;
                  setCorridorKey(k);
                  setSelectedHospitalId(EMERGENCY_CORRIDORS[k].targetHospital);
                }}
              >
                {Object.entries(EMERGENCY_CORRIDORS).map(([key, spec]) => (
                  <option key={key} value={key}>
                    {spec.label}
                  </option>
                ))}
              </Select>
            </div>

            <button
              type="button"
              onClick={() => setShowShortcuts((s) => !s)}
              className={`cursor-pointer rounded border px-2.5 py-1.5 font-mono text-[10.5px] font-semibold ${
                showShortcuts
                  ? "border-emerald-500/40 bg-emerald-500/15 text-emerald-700 dark:text-emerald-400"
                  : "border-border bg-background text-muted-foreground"
              }`}
            >
              BYPASSES {showShortcuts ? "ON" : "OFF"}
            </button>
          </div>
        </div>

        <div className="relative">
          <canvas
            ref={canvasRef}
            onClick={handleCanvasClick}
            onMouseMove={handleCanvasMove}
            onMouseLeave={() => setHoveredTls(null)}
            className="block h-auto w-full cursor-pointer rounded-md border border-border"
            style={{ aspectRatio: heroMode ? "960 / 540" : "740 / 420" }}
          />
          {hoveredTls && nodeMap[hoveredTls] && (
            <div className="pointer-events-none absolute top-3 left-3 rounded border border-border bg-card/95 px-2.5 py-1 font-mono text-[10.5px] text-foreground shadow-sm">
              TLS: <strong>{hoveredTls}</strong> ({nodeMap[hoveredTls].x}m, {nodeMap[hoveredTls].y}m)
              {heroMode && hoveredTls === "Mukhani" ? " · Click to zoom into 10-lane duel" : ""}
            </div>
          )}
        </div>

        <div className="mt-2 flex flex-wrap items-center justify-between gap-2 font-mono text-[10.5px] text-muted-foreground">
          <div className="flex flex-wrap items-center gap-3">
            <span className="flex items-center gap-1">
              <span className="inline-block h-2 w-3 bg-blue-500" /> Kaladhungi SH-41
            </span>
            <span className="flex items-center gap-1">
              <span className="inline-block h-2 w-3 bg-cyan-500" /> Nainital NH-109
            </span>
            <span className="flex items-center gap-1">
              <span className="inline-block h-2 w-3 bg-emerald-500" /> Strategic Shortcuts
            </span>
            <span className="flex items-center gap-1">
              <span className="inline-block h-2.5 w-2.5 rounded-xs bg-rose-500" /> Hospitals (click to route)
            </span>
            {activeHour && (
              <span className="font-semibold text-foreground">
                Flow: {activeHour.flowVph} veh/hr ({activeHour.direction.toUpperCase()})
              </span>
            )}
          </div>
          <span className="flex items-center gap-1 font-semibold text-foreground">
            <Route className="h-3.5 w-3.5 text-emerald-600 dark:text-emerald-400" />
            {corridor.distanceLabel}
          </span>
        </div>
      </div>

      <div
        className={`flex flex-col rounded-md border border-border bg-card p-3.5 ${
          heroMode ? "lg:col-span-3" : "lg:col-span-4"
        }`}
      >
        <div className="mb-2 flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-foreground">
            <Hospital className="h-4 w-4 text-rose-600 dark:text-rose-400" />
            Trauma & Hospital Hubs ({hospitals.length})
          </div>
          {preemption && (
            <span className="inline-flex items-center gap-1 rounded bg-rose-500/15 px-2 py-0.5 font-mono text-[10px] font-semibold text-rose-700 dark:text-rose-300">
              <Ambulance className="h-3 w-3" /> SWEEPING
            </span>
          )}
        </div>

        <div className="relative mb-2.5">
          <Search className="pointer-events-none absolute top-2.5 left-2.5 h-3.5 w-3.5 text-muted-foreground" />
          <Input
            placeholder="Filter STH, Brijlal, Krishna..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-8"
          />
        </div>

        <div
          className="flex-1 space-y-1.5 overflow-y-auto pr-1"
          style={{ maxHeight: heroMode ? 480 : 375 }}
        >
          {hospitals.map((h) => {
            const active = h.id === selectedHospitalId;
            return (
              <button
                key={h.id}
                type="button"
                onClick={() => selectHospital(h.id)}
                className={`w-full cursor-pointer rounded border p-2 text-left transition-colors ${
                  active
                    ? "border-rose-500/50 bg-rose-500/10"
                    : "border-border bg-background hover:bg-secondary/60"
                }`}
              >
                <div className="flex items-center justify-between font-mono text-[10px]">
                  <span className="font-semibold text-rose-600 dark:text-rose-400">
                    {h.id}
                  </span>
                  <span className="tabular-nums text-muted-foreground">
                    ({h.x}m, {h.y}m)
                  </span>
                </div>
                <div className="mt-0.5 text-xs font-medium text-foreground">
                  {h.name}
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}
