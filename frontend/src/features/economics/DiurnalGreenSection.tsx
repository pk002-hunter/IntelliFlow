import * as React from "react";
import { Fuel } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { DIURNAL_BPR_HOURS, FLEET_COMPOSITION } from "@/data/telemetry";
import { computeGreenAiSavings } from "@/lib/traffic";

interface DiurnalGreenSectionProps {
  selectedHour: number;
  onSelectHour: (hour: number) => void;
}

export function DiurnalGreenSection({
  selectedHour,
  onSelectHour,
}: DiurnalGreenSectionProps) {
  const [dailyVehicles, setDailyVehicles] = React.useState(32000);
  const [fuelPriceInr, setFuelPriceInr] = React.useState(96);
  const [idleSavedSec, setIdleSavedSec] = React.useState(22);

  const activeHourSpec =
    DIURNAL_BPR_HOURS.find((h) => h.hour === selectedHour) ?? DIURNAL_BPR_HOURS[9];
  const { annualSavingsCr, annualCo2Tonnes, litersSavedPerDay } =
    computeGreenAiSavings(dailyVehicles, fuelPriceInr, idleSavedSec);

  const maxFlow = 2700;

  return (
    <section className="grid grid-cols-1 gap-3 lg:grid-cols-12">
      {/* 24h Diurnal Google Maps BPR Wave */}
      <div className="rounded-md border border-border bg-card p-3.5 lg:col-span-7">
        <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
          <div>
            <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-cyan-700 dark:text-cyan-400">
              24-Hour Google Maps Probe Ingestion (BPR Formulation)
            </div>
            <div className="text-xs font-semibold text-foreground">
              Click any hour bar to test diurnal surge & directional split
            </div>
          </div>
          <span className="rounded border border-border bg-secondary px-2 py-0.5 font-mono text-[11px] font-semibold tabular-nums text-foreground">
            {activeHourSpec.timeLabel} · {activeHourSpec.flowVph} veh/hr ({activeHourSpec.delayRatio.toFixed(2)}x)
          </span>
        </div>

        <div className="mt-3 flex h-32 items-end gap-1 rounded-md border border-border bg-background px-2.5 pt-4 pb-2">
          {DIURNAL_BPR_HOURS.map((h) => {
            const pct = Math.max(8, Math.round((h.flowVph / maxFlow) * 100));
            const isSelected = h.hour === selectedHour;
            const isPeak = h.delayRatio >= 2.3;
            return (
              <button
                key={h.hour}
                type="button"
                title={`${h.timeLabel}: ${h.flowVph} veh/hr — ${h.description}`}
                onClick={() => onSelectHour(h.hour)}
                className="group flex h-full flex-1 cursor-pointer flex-col items-center justify-end gap-1"
              >
                <div
                  className={`w-full rounded-t-[2px] transition-all ${
                    isSelected
                      ? "bg-blue-600 ring-2 ring-blue-500/40"
                      : isPeak
                        ? "bg-amber-500/80 group-hover:bg-amber-500"
                        : "bg-cyan-500/50 group-hover:bg-cyan-500"
                  }`}
                  style={{ height: `${pct}%` }}
                />
                <span className="font-mono text-[8.5px] tabular-nums text-muted-foreground">
                  {h.hour % 3 === 0 ? h.hour : ""}
                </span>
              </button>
            );
          })}
        </div>

        <div className="mt-2.5 flex flex-wrap items-center justify-between gap-2 text-xs">
          <span className="font-medium text-foreground">
            {activeHourSpec.description}
          </span>
          <span className="font-mono text-[11px] uppercase text-muted-foreground">
            Dominant Split: {activeHourSpec.direction}
          </span>
        </div>

        {/* Indian Mixed-Traffic Fleet Strip */}
        <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
          {FLEET_COMPOSITION.map((f) => (
            <div
              key={f.id}
              className="rounded border border-border bg-background px-2.5 py-1.5"
            >
              <div className="flex items-center justify-between font-mono text-[10px]">
                <span className="text-muted-foreground">{f.label}</span>
                <span
                  className="inline-block h-2 w-2 rounded-full"
                  style={{ backgroundColor: f.color }}
                />
              </div>
              <div className="mt-0.5 font-mono text-xs font-bold tabular-nums text-foreground">
                {f.sharePct}% · {f.pcu} PCU
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Green AI & Commuter Fuel Ledger */}
      <div className="rounded-md border border-border bg-card p-3.5 lg:col-span-5">
        <div className="mb-3 flex items-center gap-2">
          <Fuel className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
          <div>
            <div className="text-xs font-semibold text-foreground">
              Green AI & Commuter Fuel Ledger
            </div>
            <div className="text-[11px] text-muted-foreground">
              Haldwani arterial corridor idling reduction model
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-2">
          <div className="space-y-1">
            <Label htmlFor="vol">Daily Veh</Label>
            <Input
              id="vol"
              type="number"
              value={dailyVehicles}
              onChange={(e) => setDailyVehicles(Number(e.target.value) || 0)}
            />
          </div>
          <div className="space-y-1">
            <Label htmlFor="fuel">Fuel ₹/L</Label>
            <Input
              id="fuel"
              type="number"
              value={fuelPriceInr}
              onChange={(e) => setFuelPriceInr(Number(e.target.value) || 0)}
            />
          </div>
          <div className="space-y-1">
            <Label htmlFor="idle">Saved Idle (s)</Label>
            <Input
              id="idle"
              type="number"
              value={idleSavedSec}
              onChange={(e) => setIdleSavedSec(Number(e.target.value) || 0)}
            />
          </div>
        </div>

        <div className="mt-3 grid grid-cols-2 gap-2.5">
          <div className="rounded-md border border-border bg-background p-3">
            <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
              Annual Fuel Saved
            </div>
            <div className="mt-1 font-mono text-xl font-bold tabular-nums text-emerald-600 dark:text-emerald-400">
              ₹{annualSavingsCr.toFixed(2)} Cr
            </div>
            <div className="font-mono text-[10px] text-muted-foreground">
              {Math.round(litersSavedPerDay)} L/day saved
            </div>
          </div>

          <div className="rounded-md border border-border bg-background p-3">
            <div className="font-mono text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
              Annual CO2 Abated
            </div>
            <div className="mt-1 font-mono text-xl font-bold tabular-nums text-cyan-700 dark:text-cyan-400">
              {annualCo2Tonnes.toFixed(1)} t
            </div>
            <div className="font-mono text-[10px] text-muted-foreground">
              HBEFA3 baseline 16.34 kg/hr
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
