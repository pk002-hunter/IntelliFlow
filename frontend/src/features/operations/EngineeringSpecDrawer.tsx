import { Cpu, Download, EyeOff, ShieldCheck, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  CONTROLLER_BENCHMARKS,
  MODEL_CHECKPOINTS,
  NETWORK_PROFILES,
} from "@/data/telemetry";
import type { ModelCheckpointId, NetworkId } from "@/types/telemetry";

interface EngineeringSpecDrawerProps {
  open: boolean;
  onClose: () => void;
  networkId: NetworkId;
  modelId: ModelCheckpointId;
}

export function EngineeringSpecDrawer({
  open,
  onClose,
  networkId,
  modelId,
}: EngineeringSpecDrawerProps) {
  if (!open) return null;

  const net = NETWORK_PROFILES[networkId];
  const model = MODEL_CHECKPOINTS[modelId];

  const handleExportReport = () => {
    const payload = {
      project: "IntelliFlow Adaptive Traffic Signal Control",
      exportedAt: new Date().toISOString(),
      activeNetwork: net,
      activeCheckpoint: model,
      empiricalBenchmarks: CONTROLLER_BENCHMARKS,
      statisticalTests: {
        mannWhitneyU: 822.5,
        mannWhitneyPValue: 5.778e-21,
        welchTStat: -7.14,
        welchPValue: 7.27e-8,
      },
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `intelliflow_report_${net.id}_${model.id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="rounded-md border border-blue-500/40 bg-card p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2 border-b border-border pb-2.5">
        <div className="flex items-center gap-2 font-mono text-xs font-semibold uppercase tracking-wider text-blue-700 dark:text-blue-400">
          <Cpu className="h-4 w-4" />
          Under-the-Hood Engineering Spec & Phase 2 Roadmap
        </div>
        <div className="flex items-center gap-2">
          <Button
            size="sm"
            variant="outline"
            onClick={handleExportReport}
            className="h-7 gap-1.5 font-mono text-[10.5px]"
          >
            <Download className="h-3.5 w-3.5" />
            EXPORT JSON REPORT
          </Button>
          <Button size="sm" variant="ghost" onClick={onClose} className="h-7 px-2">
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
        <div className="rounded border border-border bg-background p-3">
          <div className="font-mono text-[10px] font-semibold uppercase text-muted-foreground">
            MDP State & Reward (sumo_env.py)
          </div>
          <div className="mt-1.5 space-y-1 text-xs text-foreground">
            <div>
              <strong>Network Config:</strong>{" "}
              <code className="font-mono text-[11px] text-cyan-700 dark:text-cyan-400">
                {net.configPath}
              </code>
            </div>
            <div>
              <strong>Model Artifact:</strong>{" "}
              <code className="font-mono text-[11px] text-cyan-700 dark:text-cyan-400">
                {model.artifactPath}
              </code>
            </div>
            <div>
              <strong>State Vector:</strong> {net.obsDim} normalized in{" "}
              <code className="font-mono text-[11px]">[0, 1]</code> (queues, speed, wait, density, 1-hot phase, dwell)
            </div>
          </div>
        </div>

        <div className="rounded border border-border bg-background p-3">
          <div className="flex items-center gap-1.5 font-mono text-[10px] font-semibold uppercase text-emerald-600 dark:text-emerald-400">
            <ShieldCheck className="h-3.5 w-3.5" />
            3-Tier Safety Interlock Matrix
          </div>
          <ul className="mt-1.5 space-y-1 text-xs text-muted-foreground">
            <li>• Tier 1: Hard 5s minimum green + mandatory 3s yellow clearance</li>
            <li>• Tier 2: Anti-starvation penalty past 120s wait threshold</li>
            <li>• Tier 3: 5.0x emergency ambulance delay penalty driving green waves</li>
          </ul>
        </div>

        <div className="rounded border border-l-2 border-border border-l-blue-600 bg-background p-3">
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-1.5 font-mono text-[10px] font-semibold uppercase text-blue-700 dark:text-blue-400">
              <EyeOff className="h-3.5 w-3.5" />
              Phase 2: Edge Vision / YOLO
            </span>
            <span className="rounded border border-blue-500/30 bg-blue-500/10 px-1.5 py-0.5 font-mono text-[9.5px] text-blue-700 dark:text-blue-300">
              DEFERRED
            </span>
          </div>
          <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">
            Physical CCTV RTSP detection via TensorRT YOLOv8 is reserved for Phase 2 hardware deployment; Phase 1 operates on Eclipse SUMO + TraCI.
          </p>
        </div>
      </div>
    </div>
  );
}
