import yfinance as yf
import numpy as np 
import scipy.stats as si
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.graph_objects as go
from datetime import datetime


# ticker = yf.Ticker('AAPL')
# print(ticker)
# options_dates = ticker.options
# print(options_dates)
# options_data = ticker.option_chain(options_dates[0])
# print(options_data.calls.head())

def getOptionData(ticker):

    ticker = yf.Ticker(ticker)
    options_dates = ticker.options
    options_data = ticker.option_chain(options_dates[0])
    
    return options_data.calls, options_data.puts

aapl_calls, aapl_puts = getOptionData('AAPL')

