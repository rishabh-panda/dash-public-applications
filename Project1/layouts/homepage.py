import dash
from dash import dash_table
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output
from app import app
from data.data_loader import df

# Define the layout of the homepage
layout = html.Div(
    style={'backgroundColor': '#FFFFFF', 'height': '100vh', 'fontFamily': 'Arial'},
    children=[
        # Top Container
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
        # Bottom Container
        html.Div(
            style={
                'backgroundColor': '#FFFFFF',
                'padding': '20px',
                'height': '80%',
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
                    sort_action='native'  # Enable sorting on all columns
                )
            ]
        )
    ]
)

# Register the layout with the Dash app
app.layout = layout