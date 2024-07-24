import dash
from dash import dash_table
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output, State
from app import app
from data.data_loader import df

# Define the layout of the homepage
layout = html.Div(
    style={'backgroundColor': '#FFFFFF', 'height': '100vh', 'fontFamily': 'Arial'},
    children=[
        # Master Header Container
        html.Div(
            style={
                'backgroundColor': '#FFFFFF',
                'padding': '20px',
                'height': '5%',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'left'
            },
            children=[
                html.H1(
                    children='Retail inventory optimizer web application',
                    style={'margin': '0', 'fontFamily': 'Arial'}
                )
            ]
        ),
        
        # Column Renaming Inputs Container
        html.Div(
            style={
                'backgroundColor': '#E1E6FF',
                'padding': '10px',
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'space-around'
            },
            children=[
                html.Div(
                    style={'margin': '10px'},
                    children=[
                        html.Label(f'{col} '),
                        dcc.Input(id=f'input-{col}', type='text', value=col)
                    ]
                ) for col in df.columns
            ]
        ),
        
        html.Div(
            style={'backgroundColor': '#E1E6FF', 'textAlign': 'center', 'padding': '10px'},
            children=[
                html.Button('Rename', id='rename-button', n_clicks=0)
            ]
        ),

        # Table Container
        html.Div(
            style={
                'backgroundColor': '#FFFFFF',
                'padding': '20px',
                'height': '70%',
                'overflow': 'auto',
                'fontFamily': 'Arial'
            },
            children=[
                dash_table.DataTable(
                    id='data-table',
                    columns=[{'name': col, 'id': col} for col in df.columns],
                    data=df.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '5px',
                        'fontFamily': 'Arial'
                    },
                    style_header={
                        'fontWeight': 'bold',
                        'backgroundColor': '#284BFA',
                        'color': '#FFFFFF',
                        'fontFamily': 'Arial'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#E1E6FF'
                        },
                        {
                            'if': {'row_index': 'even'},
                            'backgroundColor': '#FFFFFF'
                        }
                    ],
                    sort_action='native',  # Enable sorting on all columns
                    sort_mode='multi'  # Enable sorting on multiple columns
                )
            ]
        )
    ]
)

# Callback to update the column names
@app.callback(
    Output('data-table', 'columns'),
    Input('rename-button', 'n_clicks'),
    [State(f'input-{col}', 'value') for col in df.columns]
)
def update_columns(n_clicks, *new_column_names):
    if n_clicks > 0:
        return [{'name': new_name, 'id': col} for new_name, col in zip(new_column_names, df.columns)]
    return [{'name': col, 'id': col} for col in df.columns]

# Register the layout with the Dash app
app.layout = layout