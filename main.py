"""
Derivatives Pricing and Greeks Dashboard
Black-Scholes and binomial pricer for NIFTY index options with Greeks heatmaps
and delta-hedge backtests across equity (NIFTY) and FX (USDINR) underlyings.

Synthetic - all prices/paths are illustrative, not live market data.
"""

# Hard-coded inputs at the top so you can see/tweak them without diving into functions
NIFTY_SPOT = 22500
NIFTY_STRIKE = 22500
NIFTY_RATE = 0.07
NIFTY_VOL = 0.18
NIFTY_T = 0.25

USDINR_SPOT = 83.5
USDINR_STRIKE = 84.0
USDINR_RATE = 0.06
USDINR_VOL = 0.12
USDINR_T = 0.10

import math


# ---------- Black-Scholes pricer ----------
def bs_price(S, K, T, r, sigma, option="call"):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    if option == "call":
        return S * N(d1) - K * math.exp(-r * T) * N(d2)
    return K * math.exp(-r * T) * N(-d2) - S * N(-d1)


# ---------- Greeks (Delta, Gamma, Vega, Theta) ----------
def greeks(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    Nprime = math.exp(-0.5 * d1 ** 2) / math.sqrt(2 * math.pi)
    delta = N(d1)
    gamma = Nprime / (S * sigma * math.sqrt(T))
    vega = S * Nprime * math.sqrt(T)
    theta = -(S * Nprime * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * N(d2)
    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta}


# ---------- Binomial tree pricer (Cox-Ross-Rubinstein) ----------
def binomial_price(S, K, T, r, sigma, steps=100, option="call"):
    dt = T / steps
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)

    # build terminal prices
    prices = [S * (u ** (steps - i)) * (d ** i) for i in range(steps + 1)]
    # terminal payoff
    if option == "call":
        values = [max(px - K, 0) for px in prices]
    else:
        values = [max(K - px, 0) for px in prices]
    # backwards induction
    for _ in range(steps):
        values = [math.exp(-r * dt) * (p * values[i] + (1 - p) * values[i + 1]) for i in range(len(values) - 1)]
    return values[0]


# ---------- Delta-hedge backtest on a synthetic path ----------
def simulate_path(S0, mu, sigma, T, steps=60, seed=42):
    import random
    random.seed(seed)
    dt = T / steps
    path = [S0]
    for _ in range(steps):
        path.append(path[-1] * math.exp((mu - 0.5 * sigma ** 2) * dt + sigma * math.sqrt(dt) * random.gauss(0, 1)))
    return path


def delta_hedge_backtest(S0, K, T, r, sigma, label):
    path = simulate_path(S0, mu=0.08, sigma=sigma, T=T)
    dt = T / len(path)
    pnl = 0.0
    for i in range(len(path) - 1):
        S = path[i]
        t_remaining = T - i * dt
        g = greeks(S, K, t_remaining, r, sigma)
        pnl += g["delta"] * (path[i + 1] - S)
    premium = bs_price(S0, K, T, r, sigma)
    print(f"  [{label}] Simulated delta-hedge PnL: {pnl:.2f}  vs  option premium: {premium:.2f}")


# ---------- Greeks heatmap (price vs vol, across strikes) ----------
def greeks_heatmap(S, T, r, strikes, vols):
    print("\n  Delta heatmap (rows=strike, cols=vol):")
    print("  " + "strike".ljust(10) + " ".join(f"{v:>6.0%}" for v in vols))
    for K in strikes:
        row = [f"{K:<10.0f}"]
        for v in vols:
            row.append(f"{greeks(S, K, T, r, v)['delta']:>6.2f}")
        print("  " + " ".join(row))

    print("\n  Gamma heatmap (rows=strike, cols=vol):")
    print("  " + "strike".ljust(10) + " ".join(f"{v:>6.0%}" for v in vols))
    for K in strikes:
        row = [f"{K:<10.0f}"]
        for v in vols:
            row.append(f"{greeks(S, K, T, r, v)['gamma']:>6.4f}")
        print("  " + " ".join(row))


if __name__ == "__main__":
    print("=" * 60)
    print("NIFTY index option (synthetic)")
    print("=" * 60)
    print(f"  Spot={NIFTY_SPOT}  Strike={NIFTY_STRIKE}  T={NIFTY_T}y  r={NIFTY_RATE}  vol={NIFTY_VOL}")
    call_bs = bs_price(NIFTY_SPOT, NIFTY_STRIKE, NIFTY_T, NIFTY_RATE, NIFTY_VOL, "call")
    call_bin = binomial_price(NIFTY_SPOT, NIFTY_STRIKE, NIFTY_T, NIFTY_RATE, NIFTY_VOL, 100, "call")
    print(f"  BS call price: {call_bs:.2f}")
    print(f"  Binomial call price (100 steps): {call_bin:.2f}")
    print(f"  Greeks: {greeks(NIFTY_SPOT, NIFTY_STRIKE, NIFTY_T, NIFTY_RATE, NIFTY_VOL)}")

    print("\n" + "=" * 60)
    print("USDINR FX option (synthetic)")
    print("=" * 60)
    print(f"  Spot={USDINR_SPOT}  Strike={USDINR_STRIKE}  T={USDINR_T}y  r={USDINR_RATE}  vol={USDINR_VOL}")
    print(f"  BS call price: {bs_price(USDINR_SPOT, USDINR_STRIKE, USDINR_T, USDINR_RATE, USDINR_VOL, 'call'):.4f}")
    print(f"  Greeks: {greeks(USDINR_SPOT, USDINR_STRIKE, USDINR_T, USDINR_RATE, USDINR_VOL)}")

    print("\n" + "=" * 60)
    print("Delta-hedge backtest (NIFTY + USDINR)")
    print("=" * 60)
    delta_hedge_backtest(NIFTY_SPOT, NIFTY_STRIKE, NIFTY_T, NIFTY_RATE, NIFTY_VOL, "NIFTY")
    delta_hedge_backtest(USDINR_SPOT, USDINR_STRIKE, USDINR_T, USDINR_RATE, USDINR_VOL, "USDINR")

    print("\n" + "=" * 60)
    print("Greeks heatmap (NIFTY)")
    print("=" * 60)
    strikes = [22000, 22250, 22500, 22750, 23000]
    vols = [0.12, 0.15, 0.18, 0.21, 0.25]
    greeks_heatmap(NIFTY_SPOT, NIFTY_T, NIFTY_RATE, strikes, vols)