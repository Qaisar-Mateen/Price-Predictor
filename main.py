import pandas as pd
import yfinance as yf
import dash
import plotly.graph_objects as graph
from datetime import datetime
from prophet import Prophet
from dash import dcc, html
from dash.dependencies import Input, Output

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

def BTC_data():
    # Get the data from Yahoo Finance
    today = datetime.today().strftime('%Y-%m-%d') 
    btc_df = get_yfinance_data('BTC-USD', '2010-01-01', today)

    # making data frame ready for the model
    btc_df.reset_index(inplace=True)
    model_df = btc_df[['Date', 'Open']]
    model_df.rename(columns={'Date':'ds', 'Open':'y'}, inplace=True)
    return model_df['ds'], model_df['y'], model_df

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': 'BTC', 'value': 'BTC-USD'}, {'label': 'ETH', 'value': 'ETH-USD'}],
        value='ETH-USD'
    ),
    dcc.Graph(id='graph')
])

xb, yb, model_btc = BTC_data()
xe, ye, model_eth = Eth_data()
mb = Prophet(seasonality_mode="multiplicative")
me = Prophet(seasonality_mode="multiplicative")
mb.fit(model_btc)
me.fit(model_eth)

futureb = mb.make_future_dataframe(periods = 365)
forecastb = mb.predict(futureb)

futuree = me.make_future_dataframe(periods = 365)
forecaste = me.predict(futuree)

today = datetime.today().strftime('%Y-%m-%d')

previous_trendb = forecastb[forecastb['ds'] < today]
future_trendb = forecastb[forecastb['ds'] >= today]

previous_trende = forecaste[forecaste['ds'] < today]
future_trende = forecaste[forecaste['ds'] >= today]


@app.callback(Output('graph', 'figure'), Input('dropdown', 'value'))
def build_graph(selectedValue):
    if selectedValue == 'BTC-USD':
        fig = graph.Figure(
            data=[
                graph.Scatter(x=[], y=[]),
                graph.Scatter(x=xb, y=yb, mode='lines', name='Actual Open Price', line=dict(color='blue')),
                graph.Scatter(
                    x=previous_trendb['ds'], 
                    y=(previous_trendb['yhat']+previous_trendb['yhat_upper'])/2, 
                    name='Previous Prediction',
                    line=dict(color='red')
                )
            ],
            frames=[graph.Frame(
                data=[graph.Scatter(
                        x=future_trendb['ds'].iloc[:i],
                        y=(future_trendb['yhat'].iloc[:i]+future_trendb['yhat_upper'].iloc[:i])/2,
                        mode='lines',
                        name='Future Predicted Trend',
                        line=dict(color='red')
                    )
                ]
            ) for i in range(0, len(future_trendb), 15)],
            layout=graph.Layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        buttons=[
                            dict(
                                label="Predict Trend",
                                method="animate",
                                args=[None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]
                            )
                        ]
                    )
                ]
            )
        )
    else:
        fig = graph.Figure(
            data=[
                graph.Scatter(x=[], y=[]),
                graph.Scatter(x=xe, y=ye, mode='lines', name='Actual Open Price', line=dict(color='blue')),
                graph.Scatter(
                    x=previous_trende['ds'], 
                    y=(previous_trende['yhat']+previous_trende['yhat_upper'])/2, 
                    name='Previous Prediction',
                    line=dict(color='red')
                )
            ],
            frames=[graph.Frame(
                data=[graph.Scatter(
                        x=future_trende['ds'].iloc[:i],
                        y=(future_trende['yhat'].iloc[:i]+future_trende['yhat_upper'].iloc[:i])/2,
                        mode='lines',
                        name='Future Predicted Trend',
                        line=dict(color='red')
                    )
                ]
            ) for i in range(0, len(future_trende), 15)],
            layout=graph.Layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        buttons=[
                            dict(
                                label="Predict Trend",
                                method="animate",
                                args=[None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]
                            )
                        ]
                    )
                ]
            )
        )

    # Set title
    fig.update_layout(
        title_text="Trend Prediction of Ethereum" if selectedValue == 'ETH-USD' else "Trend Prediction of Bitcoin", 
        xaxis_title="Date", 
        yaxis_title="Price (USD)"
    )

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
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)