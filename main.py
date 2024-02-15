import pandas as pd
import yfinance as yf
import customtkinter as ctk
import plotly.graph_objects as graph
from prophet import model
from prophet.plot import plot_plotly, plot_components_plotly

pd.options.display.float_format = '${:,.2f}'.format #global float format