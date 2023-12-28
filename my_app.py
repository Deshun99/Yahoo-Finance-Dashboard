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
app = dash.Dash(external_stylesheets=[dbc.themes.LITERA])
app.title = "Stock Analysis Dashboard"
CONTENT_STYLE = {
    }

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
    html.H1(
        'Stock Analysis Dashboard',
        style={
            "text-align": "center",
            "margin-bottom": "25px",
            "font-family": "Calibiri",
            "color": "white",
            "padding-top": "20px"
        }
    ),

    # Two-column layout for dropdowns
    html.Div(
        [
            # Column for genre-dropdown
            html.Div(
                dcc.Dropdown(
                    id='genre-dropdown',
                    value=symbols,
                    clearable=False,
                    multi=True,
                    options=[{'label': x, 'value': x} for x in symbols],
                ),
                style={"width": "45%", "display": "inline-block", "vertical-align": "top"}
            ),
            
            # Column for sales-dropdown, period-dropdown, and date picker range
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(
                            id='sales-dropdown',
                            value='Open',
                            clearable=False,
                            options=[{'label': x, 'value': x} for x in sales_list],
                        ),
                        style={"width": "48%", "display": "inline-block", "margin-right": "4%", 'color': 'black'}  # Adjusted width and added right margin
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='period-dropdown',
                            value='1d',
                            clearable=False,
                            options=[{'label': x, 'value': x} for x in period_list],
                        ),
                        style={"width": "48%", "display": "inline-block", 'color': 'black'}  # Adjusted width
                    ),
                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        start_date_placeholder_text='Start Date',
                        end_date_placeholder_text='End Date',
                        first_day_of_week=0,
                        reopen_calendar_on_clear=True,
                        is_RTL=False,
                        clearable=True,
                        min_date_allowed=date(2000,1,1),
                        max_date_allowed=date.today(),
                        initial_visible_month=date(2022,1,1),
                        start_date=date(2023, 1, 1),
                        end_date=date.today(),
                        updatemode='singledate',
                        style={"width": "100%", "margin-top": "10px"}  # Added margin-top for spacing from the dropdowns
                    ),
                ],
                style={"width": "45%", "display": "inline-block", "vertical-align": "top"}
            ),
        ],
        style={'text-align': 'center', 'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px'}
    ),

    html.Div(
        style={'width': '90%', 'margin': '0 auto', 'margin-bottom': '10px', 'overflow': 'hidden'},
        children=[
            dcc.Loading(
                id="loading",
                type="circle", 
                children=[
                    html.Div(
                        dcc.Graph(id='my-bar', config={'displayModeBar': True, 'displaylogo': False}),
                        style={'width': '100%', 'margin': '0 auto', 'margin-bottom': '10px'}
                    ),
                    html.Div(
                        id='table-container_1',
                        style={'width': '100%', 'margin': '0 auto', 'margin-bottom': '10px', 'overflowX': 'auto'}
                    ),
                ]
            ),
        ]
    ),

    # YouTube Iframe
    html.Iframe(
        src="https://www.youtube.com/embed/fE2h3lGlOsk",
        style={
            "display": "block",
            "margin": "25px auto",
            "width": "560px",
            "height": "315px",
            "border": "none",
            "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.1)"
        }
    )
], style={'textAlign': 'center', 'width': '100%', 'max-width': '1200px', 'margin': '0 auto'})


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
    print("Dataframe head:", df.head())
    if len(genre_chosen) == 0:
        dfv_fltrd = df[df['Symbol'].isin(symbols)]
    else:
        dfv_fltrd = df[df['Symbol'].isin(genre_chosen)]

    dfv_fltrd.sort_values(by=['Symbol'])

    fig = px.line(dfv_fltrd, color='Symbol', x='Calendar Year', markers=True, y=sales_chosen, text=None,
                  template='ggplot2', width=1250, height=600)

    fig.update_layout(
        xaxis=dict(showgrid=False, showline=True, linecolor="#17202A", color='white'),
        yaxis=dict(showgrid=True, showline=True, linecolor="#17202A", gridcolor='#EAECEE',color='white'),
        font=dict(
            family="Montserrat",
            size=14,
            color='white',
        ),

        paper_bgcolor='black',
        plot_bgcolor='black',
        xaxis_title="Day/Month (Calendar Year)",
        width=1055,
        legend_font_size=19,
        legend=dict(itemsizing='trace'),)
    fig.update_traces(line=dict(width=4))

    df_reshaped = dfv_fltrd.pivot(index='Symbol', columns='Calendar Year', values=sales_chosen)
    df_reshaped_2 = df_reshaped.reset_index()

    table = dash_table.DataTable(
    columns=[{"name": i, "id": i} for i in df_reshaped_2.columns],
    data=df_reshaped_2.to_dict('records'),
    export_format="csv",
    style_as_list_view=True,
    fill_width=True,
    style_cell={
        'font-size': '12px',
        'backgroundColor': '#D3D3D3', # light gray
        'color': 'black', # black text
    },
    style_table={
        'maxWidth': 1055,
        'backgroundColor': 'white', # white background
        'color': 'black', # black text
    },
    style_header={
        'backgroundColor': '#007BFF', # blue background
        'color': 'black', # white text
    },
    )

    return (fig, table)

#####################################################
# Part 6: Set up local server to show the dashboard
#####################################################
if __name__ == '__main__':
    app.run_server(debug=True, port=8008)