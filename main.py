import pandas as pd
import yfinance as yf
import customtkinter as ctk
import plotly.graph_objects as graph
from datetime import datetime
from prophet import models, Prophet
from prophet.plot import plot_plotly, plot_components_plotly

pd.options.display.float_format = '${:,.2f}'.format #global float format

# Get the data from Yahoo Finance
today = datetime.today().strftime('%Y-%m-%d')
start_date = '2016-01-01'
eth_df = yf.download('ETH-USD',start_date, today)

# making data frame ready for the model
eth_df.reset_index(inplace=True)
model_df = eth_df[['Date', 'Close']]
model_df.rename(columns={'Date':'ds', 'Close':'y'}, inplace=True)

# plot the open price

# x = model_df["ds"]
# y = model_df["y"]

# fig = graph.Figure()

# fig.add_trace(graph.Scatter(x=x, y=y))

# # Set title
# fig.update_layout(
#     title_text="Time series plot of Ethereum Open Price",
# )

# fig.update_layout(
#     xaxis=dict(
#         rangeselector=dict(
#             buttons=list(
#                 [
#                     dict(count=1, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(count=1, label="YTD", step="year", stepmode="todate"),
#                     dict(count=1, label="1y", step="year", stepmode="backward"),
#                     dict(step="all"),
#                 ]
#             )
#         ),
#         rangeslider=dict(visible=True),
#         type="date",
#     )
# )

m = Prophet(
    seasonality_mode="multiplicative",
)
m.fit(model_df)

future = m.make_future_dataframe(periods = 365)
future.tail()