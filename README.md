# Derivatives Pricing and Greeks Dashboard

NIFTY Options Pricer and Delta-Hedging Backtester — Python, VBA

Built Black-Scholes binomial pricer for equity index options with Greeks analytics and delta-hedge backtesting in Python & VBA.

## Features
- src/pricer.py — Black-Scholes price + Greeks (delta, gamma, vega, theta) with heatmap example
- src/backtest.py — delta-hedge backtest across equity (NIFTY) & FX underlyings (synthetic path)
- src/greeks.py — to be added for heatmap generation
- dashboard.xlsm — VBA dashboard placeholder (Greeks heatmaps, backtest chart) — to be added
- equirements.txt — 
umpy, pandas, matplotlib`n
## Run
``npython src/pricer.py
python src/backtest.py
``n
*Synthetic vol/rate, illustrative — extend with live NIFTY/FX data and VBA dashboard.*

