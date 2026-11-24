# IntelliFlow Frontend (React + TypeScript + Tailwind v4)

Interactive **AI vs. Legacy Traffic Duel**, **Animated Haldwani City Traffic Flow Map**, **4-Controller Delay Race + 5-Axis Radar + BPR Stress-Tester**, **24h BPR Diurnal & Green AI Ledger**, and **Team #54 Individual Contributions Page** with Light & Dark mode support.

## Directory Layout

```text
src/
├── components/ui/      # Pure shadcn/ui primitives (button, card, input, label, select, tabs)
├── features/
│   ├── operations/     # TopCommandBar, TrafficDuelArena, 60fps MukhaniFlowCanvas, Specs
│   ├── benchmarks/     # ControllerRaceArena (delay race, 5-axis radar & BPR stress tester)
│   ├── corridors/      # HaldwaniCorridorMap (animated city traffic flow + Green-Wave routes)
│   ├── economics/      # DiurnalGreenSection (24h BPR wave + fuel/CO2 ledger)
│   └── team/           # TeamContributionsPage (Team #54 individual member work & viva Q&As)
├── data/               # Exported 360-step CSVs & Haldwani XML topology (telemetry.json + ts)
├── lib/                # Pure helpers (cn, traffic signal & fuel math)
├── types/              # Shared TypeScript interfaces
├── App.tsx             # Operations & Team #54 shell
└── index.css           # Light & Dark tokens + Tailwind v4 @custom-variant dark
```

## Commands

```bash
npm install
npm run dev
npm run build
```
