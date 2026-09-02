# NewsSentimentAlpha - Agent Instructions

This file defines project-specific instructions for AI agents working on this strategy.

For workspace-level guidelines, see `~/Documents/Q-agent/AGENTS.md`.

## Project Summary

- **Strategy**: Daily long/short equal-weight portfolio ranked by a
  financial-media news-tone z-score signal per stock (GDELT), top half of
  the ranked universe long / bottom half short, rebalanced daily across a
  10-stock universe (GS, AAPL, JPM, BA, HD, IBM, VZ, V, NKE, CSCO).
- **Current state**: BASELINE SCAFFOLD ONLY. The news-tone ranking is not
  implemented — `main.py` currently holds the full universe equal-weight,
  long-only (see `models/alpha.py` and `models/portfolio.py` TODOs). This
  exists to prove the project compiles and backtests locally before the
  real signal is layered in.
- **Architecture**: Atomic Structure (Composition Root → Organisms → Molecules → Atoms)
- **Entry Point**: `main.py` (`NewsSentimentAlphaAlgorithm`)

## Planned Work (owned by the parent/user session, not this bootstrap)

The parent session will add, on top of this scaffold:

1. `data/sentiment_panel.csv` — bundled GDELT financial-media news-tone
   z-score panel (date, ticker, z-score columns). No extraction pipeline
   exists for this in the workspace; it is supplied directly.
2. Expanded `domain/config.py` — additional signal parameters (lookback,
   long/short split, etc.) alongside the universe/date constants already
   present.
3. Real `models/alpha.py::compute_signals` — reads the sentiment panel,
   returns a per-ticker z-score for the current rebalance date instead of
   the flat placeholder signal.
4. Real `models/portfolio.py::to_targets` — ranks tickers by z-score, goes
   long the top half and short the bottom half (see TODOs already in both
   files for the exact hand-off shape expected).

Until that lands, treat `main.py`'s equal-weight behavior as the source of
truth for "does the project work," not as the intended strategy.

## Architecture

```
main.py              # Composition Root - wires models together, scheduled daily rebalance
├── models/          # Organisms - domain orchestrators
│   ├── alpha.py     # Signal generation (BASELINE: flat signal; TODO: news-tone z-score)
│   ├── portfolio.py # Portfolio construction (BASELINE: equal-weight long; TODO: long/short by z-score rank)
│   ├── execution.py # Order execution (SetHoldings — no change needed for the real signal)
│   └── logger.py    # ObjectStore logging
├── domain/          # Molecules + Atoms - pure business logic
│   ├── config.py    # Universe, dates, cash, ObjectStore namespace, SENTIMENT_PANEL_CSV path
│   └── models.py    # DTOs, enums (ATOMS)
├── data/            # Bundled per-project CSV — sentiment_panel.csv goes here (parent session)
└── research/        # Marimo notebooks (empty for now)
```

## Pattern Choice — Direct SetHoldings (teaching pattern)

This project uses the **teaching pattern**: `models/{alpha,portfolio,execution}.py`
are plain Python classes, not QC `AlphaModel`/`PortfolioConstructionModel`/
`ExecutionModel` subclasses. `main.py::_rebalance` (scheduled daily) calls
`alpha.compute_signals()` → `portfolio.to_targets(...)` → `executor.execute(...)`
→ `SetHoldings(...)` directly. This mirrors `MyProjects/ElectionIndustryBeta/`
and keeps the wiring obvious while the signal itself is being built out.

If this strategy later needs the full QC alpha-streaming/insight lifecycle
(e.g. to combine with other alpha models via `SetAlpha`), that's a deliberate
architecture change — ask before converting.

## Strategy Invariants

These rules must NOT change without explicit approval:

1. Universe is a static 10-stock list (GS, AAPL, JPM, BA, HD, IBM, VZ, V, NKE, CSCO) — no dynamic universe selection.
2. Rebalance is daily, scheduled at market open + 5 minutes.
3. Data sources are WRDS/CRSP daily equity prices (local) and the bundled GDELT news-tone CSV — no live API calls at runtime.

## ObjectStore Keys

Keep these keys stable unless migration is explicitly requested:

- `news_sentiment_alpha/daily_snapshots.csv`
- `news_sentiment_alpha/positions.csv`
- `news_sentiment_alpha/trades.csv`

## Development Workflow

```bash
cd ~/Documents/Q-agent
source venv/bin/activate
cd MyProjects
lean backtest "NewsSentimentAlpha"
lean research "NewsSentimentAlpha"
```

Cloud is optional for this project (not required for local development):

```bash
lean cloud push --project "NewsSentimentAlpha" --force
lean cloud backtest "NewsSentimentAlpha" --name "Description"
```

## Validation

Before handing off code changes:

```bash
python -m py_compile main.py models/*.py domain/*.py
```

Then run a local backtest (or cloud, if requested).

## Scope Guidance

- **Safe**: Changes within a single layer that don't affect trading behavior
- **Ask First**: Cross-layer changes, strategy parameter changes (universe, dates, rebalance cadence), ObjectStore schema changes
- **Prohibited**: Changes to `config.json`, violating layer dependencies

## Layer Rules

| Layer | Can Import From |
|-------|-----------------|
| `domain/` | Python stdlib only |
| `models/` | `domain/`, `AlgorithmImports` |
| `main.py` | All layers |

Never import from a higher layer (e.g., `domain/` importing from `models/`).
