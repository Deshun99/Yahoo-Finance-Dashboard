#####################################################
# Part 1: Import needed packages
#####################################################
from datetime import date
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
import yfinance as yf

#####################################################
# Part 2: Basic app information
#####################################################
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Stock Analysis Dashboard"
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",}

#####################################################
# Part 3: Data information
#####################################################
symbols = ['D05.SI', 'U11.SI', 'O39.SI','Z74.SI', 'F34.SI', 'C38U.SI', 'C6L.SI', 'V03.SI', 'BN4.SI']
# ["AMZN", "TSLA", "MSFT", "AAPL", "GOOGL"]

sales_list = ["Open", "High", "Low", "Close","Adj Close", "Volume"]

period_list = ["1d", "5d", "1wk", "1mo"]

def get_stock_data(symbols, start_date, end_date, period):
    df = pd.DataFrame()
    for symbol in symbols:
        stock_data = yf.download(symbol, start=start_date, end=end_date, interval=period)
        stock_data["Symbol"] = symbol
        df = pd.concat([df, stock_data])
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df.rename(columns={"Date": "Calendar Year"}, inplace=True)
    return df

sales_list = ["Open", "High", "Low", "Close","Adj Close", "Volume"]

period_list = ["1d", "5d", "1wk", "1mo"]

#####################################################
# Part 4: App layout
#####################################################
app.layout = html.Div([

    html.H1('Stock Analysis Dashboard',style={"text-align": "center", "margin-bottom": "25px", "font-family":"Courier New"}),

    html.Iframe(
        src="https://www.youtube.com/embed/kqCdZK6V0t8", style={"display": "block", "margin": "25px auto", "width": "560px", "height": "315px"}
    ),

    html.Div([html.Div([
        html.Div(dcc.Dropdown(
            id='genre-dropdown', value= symbols, clearable=False, multi=True,
            options=[{'label': x, 'value': x} for x in symbols]
        ), className='six columns', style={"width": "70%"}, ),

        html.Div(dcc.Dropdown(
            id='sales-dropdown', value='Open', clearable=False,
            options=[{'label': x, 'value': x} for x in sales_list]
        ), className='six columns', style={"width": "15%"}, ),

        html.Div(dcc.Dropdown(
            id='period-dropdown', value='1m', clearable=False,
            options=[{'label': x, 'value': x} for x in period_list]
        ), className='six columns', style={"width": "15%"}, ),

        html.Div(dcc.DatePickerRange(
            id='my-date-picker-range',
            start_date_placeholder_text='Start Date',
            end_date_placeholder_text='End Date',
            first_day_of_week = 0,
            reopen_calendar_on_clear = True,
            is_RTL = False,
            clearable = True,
            min_date_allowed=date(2000,1,1),
            max_date_allowed=date.today(),
            initial_visible_month=date(2022,1,1),
            end_date=date.today(),
            updatemode='singledate',
        ), className='six columns', style={"width": "40%", "marginTop": "10px"}, ),

    
    ], className='row'), ], className='custom-dropdown'),

    

    html.Div([dcc.Graph(id='my-bar', figure={}, config={'displayModeBar': True, 'displaylogo': False,
                                                        'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d',
                                                                                   'zoomIn2d', 'zoomOut2d',
                                                                                   'resetScale2d']}), ],style={'width': '1250px'}),

    html.Div(html.Div(id='table-container_1'), style={'marginBottom': '15px', 'marginTop': '0px', 'width': '1000px'}),], style=CONTENT_STYLE)

    

#####################################################
# Part 5: Callback to update the chart and table
#####################################################
@app.callback(
    [Output(component_id='my-bar', component_property='figure'), Output('table-container_1', 'children')],
    [Input(component_id='genre-dropdown', component_property='value'),
     Input(component_id='sales-dropdown', component_property='value'),
     Input(component_id='period-dropdown', component_property='value'),
     Input(component_id='my-date-picker-range', component_property='start_date'),
     Input(component_id='my-date-picker-range', component_property='end_date')
    ]
)

def display_value(genre_chosen, sales_chosen, period_chosen, start_date, end_date):
    
    df = get_stock_data(symbols,start_date,end_date,period_chosen)
    
    if len(genre_chosen) == 0:
        dfv_fltrd = df[df['Symbol'].isin(symbols)]
    else:
        dfv_fltrd = df[df['Symbol'].isin(genre_chosen)]

    dfv_fltrd.sort_values(by=['Symbol'])

    fig = px.line(dfv_fltrd, color='Symbol', x='Calendar Year', markers=True, y=sales_chosen, text=None,
                  template='ggplot2', width=1250, height=600)

    fig.update_layout(
        xaxis=dict(showgrid=False, showline=True, linecolor="#17202A"),
        yaxis=dict(showgrid=True, showline=True, linecolor="#17202A", gridcolor='#EAECEE'),
        font=dict(
            family="Times New Roman",
            size=14,
        ),

        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis_title="Day/Month (Calendar Year)",
        width=1055,
        legend_font_size=19,
        legend=dict(itemsizing='trace'),)
    fig.update_traces(line=dict(width=4))

    df_reshaped = dfv_fltrd.pivot(index='Symbol', columns='Calendar Year', values=sales_chosen)
    df_reshaped_2 = df_reshaped.reset_index()


    return (fig,
            dash_table.DataTable(columns=[{"name": i, "id": i} for i in df_reshaped_2.columns],
                                 data=df_reshaped_2.to_dict('records'),
                                 export_format="csv",
                                 style_as_list_view=True,
                                 fill_width=True,
                                 style_cell={'font-size': '12px'},
                                 style_table={'maxWidth': 1055},
                                 style_header={'backgroundColor': 'black',
                                               'color': 'white', },
                                 style_data_conditional=[
                                     {
                                         'if': {
                                             'row_index': 'even',
                                             'filter': 'row_index >num(2)',
                                         },
                                         'backgroundColor': '#EBEDEF'
                                     }, ]
                                 ),
)

#####################################################
# Part 6: Set up local server to show the dashboard
#####################################################
if __name__ == '__main__':
    app.run_server(debug=False, port=8008)