import pandas as pd
import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as graph
from datetime import datetime
from prophet import Prophet
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

def build_graph(selectedValue):
    if selectedValue == 'BTC-USD':
        x, y, model = BTC_data()
    else:
        x, y, model = Eth_data()

    m = Prophet(seasonality_mode="multiplicative")
    m.fit(model)

    future = m.make_future_dataframe(periods = 365)
    forecast = m.predict(future)
    today = datetime.today().strftime('%Y-%m-%d')

    previous_trend = forecast[forecast['ds'] < today]
    future_trend = forecast[forecast['ds'] >= today]
    fig = graph.Figure(
        data=[
            graph.Scatter(x=[], y=[]),
            graph.Scatter(x=x, y=y, mode='lines', name='Actual Open Price', line=dict(color='blue')),
            graph.Scatter(
                x=previous_trend['ds'], 
                y=(previous_trend['yhat']+previous_trend['yhat_upper'])/2, 
                name='Previous Prediction',
                line=dict(color='red')
            )
        ],
        frames=[graph.Frame(
            data=[graph.Scatter(
                    x=future_trend['ds'].iloc[:i],
                    y=(future_trend['yhat'].iloc[:i]+future_trend['yhat_upper'].iloc[:i])/2,
                    mode='lines',
                    name='Future Predicted Trend',
                    line=dict(color='red')
                )
            ]
        ) for i in range(0, len(future_trend), 15)],
        layout=graph.Layout(
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[
                        dict(
                            label="Predict Trend",
                            method="animate",
                            args=[None]
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
    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': 'BTC', 'value': 'BTC-USD'}, {'label': 'ETH', 'value': 'ETH-USD'}],
            value='ETH-USD'
        ),
        dcc.Graph(id='graph')
    ])
    app.callback(Output('graph', 'figure'), Input('dropdown', 'value'))

    app.run_server(debug=True)
   

    # # Add dropdown
    # fig.update_layout(
    #     updatemenus=[
    #         dict(
    #         buttons=list([
    #                 dict(
    #                     args=["type", "surface"],
    #                     label="ETH",
    #                     method="update"
    #                 ),
    #                 dict(
    #                     args=["type", "heatmap"],
    #                     label="BTC",
    #                     method="update"
    #                 )
    #             ]),
    #             direction="down",
    #             pad={"r": 10, "t": 10},
    #             showactive=True,
    #             x=1.0,
    #             xanchor="right",
    #             y=1.12,
    #             yanchor="top"
    #         ),
    #     ]
    # )
    

    fig.show()