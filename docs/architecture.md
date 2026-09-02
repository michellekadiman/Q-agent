# NewsSentimentAlpha - Architecture

## Overview

Daily long/short equal-weight portfolio ranked by a financial-media
news-tone z-score signal per stock, rebalanced daily. This scaffold
currently implements only an equal-weight, long-only baseline — see
`strategy.md` for what's implemented vs. planned.

## Atomic Structure

```
NewsSentimentAlpha/
├── main.py                  # COMPOSITION ROOT
│                            # QCAlgorithm facade, daily scheduled rebalance
│
├── models/                  # ORGANISMS
│   ├── alpha.py             # EqualWeightAlpha — signal generation (baseline placeholder)
│   ├── portfolio.py         # EqualWeightPortfolio — target-weight construction (baseline placeholder)
│   ├── execution.py         # MarketOrderExecutor — SetHoldings per target
│   └── logger.py            # PortfolioLogger — ObjectStore logging facade
│
├── domain/                  # MOLECULES + ATOMS
│   ├── config.py            # Universe, dates, cash, ObjectStore namespace (ATOMS)
│   └── models.py            # DTOs, enums, protocols (ATOMS)
│
├── data/                    # Bundled per-project CSV (sentiment_panel.csv — TODO)
│
└── docs/                    # Documentation
    ├── architecture.md      # This file
    ├── strategy.md          # Strategy logic details
    └── objectstore.md       # Data output schemas
```

## Layer Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPOSITION ROOT                          │
│                      (main.py)                               │
│         Can import: ALL layers                               │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                       ORGANISMS                              │
│                    (models/*.py)                             │
│         Can import: domain/, AlgorithmImports                │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   MOLECULES + ATOMS                          │
│                    (domain/*.py)                             │
│         Can import: Python stdlib only                       │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. Direct SetHoldings, not the QC AlphaModel framework

`models/{alpha,portfolio,execution}.py` are plain Python classes wired
directly from `main.py::_rebalance`, not `AlphaModel` /
`PortfolioConstructionModel` / `ExecutionModel` subclasses. This keeps the
signal → target → order pipeline explicit and easy to follow while the
real news-tone logic is still being built. See
`MyProjects/ElectionIndustryBeta/` for the pattern this mirrors.

### 2. Equal-weight baseline before the real signal

`models/alpha.py::EqualWeightAlpha` and `models/portfolio.py::EqualWeightPortfolio`
are intentionally trivial placeholders (flat signal → equal weight,
long-only). This gives a known-good local baseline that compiles and
backtests against WRDS/CRSP daily data before the news-tone ranking logic
is layered on top. `models/execution.py` does not need to change when the
real signal lands — it already applies whatever weight dict it's given,
including negative (short) weights.

## Data Flow

```
[Static Universe] → [Alpha Model] → [Portfolio Model] → [Execution Model]
                          ↓                  ↓                   ↓
                      Signals            Targets              Orders
                          ↓                  ↓                   ↓
                      [Logger] ←─────────────┴───────────────────┘
                          ↓
                    [ObjectStore]
```

## Module Responsibilities

| Module | Layer | Responsibility |
|--------|-------|----------------|
| `main.py` | Root | Wire models, schedule daily rebalance, handle order events |
| `models/alpha.py` | Organism | Generate trading signal (baseline: flat; target: news-tone z-score) |
| `models/portfolio.py` | Organism | Convert signal to target weights (baseline: equal-weight long; target: ranked long/short) |
| `models/execution.py` | Organism | Apply target weights via SetHoldings |
| `models/logger.py` | Organism | Persist data to ObjectStore |
| `domain/config.py` | Atom | Universe, dates, cash, namespace constants |
| `domain/models.py` | Atom | DTOs, enums, protocols |
