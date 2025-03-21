import yfinance as yf
import numpy as np 
import scipy.stats as si
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.graph_objects as go
from datetime import datetime



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

    # Strike Price
    K = 340

    # Time to Maturity
    T = 7


    return current_price, K, T, r, sigma



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

        # Stores strike price and time to maturity
        for strike in calls["strike"]:
            options_data.append({"Strike Price": strike, "Time to Maturity (Days)": time_to_maturity})

    # Return data frame
    return pd.DataFrame(options_data)



def black_scholes_calculation(S, K, T, r, sigma):
    # Black-Scholes formula for call option price
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * si.norm.cdf(d1, 0, 1) - K * np.exp(-r * T) * si.norm.cdf(d2, 0, 1)

    return call_price



def black_scholes_call(ticker):
    # Going to loop through data and calculate the call price for each day
    # Done using previous two functions to get relevant data and applying the Black-Scholes formula
    # Return a dataframe with the date and the call price

    # Get strike price and time to maturity dataframe
    data = fetch_option_data(ticker)

    data = data[data['Time to Maturity (Days)'] > 0]

    # Loop through the data and calculate the call price
    call_prices = pd.DataFrame(columns=['Date', 'Call Price'])
    for index, row in data.iterrows():
        K = row['Strike Price']
        T = row['Time to Maturity (Days)'] / 365
        S, K, T, r, sigma = fetch_stock_data(ticker)
        if sigma == 0:
            sigma = 1e-8
        call_price = black_scholes_calculation(S, K, T, r, sigma)
        call_prices = call_prices._append({'Date': datetime.today().date(), 'Call Price': call_price}, ignore_index=True)

    return call_prices



# Test this with a European stock that doesn't pay dividends
test_call_prices = black_scholes_call('^XSP')
print(test_call_prices)