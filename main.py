import pandas as pd
import yfinance as yf
import customtkinter as ctk
import plotly.graph_objects as graph
from datetime import datetime
from prophet import models, Prophet
#from prophet.plot import plot_plotly, plot_components_plotly

pd.options.display.float_format = '${:,.2f}'.format #global float format

def get_yfinance_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def Eth_data():
    # Get the data from Yahoo Finance
    today = datetime.today().strftime('%Y-%m-%d') 
    eth_df = get_yfinance_data('ETH-USD', '2016-01-01', today)

    # making data frame ready for the model
    eth_df.reset_index(inplace=True)
    model_df = eth_df[['Date', 'Open']]
    model_df.rename(columns={'Date':'ds', 'Open':'y'}, inplace=True)
    return model_df['ds'], model_df['y'], model_df


if __name__ == "__main__":
    x, y, model = Eth_data()

    fig = graph.Figure()

    fig.add_trace(graph.Scatter(x=x, y=y, name='Actual Open Price'))

    # Set title
    fig.update_layout(title_text="Time series plot of Ethereum Open Price", xaxis_title="Date", yaxis_title="Price (USD)")

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
            buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="todate"),
                        dict(count=6, label="6m", step="month", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="todate"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    m = Prophet(
        seasonality_mode="multiplicative",
    )
    m.fit(model)

    future = m.make_future_dataframe(periods = 365)
    future.tail()
    forecast = m.predict(future)
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    #plot_plotly(m, forecast)

    fig.add_trace(graph.Scatter(x=forecast["ds"], y=(forecast["yhat"]+forecast['yhat_upper'])/2, name='Predicted Trend'))