import pandas as pd
import yfinance as yf
import customtkinter as ctk
import plotly.graph_objects as graph
from datetime import datetime
from prophet import models
from prophet.plot import plot_plotly, plot_components_plotly

pd.options.display.float_format = '${:,.2f}'.format #global float format

# Get the data from Yahoo Finance
today = datetime.today().strftime('%Y-%m-%d')
start_date = '2016-01-01'
eth_df = yf.download('ETH-USD',start_date, today) 
eth_df.reset_index(inplace=True)
model_df = eth_df[['Date', 'Close']]
model_df.rename(columns={'Date':'ds', 'Close':'y'}, inplace=True)