import yfinance as yf
import numpy as np 
import scipy.stats as si
from scipy.optimize import brentq
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

# List to store implied volatility values
iv_values = []

def fetch_stock_data(ticker):
    # Get stock data with yfinance
    stock = yf.Ticker(ticker)

    # Spot price (S): Last close price
    current_price = stock.history(period='1d')['Close'].iloc[0]

    # Historical data for volatility calculation
    hist = stock.history(period='1y')

    # Calculate log returns
    hist['LogReturn'] = np.log(hist['Close'] / hist['Close'].shift(1))

    # Daily volatility * sqrt(252) for annualized volatility
    sigma = hist['LogReturn'].std() * np.sqrt(252)

    # Risk-free rate
    r = 0.05

    return current_price, r, sigma



def fetch_option_data(ticker):

    # Get stock data with yfinance
    stock = yf.Ticker(ticker)
    
    # Todays date (to calculate time to maturity)
    today = datetime.today().date()
    
    # Store options data
    options_data = []

    # Loops through expiration dates 
    for exp in stock.options:

        # Fetch call options
        calls = stock.option_chain(exp).calls

        # Calculates time to maturity
        exp_date = datetime.strptime(exp, "%Y-%m-%d").date()
        time_to_maturity = (exp_date - today).days

        # Stores sstrike price, bid ask, and time to maturity
        for _, row in calls.iterrows():
            options_data.append({
                "Strike Price": row["strike"],
                "Bid": row["bid"],
                "Ask": row["ask"],
                "Time to Maturity (Days)": time_to_maturity,
                "Expiration Date": exp_date
            })

    # Return data frame
    return pd.DataFrame(options_data)



def black_scholes_calculation(S, K, T, r, sigma):
    # Black-Scholes formula for call option price
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * si.norm.cdf(d1, 0, 1) - K * np.exp(-r * T) * si.norm.cdf(d2, 0, 1)

    return call_price

def implied_volatility(S, K, T, r, market_price):
    # Uses Brent's method to find the implied volatility
    def bs_error(sigma):
        return black_scholes_calculation(S, K, T, r, sigma) - market_price
    
    try:
        return brentq(bs_error, 0.0001, 5)
    except ValueError:
        return None



def black_scholes_call(ticker, limit=250):
    # Loop through data and calculate the call price for each day
    # Done using previous two functions to get relevant data and applying the Black-Scholes formula
    # Return a dataframe with relevant data

    # Get strike price and time to maturity dataframe
    data = fetch_option_data(ticker)
    data = data[data['Time to Maturity (Days)'] > 0].head(limit)

    # Loop through the data and calculate the call price
    call_prices = pd.DataFrame(columns=['Date', 'Call Price'])

    # Get stock data
    S, r, sigma = fetch_stock_data(ticker)
    
    for index, row in data.iterrows():
        K = row['Strike Price']
        T = row['Time to Maturity (Days)'] / 365
        market_price = (row['Bid'] + row['Ask']) / 2  # Midpoint of bid-ask
        exp_date = row['Expiration Date']

        sigma = max(sigma, 1e-8)
        call_price_hist = black_scholes_calculation(S, K, T, r, sigma)
        iv = implied_volatility(S, K, T, r, market_price)

        iv_values.append(iv)

        call_price_iv = black_scholes_calculation(S, K, T, r, iv) if iv else None

        call_prices = call_prices._append({"Date": exp_date, 
                                           "Strike": K, 
                                           "Market Price": market_price,
                                           "Call Price (Hist Model)": call_price_hist,
                                           "Call Price (IV)": call_price_iv,
                                           "Bid": row['Bid'],
                                           "Ask": row['Ask'],
                                           "Implied Volatility": iv},
                                           ignore_index=True)

    call_prices.to_csv("black_scholes_prices.csv", index=False)
    return call_prices

def plot_volatility_3d(strike_prices, days_to_maturity, volatilities):
    
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create a grid for interpolation
    strike_grid, days_grid = np.meshgrid(
        np.linspace(min(strike_prices), max(strike_prices), 50),
        np.linspace(min(days_to_maturity), max(days_to_maturity), 50)
    )
    
    # Interpolate volatility values
    vol_grid = griddata((strike_prices, days_to_maturity), volatilities, (strike_grid, days_grid), method='cubic')
    
    # Plot surface
    surf = ax.plot_surface(strike_grid, days_grid, vol_grid, cmap='viridis', edgecolor='none')
    
    # Labels and title
    ax.set_xlabel('Strike Price')
    ax.set_ylabel('Days to Maturity')
    ax.set_zlabel('Volatility')
    ax.set_title('3D Volatility Surface')
    
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    plt.show()

# Test this with a European stock that doesn't pay dividends
test_call_prices = black_scholes_call('^XSP')

# Gets plot data
plot_data = fetch_option_data('XSP')

strike_prices = np.array(plot_data["Strike Price"])
days_to_maturity = np.array(plot_data["Time to Maturity (Days)"])
iv_array = np.array(iv_values)

# Plots volalitity surface
plot_volatility_3d(strike_prices, days_to_maturity, iv_array)