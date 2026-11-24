import { Ambulance, Cpu, Moon, Sun, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import { NETWORK_PROFILES } from "@/data/telemetry";
import type { NetworkId, ThemeMode } from "@/types/telemetry";

export type DemoPresetId = "custom" | "loop_failure" | "morning_ppo" | "sth_emergency";
export type PageViewId = "operations" | "team";

interface TopCommandBarProps {
  pageView: PageViewId;
  onSelectPage: (page: PageViewId) => void;
  theme: ThemeMode;
  onToggleTheme: () => void;
  networkId: NetworkId;
  onSelectNetwork: (id: NetworkId) => void;
  selectedHour: number;
  onSelectHour: (hour: number) => void;
  activePreset: DemoPresetId;
  onApplyPreset: (preset: DemoPresetId) => void;
  preemption: boolean;
  onTogglePreemption: () => void;
  specsOpen: boolean;
  onToggleSpecs: () => void;
}

const SCENARIO_PRESETS = [
  { hour: 9, label: "Morning Peak (09:00)" },
  { hour: 18, label: "Evening Peak (18:00)" },
  { hour: 13, label: "Midday Flow (13:00)" },
  { hour: 3, label: "Night Lull (03:00)" },
];

export function TopCommandBar({
  pageView,
  onSelectPage,
  theme,
  onToggleTheme,
  networkId,
  onSelectNetwork,
  selectedHour,
  onSelectHour,
  activePreset,
  onApplyPreset,
  preemption,
  onTogglePreemption,
  specsOpen,
  onToggleSpecs,
}: TopCommandBarProps) {
  return (
    <header className="sticky top-2 z-30 flex flex-wrap items-center justify-between gap-2.5 rounded-md border border-border bg-card/95 px-3.5 py-2 backdrop-blur-md shadow-xs dark:shadow-none">
      <div className="flex flex-wrap items-center gap-2.5">
        <div className="flex items-center gap-2">
          <div className="h-6 w-1.5 rounded-xs bg-gradient-to-b from-emerald-500 to-blue-600" />
          <div>
            <div className="text-xs font-bold tracking-wider text-foreground sm:text-sm">
              INTELLIFLOW
            </div>
            <div className="font-mono text-[10px] text-muted-foreground">
              Team #54 · Adaptive Traffic Control
            </div>
          </div>
        </div>

        {/* Page View Switcher: Operations vs Team Contributions */}
        <div className="inline-flex rounded-md border border-border bg-background p-0.5">
          <button
            type="button"
            onClick={() => onSelectPage("operations")}
            className={`cursor-pointer rounded px-2.5 py-1 font-mono text-[10.5px] font-semibold transition-colors ${
              pageView === "operations"
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            OPERATIONS
          </button>
          <button
            type="button"
            onClick={() => onSelectPage("team")}
            className={`inline-flex cursor-pointer items-center gap-1 rounded px-2.5 py-1 font-mono text-[10.5px] font-semibold transition-colors ${
              pageView === "team"
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Users className="h-3 w-3" /> TEAM #54 WORK
          </button>
        </div>

        {pageView === "operations" && (
          <div className="inline-flex rounded-md border border-border bg-background p-0.5">
            {(Object.keys(NETWORK_PROFILES) as NetworkId[]).map((nid) => {
              const net = NETWORK_PROFILES[nid];
              const active = nid === networkId;
              return (
                <button
                  key={nid}
                  type="button"
                  onClick={() => onSelectNetwork(nid)}
                  className={`cursor-pointer rounded px-2.5 py-1 font-mono text-[10.5px] font-semibold transition-colors ${
                    active
                      ? "bg-secondary text-foreground ring-1 ring-border"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {net.shortName}
                </button>
              );
            })}
          </div>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {pageView === "operations" && (
          <>
            <div className="w-40">
              <Select
                aria-label="1-Click Viva Preset"
                value={activePreset}
                onChange={(e) => onApplyPreset(e.target.value as DemoPresetId)}
              >
                <option value="custom">Demo: Custom</option>
                <option value="loop_failure">1. Loop Failure</option>
                <option value="morning_ppo">2. Morning PPO</option>
                <option value="sth_emergency">3. STH Wave</option>
              </Select>
            </div>

            <div className="w-36">
              <Select
                aria-label="Diurnal Traffic Scenario"
                value={String(selectedHour)}
                onChange={(e) => onSelectHour(Number(e.target.value))}
              >
                {!SCENARIO_PRESETS.some((p) => p.hour === selectedHour) && (
                  <option value={String(selectedHour)}>
                    {String(selectedHour).padStart(2, "0")}:00 IST
                  </option>
                )}
                {SCENARIO_PRESETS.map((p) => (
                  <option key={p.hour} value={String(p.hour)}>
                    {p.label}
                  </option>
                ))}
              </Select>
            </div>

            <Button
              size="sm"
              variant={preemption ? "destructive" : "outline"}
              onClick={onTogglePreemption}
              className="font-mono text-[11px]"
            >
              <Ambulance className="mr-1.5 h-3.5 w-3.5" />
              {preemption ? "CLEAR STH" : "DISPATCH STH"}
            </Button>

            <Button
              size="sm"
              variant={specsOpen ? "secondary" : "outline"}
              onClick={onToggleSpecs}
              className="font-mono text-[11px]"
            >
              <Cpu className="mr-1.5 h-3.5 w-3.5" />
              SPECS
            </Button>
          </>
        )}

        <Button
          size="sm"
          variant="outline"
          onClick={onToggleTheme}
          aria-label="Toggle Light/Dark Mode"
          className="gap-1.5 font-mono text-[11px]"
        >
          {theme === "dark" ? (
            <>
              <Sun className="h-3.5 w-3.5 text-amber-400" />
              LIGHT
            </>
          ) : (
            <>
              <Moon className="h-3.5 w-3.5 text-blue-600" />
              DARK
            </>
          )}
        </Button>
      </div>
    </header>
  );
}
