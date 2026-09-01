"""
Delta-hedge backtest across equity & FX underlyings (synthetic NIFTY path).
"""
import math, random
from pricer import bs_price, greeks

def simulate(S0=22500, mu=0.08, sigma=0.18, T=0.25, steps=60):
    dt=T/steps
    path=[S0]
    for _ in range(steps):
        path.append(path[-1]*math.exp((mu-0.5*sigma**2)*dt + sigma*math.sqrt(dt)*random.gauss(0,1)))
    return path

def delta_hedge_pnl(S0=22500, K=22500, T=0.25, r=0.07, sigma=0.18):
    path=simulate(S0, sigma=sigma, T=T)
    dt=T/len(path)
    # simple: hold delta,PnL
    pnl=0
    for i in range(len(path)-1):
        S=path[i]
        t=T - i*dt
        g=greeks(S,K,t,r,sigma)
        pnl+= g["delta"]*(path[i+1]-S)
    price=bs_price(S0,K,T,r,sigma)
    # illustrative PnL vs price
    print(f"Simulated PnL of delta hedge: {pnl:.2f} vs premium {price:.2f}")

if __name__=="__main__":
    delta_hedge_pnl()
    # FX underlying example
    delta_hedge_pnl(S0=83.5, K=84, T=0.1, r=0.06, sigma=0.12)
