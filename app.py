import dash
from dash import dcc 
from dash import html
from datetime import datetime as dt
from dash.dependencies import Input, Output, State

# Creating a Dash instance
# path = ['/Users/kshitijvaidya/Desktop/VirtualEnvironment/Stock_Dashboard_Visualisation/styles.css']
app = dash.Dash(__name__)
server = app.server


# This is the schematic of the layout of the application. 
# This takes in the stock ticker from the user 
app.layout = html.Div(
    [
        html.Div(
          [
            html.H1(children="Welcome to the Stock Dash App!", id='title-message', className='text-success'),
            html.P(children="Enter the Stock Code:", id='enter-code-message', className='bg-light'),
            html.Div([
              # stock code input
              dcc.Input(id='stock-code-input', type='text', placeholder='Enter Stock Code'),
              html.Button('Submit', id='submit')
            ]),

            html.Div([
              # Date range picker input
              dcc.DatePickerRange(
                  id='date-picker-range',
                  start_date = '2020-01-01',
                  end_date='2023-12-31',
                  display_format='DD-MM-YYYY',
                  persistence=True,
                  persistence_type='local',
              )
            ]),
            html.Div([
              # Stock price button
              html.Button('Stock Price', id='stock-price-button'),
              # Indicators button
              html.Button('Indicators', id='indicator-button'),
              # Number of days of forecast input
              dcc.Input(id='number-of-days-input', type='text', placeholder='Number of Days'),
              # Forecast button
              html.Button('Forecast', id='forecast-button'),
            ]),
          ],
        className="header"),

        html.Div(
          [
            html.Div(
                  [  
                      html.Img(id='company-logo'),
                      # To add the Company Name and Logo
                      html.H2(id='company-name'),
                      html.P(id='company-description')
                  ],
                id='logo-company-name'),
            html.Div([
                dcc.Graph(id='stock-price-graph'),
            ], id="graphs-content"),
            html.Div([
                # Indicator plot
                dcc.Graph(id='indicator-graph'),
            ], id="main-content"),
            html.Div([
                dcc.Graph(id='forecast-graph')
                # Forecast plot
            ], id="forecast-content")
          ],
        className="content")
    ],
    className='container',
)
    

# Define callback functions and app logic (if any) here
import yfinance as yf
import plotly.express as px
import matplotlib.pyplot as plt

# Callback function to fetch the company's information
@app.callback(
    [
        Output('company-logo', 'src'),
        Output('company-name', 'children'),
        Output('company-description', 'children')
    ],
    Input('submit', 'n_clicks'),
    State('stock-code-input', 'value')
)
def Company_Info(n_clicks, stock_code):
    if n_clicks:
        try:
            ticker = yf.Ticker(stock_code)
            info = ticker.info
            return info.get('logo_url', ''), info.get('shortName', ''), info.get('longBusinessSummary', '')
        except Exception as e:
            print(f"Error fetching company info: {e}")
    return '','',''


# Callback to fetch the stock price graph
@app.callback(
    Output('stock-price-graph', 'figure'),
    [
        Input('stock-price-button', 'n_clicks')
    ],
    [
        State('stock-code-input', 'value'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date')
    ]
)
def StockPriceGraph(n_clicks, stock_code, start_date, end_date):
    if n_clicks:
        try:
            Data = yf.download(stock_code, end=end_date)
            Data.reset_index(inplace=True)
            Fig = plt.plot(Data['Date'], Data['Close'], linestyle='-', label='Closing Prices')
            return Fig
        except Exception as e:
            print(f"Error fetching stock price data: {e}")
        return {}
    


# Function to get the EMA graph
def Get_EMA(data):
    data['EWA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
    Fig = px.scatter(data, x='Date', y='EWA_20', title='Estimated Moving Average vs Date')
    Fig.update_traces(mode='lines')
    return Fig


# Callback functions for the Indicator Graph
@app.callback(
    Output('indicator-graph', 'figure'),
    [
        Input('indicator-button', 'n_clicks')
    ],
    [
        State('stock-code-input', 'value'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date')
    ]
)
def IndicatorGraph(n_clicks, stock_code, start_date, end_date):
    if n_clicks:
        try:
            Data = yf.download(stock_code, start=start_date, end=end_date)
            Data.reset_index(inplace=True)
            Fig = Get_EMA(Data)
            return Fig
        except Exception as e:
            print(f"Error fetching Indicator Data: {e}")
        return {}
    

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)




