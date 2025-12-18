# FamPay Data Engineering Intern Assignment

## Overview
- Transforms daily OHLC stock data into monthly summaries per ticker.
- Computes technical indicators on monthly closes: `SMA 10`, `SMA 20`, `EMA 10`, `EMA 20`.
- Writes 10 CSV files following `result_{SYMBOL}.csv` naming, each with 24 rows.

## Practical Assumptions
- Input path is fixed to `"/Users/milindranjan/Downloads/FamPay/output_file.csv"`.
- Months may have missing trading days; the first/last available trading day in a month is used for `Open`/`Close`.
- Monthly `date` represents the month-end timestamp.
- Indicators are based strictly on monthly `close` values.
- SMA returns `NaN` until a full window is available; EMA seeds at the `N`th month using SMA of the first `N` months, then applies the standard recursive EMA with `alpha = 2/(N+1)`.

## Monthly Aggregation Logic
- `Open`: price on the first trading day of the month.
- `Close`: price on the last trading day of the month.
- `High`: maximum price within the month.
- `Low`: minimum price within the month.

## Code Structure
- `load_data`: reads and sorts the input CSV.
- `aggregate_monthly`: builds monthly OHLC per ticker using snapshot logic (`first`/`last`) and extrema (`max`/`min`).
- `sma`, `ema`: indicator calculations implemented with Pandas rolling and ewm (no third‑party TA libs).
- `add_indicators`: attaches SMA/EMA columns to monthly data per ticker.
- `write_symbol_files`: partitions monthly data into 10 CSVs with 24 rows each.
- `main`: orchestrates the pipeline end‑to‑end.

## How to Run
```bash
python3 -m venv .venv
./.venv/bin/pip install pandas
./.venv/bin/python monthly_indicators.py
```

## Outputs
- Created in `results/`:
  - `result_AAPL.csv`, `result_AMD.csv`, `result_AMZN.csv`, `result_AVGO.csv`, `result_CSCO.csv`, `result_MSFT.csv`, `result_NFLX.csv`, `result_PEP.csv`, `result_TMUS.csv`, `result_TSLA.csv`.
- Each file contains exactly 24 data rows (plus header).
