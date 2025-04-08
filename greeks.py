import math
from scipy.stats import norm
import scipy.stats as si

def calculate_delta(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return si.norm.cdf(d1)

def calculate_gamma(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return si.norm.pdf(d1) / (S * sigma * math.sqrt(T))

def calculate_theta(S, K, T, r, sigma, option_type='call'):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    term1 = - (S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T))

    if option_type == 'call':
        term2 = - r * K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        term2 = + r * K * math.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    theta = term1 + term2
    return theta / 365  # Daily theta

def calculate_vega(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    vega = S * norm.pdf(d1) * math.sqrt(T)
    return vega / 100 / 365  # Vega per 1% change in volatility, daily

def calculate_rho(S, K, T, r, sigma, option_type='call'):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        rho = K * T * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        rho = -K * T * math.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return rho / 100 / 365  # Rho per 1% change in interest rate, daily