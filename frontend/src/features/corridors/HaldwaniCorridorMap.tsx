import * as React from "react";
import { Ambulance, Hospital, Route, Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { EMERGENCY_CORRIDORS, HALDWANI_TOPOLOGY } from "@/data/telemetry";

interface HaldwaniCorridorMapProps {
  preemption: boolean;
}

export function HaldwaniCorridorMap({ preemption }: HaldwaniCorridorMapProps) {
  const [corridorKey, setCorridorKey] = React.useState("sth_rampur");
  const [showShortcuts, setShowShortcuts] = React.useState(true);
  const [query, setQuery] = React.useState("");
  const [selectedHospitalId, setSelectedHospitalId] = React.useState<string>("HOSP_STH");

  const nodeMap = React.useMemo(
    () => Object.fromEntries(HALDWANI_TOPOLOGY.nodes.map((n) => [n.id, n])),
    [],
  );

  // Project Haldwani meter coordinates (X: -2100..1850, Y: -2550..2500) into SVG (740x430)
  const projX = (x: number) => ((x + 2150) / 4050) * 690 + 25;
  const projY = (y: number) => 405 - ((y + 2550) / 5100) * 380;

  const corridor = EMERGENCY_CORRIDORS[corridorKey];
  const routePoints = corridor.routeNodes
    .map((id) => nodeMap[id])
    .filter(Boolean)
    .map((n) => `${projX(n.x).toFixed(1)},${projY(n.y).toFixed(1)}`)
    .join(" ");

  const hospitals = HALDWANI_TOPOLOGY.landmarks.filter(
    (l) =>
      l.type === "hospital" &&
      `${l.id} ${l.name}`.toLowerCase().includes(query.trim().toLowerCase()),
  );

  const edgeStroke = (cat: string) => {
    if (cat === "kaladhungi") return "#3B82F6";
    if (cat === "nainital") return "#06B6D4";
    if (cat === "rampur") return "#64748B";
    if (cat === "shortcut") return "#10B981";
    return "#F43F5E";
  };

  return (
    <section className="grid grid-cols-1 gap-3 lg:grid-cols-12">
      <div className="rounded-md border border-border bg-card p-3.5 lg:col-span-8">
        <div className="mb-2.5 flex flex-wrap items-center justify-between gap-2">
          <div>
            <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-cyan-700 dark:text-cyan-400">
              City-Scale Topology · Kathgodam to Rampur / Bareilly Corridors
            </div>
            <div className="text-xs font-semibold text-foreground">
              Haldwani Signalized Junctions, Shortcuts & Emergency Green-Wave Map
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <div className="w-64">
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

        <svg
          viewBox="0 0 740 430"
          className="w-full rounded-md border border-border"
          style={{ backgroundColor: "var(--twin-canvas)" }}
        >
          {/* Road Edges */}
          {HALDWANI_TOPOLOGY.edges.map((edge) => {
            if (edge.category === "shortcut" && !showShortcuts) return null;
            const n1 = nodeMap[edge.from];
            const n2 = nodeMap[edge.to];
            if (!n1 || !n2) return null;
            return (
              <line
                key={edge.id}
                x1={projX(n1.x)}
                y1={projY(n1.y)}
                x2={projX(n2.x)}
                y2={projY(n2.y)}
                stroke={edgeStroke(edge.category)}
                strokeWidth={edge.category === "shortcut" || edge.category === "gully" ? 1.6 : 2.6}
                strokeDasharray={edge.category === "shortcut" ? "5 4" : undefined}
                strokeOpacity={0.72}
              />
            );
          })}

          {/* Highlighted Emergency Green-Wave Corridor */}
          {routePoints && (
            <polyline
              points={routePoints}
              fill="none"
              stroke={preemption ? "#F43F5E" : "#10B981"}
              strokeWidth={preemption ? 4.2 : 3.2}
              strokeDasharray={preemption ? "8 4" : undefined}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          )}

          {/* Traffic Light Junctions */}
          {HALDWANI_TOPOLOGY.nodes
            .filter((n) => n.type === "traffic_light")
            .map((n) => {
              const onRoute = corridor.routeNodes.includes(n.id);
              return (
                <g key={n.id}>
                  <circle
                    cx={projX(n.x)}
                    cy={projY(n.y)}
                    r={onRoute ? 6.5 : 5}
                    fill={onRoute ? (preemption ? "#F43F5E" : "#10B981") : "#06B6D4"}
                    stroke="#0B0E14"
                    strokeWidth={1.5}
                  />
                  <text
                    x={projX(n.x) + 8}
                    y={projY(n.y) - 6}
                    fill="var(--twin-label)"
                    fontSize={9}
                    fontWeight={600}
                    fontFamily="JetBrains Mono, monospace"
                  >
                    {n.id.replace("_Jct", "").replace("_", " ")}
                  </text>
                </g>
              );
            })}

          {/* Hospital Markers */}
          {HALDWANI_TOPOLOGY.landmarks
            .filter((l) => l.type === "hospital")
            .map((h) => {
              const selected = h.id === selectedHospitalId;
              return (
                <g
                  key={h.id}
                  onClick={() => setSelectedHospitalId(h.id)}
                  className="cursor-pointer"
                >
                  <rect
                    x={projX(h.x) - (selected ? 6 : 4.5)}
                    y={projY(h.y) - (selected ? 6 : 4.5)}
                    width={selected ? 12 : 9}
                    height={selected ? 12 : 9}
                    rx={2}
                    fill="#F43F5E"
                    stroke="#FFFFFF"
                    strokeWidth={selected ? 1.6 : 1}
                  />
                </g>
              );
            })}
        </svg>

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
              <span className="inline-block h-2.5 w-2.5 rounded-xs bg-rose-500" /> Trauma Centers
            </span>
          </div>
          <span className="flex items-center gap-1 font-semibold text-foreground">
            <Route className="h-3.5 w-3.5 text-emerald-600 dark:text-emerald-400" />
            {corridor.distanceLabel}
          </span>
        </div>
      </div>

      {/* Compact Hospital & Bypass Inspector */}
      <div className="flex flex-col rounded-md border border-border bg-card p-3.5 lg:col-span-4">
        <div className="mb-2 flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-foreground">
            <Hospital className="h-4 w-4 text-rose-600 dark:text-rose-400" />
            Trauma & Hospital Hubs ({hospitals.length})
          </div>
          {preemption && (
            <span className="inline-flex items-center gap-1 rounded bg-rose-500/15 px-2 py-0.5 font-mono text-[10px] font-semibold text-rose-700 dark:text-rose-300">
              <Ambulance className="h-3 w-3" /> PREEMPTING
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

        <div className="flex-1 space-y-1.5 overflow-y-auto pr-1" style={{ maxHeight: 375 }}>
          {hospitals.map((h) => {
            const active = h.id === selectedHospitalId;
            return (
              <button
                key={h.id}
                type="button"
                onClick={() => setSelectedHospitalId(h.id)}
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
