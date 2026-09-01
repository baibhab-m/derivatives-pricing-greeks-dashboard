"""
Black-Scholes and binomial pricer for NIFTY index options with Greeks.
Synthetic — uses illustrative vol/rate, not live market data.
"""
import math

def bs_price(S, K, T, r, sigma, option="call"):
    d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    N = lambda x: 0.5*(1+math.erf(x/math.sqrt(2)))
    if option=="call":
        return S*N(d1) - K*math.exp(-r*T)*N(d2)
    else:
        return K*math.exp(-r*T)*N(-d2) - S*N(-d1)

def greeks(S,K,T,r,sigma):
    d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    from math import exp, sqrt, pi
    Nprime = exp(-0.5*d1**2)/sqrt(2*pi)
    delta = 0.5*(1+math.erf(d1/math.sqrt(2)))
    gamma = Nprime/(S*sigma*sqrt(T))
    vega = S*Nprime*sqrt(T)
    theta = -(S*Nprime*sigma)/(2*sqrt(T)) - r*K*exp(-r*T)*0.5*(1+math.erf((d1 - sigma*sqrt(T))/sqrt(2)))
    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta}

if __name__=="__main__":
    S=22500; K=22500; T=0.25; r=0.07; sigma=0.18
    print(f"Call: {bs_price(S,K,T,r,sigma,'call'):.2f}")
    print(greeks(S,K,T,r,sigma))
    # heatmap example
    for k in [22000,22500,23000]:
        print(k, bs_price(S,k,T,r,sigma))
