import * as React from "react";
import { ControllerRaceArena } from "@/features/benchmarks";
import { HaldwaniCorridorMap } from "@/features/corridors";
import { DiurnalGreenSection } from "@/features/economics";
import {
  EngineeringSpecDrawer,
  TopCommandBar,
  TrafficDuelArena,
  type DemoPresetId,
  type PageViewId,
} from "@/features/operations";
import { TeamContributionsPage } from "@/features/team";
import { DIURNAL_BPR_HOURS, TELEMETRY_SERIES } from "@/data/telemetry";
import type {
  BaselineId,
  ModelCheckpointId,
  NetworkId,
  ThemeMode,
} from "@/types/telemetry";

export function App() {
  const [pageView, setPageView] = React.useState<PageViewId>("operations");
  const [theme, setTheme] = React.useState<ThemeMode>(() => {
    const saved = window.localStorage.getItem("intelliflow-theme");
    return saved === "light" ? "light" : "dark";
  });
  const [networkId, setNetworkId] = React.useState<NetworkId>("mukhani");
  const [baselineId, setBaselineId] = React.useState<BaselineId>("fixed");
  const [aiModelId, setAiModelId] =
    React.useState<ModelCheckpointId>("ppo_mukhani");
  const [selectedHour, setSelectedHour] = React.useState<number>(9);
  const [preemption, setPreemption] = React.useState<boolean>(false);
  const [specsOpen, setSpecsOpen] = React.useState<boolean>(false);
  const [stepIdx, setStepIdx] = React.useState<number>(8);
  const [isPlaying, setIsPlaying] = React.useState<boolean>(true);
  const [speedMultiplier, setSpeedMultiplier] = React.useState<number>(1);
  const [fullHorizon, setFullHorizon] = React.useState<boolean>(false);
  const [activePreset, setActivePreset] = React.useState<DemoPresetId>("custom");

  const applyDemoPreset = (preset: DemoPresetId) => {
    setActivePreset(preset);
    setPageView("operations");
    if (preset === "loop_failure") {
      setNetworkId("mukhani");
      setBaselineId("actuated");
      setAiModelId("ppo_mukhani");
      setSelectedHour(9);
      setPreemption(false);
      setFullHorizon(false);
      setStepIdx(21);
      setIsPlaying(false);
    } else if (preset === "morning_ppo") {
      setNetworkId("mukhani");
      setBaselineId("fixed");
      setAiModelId("ppo_mukhani");
      setSelectedHour(9);
      setPreemption(false);
      setFullHorizon(false);
      setStepIdx(8);
      setIsPlaying(true);
    } else if (preset === "sth_emergency") {
      setNetworkId("haldwani");
      setBaselineId("fixed");
      setAiModelId("ppo_colab");
      setSelectedHour(18);
      setPreemption(true);
      setFullHorizon(false);
      setStepIdx(12);
      setIsPlaying(true);
    }
  };

  React.useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
    window.localStorage.setItem("intelliflow-theme", theme);
  }, [theme]);

  React.useEffect(() => {
    if (!isPlaying) return;
    const maxLen = fullHorizon
      ? TELEMETRY_SERIES.mukhani_ppo.length
      : TELEMETRY_SERIES.fixed.length;
    const intervalMs = Math.max(180, Math.round(850 / speedMultiplier));
    const id = window.setInterval(() => {
      setStepIdx((prev) => (prev + 1) % maxLen);
    }, intervalMs);
    return () => window.clearInterval(id);
  }, [isPlaying, speedMultiplier, fullHorizon]);

  const handleSelectNetwork = (net: NetworkId) => {
    setNetworkId(net);
    if (aiModelId !== "dqn_final") {
      if (net === "single") setAiModelId("ppo_single");
      else if (net === "haldwani") setAiModelId("ppo_colab");
      else setAiModelId("ppo_mukhani");
    }
  };

  const handleToggleHorizon = () => {
    setFullHorizon((prev) => {
      const next = !prev;
      if (!next && stepIdx >= TELEMETRY_SERIES.fixed.length) {
        setStepIdx(TELEMETRY_SERIES.fixed.length - 1);
      }
      return next;
    });
  };

  const activeHour =
    DIURNAL_BPR_HOURS.find((h) => h.hour === selectedHour) ??
    DIURNAL_BPR_HOURS[9];

  const isHaldwaniHero = networkId === "haldwani";

  return (
    <div className="min-h-screen bg-background text-foreground transition-colors">
      <main className="mx-auto flex w-full max-w-7xl flex-col gap-4 px-4 py-4">
        <TopCommandBar
          pageView={pageView}
          onSelectPage={setPageView}
          theme={theme}
          onToggleTheme={() =>
            setTheme((prev) => (prev === "dark" ? "light" : "dark"))
          }
          networkId={networkId}
          onSelectNetwork={handleSelectNetwork}
          selectedHour={selectedHour}
          onSelectHour={setSelectedHour}
          activePreset={activePreset}
          onApplyPreset={applyDemoPreset}
          preemption={preemption}
          onTogglePreemption={() => setPreemption((prev) => !prev)}
          specsOpen={specsOpen}
          onToggleSpecs={() => setSpecsOpen((prev) => !prev)}
        />

        {pageView === "team" ? (
          <TeamContributionsPage />
        ) : (
          <>
            <EngineeringSpecDrawer
              open={specsOpen}
              onClose={() => setSpecsOpen(false)}
              networkId={networkId}
              modelId={aiModelId}
            />

            {preemption && (
              <div className="flex flex-wrap items-center justify-between gap-2 rounded-md border border-rose-500/50 bg-rose-500/10 px-3.5 py-2 text-xs">
                <span className="font-medium text-rose-900 dark:text-rose-100">
                  EMERGENCY PREEMPTION ACTIVE: Legacy baseline stalls in spillback while IntelliFlow locks EW Green &rarr; Rampur Rd (SH-49) &rarr; STH Hospital (0s delay)
                </span>
                <span className="rounded bg-rose-500/20 px-2 py-0.5 font-mono text-[10px] font-semibold text-rose-700 dark:text-rose-300">
                  3s YELLOW INTERLOCK ARMED
                </span>
              </div>
            )}

            {/* When Haldwani City is selected, promote the live animated city-wide traffic flow map to Hero */}
            {isHaldwaniHero && (
              <HaldwaniCorridorMap
                preemption={preemption}
                heroMode={true}
                theme={theme}
                activeHour={activeHour}
                isPlaying={isPlaying}
                onTogglePlay={() => setIsPlaying((p) => !p)}
                speedMultiplier={speedMultiplier}
                onZoomMukhani={() => handleSelectNetwork("mukhani")}
              />
            )}

            {/* Split-Screen AI vs. Legacy Traffic Duel */}
            <TrafficDuelArena
              networkId={networkId}
              baselineId={baselineId}
              onSelectBaseline={setBaselineId}
              aiModelId={aiModelId}
              onSelectAiModel={setAiModelId}
              stepIdx={stepIdx}
              onChangeStep={(idx) => {
                setIsPlaying(false);
                setStepIdx(idx);
              }}
              isPlaying={isPlaying}
              onTogglePlay={() => setIsPlaying((p) => !p)}
              onReset={() => {
                setIsPlaying(false);
                setStepIdx(0);
              }}
              speedMultiplier={speedMultiplier}
              onChangeSpeed={setSpeedMultiplier}
              fullHorizon={fullHorizon}
              onToggleHorizon={handleToggleHorizon}
              preemption={preemption}
              theme={theme}
              activeHour={activeHour}
            />

            {/* Empirical Delay Race & 5-Axis Radar / BPR Stress Curve */}
            <ControllerRaceArena
              stepIdx={stepIdx}
              baselineId={baselineId}
              aiModelId={aiModelId}
            />

            {/* Show Haldwani Corridor Map below when viewing junction-level networks */}
            {!isHaldwaniHero && (
              <HaldwaniCorridorMap
                preemption={preemption}
                heroMode={false}
                theme={theme}
                activeHour={activeHour}
                isPlaying={isPlaying}
                speedMultiplier={speedMultiplier}
              />
            )}

            {/* 24-Hour Google Maps BPR Wave & Green AI Impact Ledger */}
            <DiurnalGreenSection
              selectedHour={selectedHour}
              onSelectHour={setSelectedHour}
            />
          </>
        )}
      </main>
    </div>
  );
}

export default App;
