# IntelliFlow Frontend (React + TypeScript + Tailwind v4)

Interactive **AI vs. Legacy Traffic Duel**, **Haldwani Spatial Corridor Map**, **4-Controller Delay Race + 5-Axis Radar**, and **24h BPR Diurnal & Green AI Ledger** with Light & Dark mode support.

## Directory Layout

```text
src/
├── components/ui/      # Pure shadcn/ui primitives (button, card, input, label, select, tabs)
├── features/
│   ├── operations/     # TopCommandBar, TrafficDuelArena, 60fps MukhaniFlowCanvas, EngineeringSpecDrawer
│   ├── benchmarks/     # ControllerRaceArena (cumulative delay race + 5-axis SVG radar)
│   ├── corridors/      # HaldwaniCorridorMap (real SUMO coordinates + Green-Wave routes + hospitals)
│   └── economics/      # DiurnalGreenSection (24h Google Maps BPR wave + fuel/CO2 ledger)
├── data/               # Exported 360-step CSVs & Haldwani XML topology (telemetry.json + ts)
├── lib/                # Pure helpers (cn, traffic signal & fuel math)
├── types/              # Shared TypeScript interfaces
├── App.tsx             # 4-Act Operations & Viva Showcase shell
└── index.css           # Light & Dark tokens + Tailwind v4 @custom-variant dark
```

## Commands

```bash
npm install
npm run dev
npm run build
```
