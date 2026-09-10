# Derivatives Pricing and Greeks Dashboard

Black-Scholes and binomial pricer for NIFTY index options with Greeks heatmaps and delta-hedge backtests across equity (NIFTY) and FX (USDINR) underlyings.

## What it does
- Prices European call/put via **Black-Scholes** and **binomial tree (CRR)**
- Computes **Delta, Gamma, Vega, Theta** Greeks
- Runs a **delta-hedge backtest** on a synthetic price path for both NIFTY and USDINR
- Prints **Greeks heatmaps** (price vs strike vs vol)

## Run
```bash
pip install -r requirements.txt
python main.py
```

No external dependencies beyond Python stdlib (`math`, `random`).

## Inputs
All hard-coded at the top of `main.py`:
- NIFTY: spot=22500, strike=22500, T=0.25y, r=7%, vol=18%
- USDINR: spot=83.5, strike=84.0, T=0.10y, r=6%, vol=12%

## Note
Synthetic illustrative inputs only. Not connected to live market data.