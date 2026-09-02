# NewsSentimentAlpha - News-tone long/short equity strategy (baseline scaffold)

## Repository

- **GitHub URL:** (none — local-only standalone repo, no remote added)
- **Default Branch:** main

## Project Overview

Daily long/short equal-weight portfolio ranked by a financial-media
news-tone z-score signal per stock (GDELT), rebalanced daily. Top half of
the ranked 10-stock universe is long, bottom half is short.

**This scaffold implements only the baseline**: equal-weight, long-only,
buy-and-hold across the full universe. The ranked news-tone signal is not
wired in yet — see `AGENTS.md` § "Planned Work" for exactly what the
parent/user session will add on top of this.

## Project Structure

```
NewsSentimentAlpha/
├── main.py                  # Composition root (QCAlgorithm), daily scheduled rebalance
├── models/                  # Organisms (orchestrators)
│   ├── alpha.py             # EqualWeightAlpha — BASELINE (flat signal); TODO: news-tone z-score
│   ├── portfolio.py         # EqualWeightPortfolio — BASELINE (equal-weight long); TODO: long/short by rank
│   ├── execution.py         # MarketOrderExecutor — SetHoldings per target weight
│   └── logger.py            # ObjectStore logging
├── domain/                  # Molecules + Atoms
│   ├── config.py            # Universe, dates, cash, ObjectStore namespace, SENTIMENT_PANEL_CSV path
│   └── models.py            # DTOs, enums
├── data/                    # Bundled per-project CSV — sentiment_panel.csv added by parent session
├── docs/                    # Documentation
│   ├── architecture.md      # System architecture
│   ├── strategy.md          # Strategy logic (baseline + TODO for real signal)
│   └── objectstore.md       # Data schemas
├── research/                # Marimo notebooks (empty for now — .py, not .ipynb)
├── Manually_Backtested_Results/  # Drop QC-website backtest downloads here for qc-backtest-analyzer
├── config.json               # QC cloud config (DO NOT COMMIT, not required for local dev)
└── claude.md                 # This file
```

**Pattern**: direct `SetHoldings` from a scheduled `_rebalance` method (teaching
pattern), not the QC `AlphaModel`/`PortfolioConstructionModel` framework
lifecycle. See `AGENTS.md` § "Pattern Choice" and
`MyProjects/ElectionIndustryBeta/` as the worked example this mirrors.

## Data Sources

| Source | Local path | Status |
|--------|-----------|--------|
| WRDS/CRSP daily equity prices | `infrastructure/pipelines/wrds/lean-data/equity/usa/daily/{ticker}.zip` | Ready — used by this scaffold's `AddEquity` calls |
| GDELT financial-media news-tone z-score panel | `data/sentiment_panel.csv` (this project) | **TODO** — added by parent session, no extraction pipeline needed |

## Strategy Parameters (current baseline)

| Parameter | Value | Description |
|-----------|-------|--------------|
| Universe | GS, AAPL, JPM, BA, HD, IBM, VZ, V, NKE, CSCO | Static 10-stock list, `domain/config.py::UNIVERSE` |
| Rebalance | Daily, market open + 5 min | `main.py::Initialize` Schedule.On |
| Signal (baseline) | Flat (1.0 for every ticker) | `models/alpha.py::EqualWeightAlpha` — placeholder |
| Portfolio (baseline) | Equal-weight, long-only | `models/portfolio.py::EqualWeightPortfolio` — placeholder |

Once the real signal lands: rank by news-tone z-score, long top half /
short bottom half — see `docs/strategy.md`.

## LEAN CLI Commands

### Setup (Run Once Per Terminal Session)

```bash
cd ~/Documents/Q-agent
source venv/bin/activate
cd MyProjects
```

### Local Backtest (primary workflow for this project)

```bash
lean backtest "NewsSentimentAlpha"
```

`MyProjects/lean.json` `data-folder` is set to
`../infrastructure/pipelines/wrds/lean-data`, which already has zip/factor/map
files for all 10 universe tickers plus SPY. No cloud setup or `config.json`
is required for this to work.

### Local Research

```bash
lean research "NewsSentimentAlpha"
```

### Cloud (optional — not required for local development)

```bash
lean cloud push --project "NewsSentimentAlpha"
lean cloud backtest "NewsSentimentAlpha" --name "Description"
lean cloud pull --project "NewsSentimentAlpha"
```

`config.json` is created automatically on first `lean cloud push` — it does
not need to exist for local backtest/research.

## ObjectStore Data

### Files Created

| File | Description |
|------|-------------|
| `news_sentiment_alpha/daily_snapshots.csv` | Daily portfolio metrics |
| `news_sentiment_alpha/positions.csv` | Position-level data |
| `news_sentiment_alpha/trades.csv` | Trade executions |

See `docs/objectstore.md` for full schema documentation.

### Reading in Research Notebook

```python
from io import StringIO
import pandas as pd

snapshots_str = qb.ObjectStore.Read("news_sentiment_alpha/daily_snapshots.csv")
df = pd.read_csv(StringIO(snapshots_str), parse_dates=['date'])
```

## Backtest Configuration

| Setting | Value |
|---------|-------|
| Start Date | 2017-01-01 |
| End Date | 2021-12-31 |
| Starting Cash | $100,000 |
| Benchmark | SPY |

Window chosen for dense GDELT news-tone coverage (per parent session).

## Git Version Control

Standalone repo, initialized locally (`git init -b main`), no remote added.

### Files Tracked

- `main.py`, `models/*.py`, `domain/*.py`
- `data/*.csv` (bundled data — see workspace claude.md "Bundled Per-Project Data")
- Documentation (`docs/`, `claude.md`, `README.md`, `AGENTS.md`)
- `.gitignore`

### Files NOT Tracked

- `config.json` (contains QC organization/cloud IDs, not created yet)
- `backtests/` (regeneratable)
- `__pycache__/`

## Common Issues

### "lean: command not found"

```bash
source ~/Documents/Q-agent/venv/bin/activate
```

### "lean.json not found" / no data locally

`MyProjects/lean.json` already points at the WRDS lean-data folder for this
workspace. If it's missing entirely: `cd MyProjects && lean init`, then set
`data-folder` to `../infrastructure/pipelines/wrds/lean-data`.
