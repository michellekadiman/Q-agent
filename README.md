# NewsSentimentAlpha

Daily long/short equal-weight equity portfolio ranked by a financial-media
news-tone z-score signal (GDELT), rebalanced daily across a 10-stock
universe. **This scaffold ships a known-good equal-weight, long-only
baseline** — the ranked long/short signal is not implemented yet (see
`docs/strategy.md`).

## Quick Start

```bash
# Activate environment
cd ~/Documents/Q-agent
source venv/bin/activate
cd MyProjects

# Local backtest (WRDS/CRSP daily data, already configured in lean.json)
lean backtest "NewsSentimentAlpha"

# Local research environment
lean research "NewsSentimentAlpha"
```

Cloud commands (optional, not required for local development):

```bash
lean cloud push --project "NewsSentimentAlpha" --force
lean cloud backtest "NewsSentimentAlpha" --name "Test"
```

## Documentation

- **Project Overview**: [claude.md](claude.md)
- **Architecture**: [docs/architecture.md](docs/architecture.md)
- **Strategy Logic**: [docs/strategy.md](docs/strategy.md)
- **ObjectStore Schema**: [docs/objectstore.md](docs/objectstore.md)
- **Agent Instructions**: [AGENTS.md](AGENTS.md)

## Project Structure

```
NewsSentimentAlpha/
├── main.py          # Algorithm entry point (baseline: equal-weight long-only)
├── models/          # Alpha, portfolio, execution, logging
├── domain/          # Business logic, DTOs, config (universe, dates, cash)
├── data/            # Bundled per-project CSV — sentiment_panel.csv (TODO, added by parent session)
├── docs/            # Documentation
├── research/         # Marimo research notebooks (empty for now)
└── Manually_Backtested_Results/  # Drop QC-website backtest downloads here for offline analysis
```

## Strategy Overview

| Aspect | Description |
|--------|-------------|
| Type | Cross-sectional long/short, news-tone signal (target); equal-weight long-only (current baseline) |
| Asset Class | US Equities |
| Universe | GS, AAPL, JPM, BA, HD, IBM, VZ, V, NKE, CSCO |
| Rebalance | Daily |
| Backtest Window | 2017-01-01 to 2021-12-31 |

## Data Sources

| Source | Status |
|--------|--------|
| WRDS/CRSP daily equity prices | Local, ready — `infrastructure/pipelines/wrds/lean-data/equity/usa/daily/{ticker}.zip` |
| GDELT financial-media news-tone z-score panel | **TODO** — parent session adds `data/sentiment_panel.csv` |

## ObjectStore Outputs

| File | Description |
|------|-------------|
| `news_sentiment_alpha/daily_snapshots.csv` | Daily portfolio metrics |
| `news_sentiment_alpha/positions.csv` | Position data |
| `news_sentiment_alpha/trades.csv` | Trade history |

## Contributing

See [AGENTS.md](AGENTS.md) for guidelines on making changes to this project.
