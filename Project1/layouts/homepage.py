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
                'justifyContent': 'space-between'
            },
            children=[
                # Master Heading
                html.H1(
                    children='Retail inventory optimizer application | WIP version',
                    style={'margin': '0', 'fontFamily': 'Arial', 'color': '#848484'}
                ),
                # Live and Extract Buttons
                dcc.RadioItems(
                    id='data-mode',
                    options=[
                        {'label': 'Live', 'value': 'live'},
                        {'label': 'Extract', 'value': 'extract'}
                    ],
                    value='live',
                    labelStyle={
                        'display': 'inline-block',
                        'margin': '0 10px',
                        'padding': '5px 15px',
                        'border': '1px solid #ccc',
                        'borderRadius': '10px',
                        'backgroundColor': '#ECECEC',
                        'cursor': 'pointer',
                        'fontFamily': 'Arial',
                        'textAlign': 'center'
                    },
                    inputStyle={
                        'marginRight': '5px'
                    },
                    style={
                        'display': 'flex',
                        'alignItems': 'center'
                    }
                )
            ]
        ),
        
        # Column Renaming Inputs Container
        html.Div(
            style={
                'backgroundColor': '#E1E6FF',
                'padding': '10px',
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center',
                'flexWrap': 'nowrap',
                'overflowX': 'auto',
                'position': 'relative'
            },
            children=[
                html.Div(
                    style={'margin': '0 5px'},
                    children=[
                        html.Label(
                            f'{col} ',
                            style={'fontSize': '12px', 'marginRight': '5px'}
                        ),
                        dcc.Input(
                            id=f'input-{col}',
                            type='text',
                            value=col,
                            style={'width': '80px', 
                                   'height': '20px', 
                                   'fontSize': '12px', 
                                   'border': '1px solid #ccc', 
                                   'borderRadius': '10px'}
                        ),
                    ]
                ) for col in df.columns
            ] + [
                html.Button(
                    'Rename',
                    id='rename-button',
                    n_clicks=0,
                    style={
                        'fontSize': '12px',
                        'padding': '2px 5px',
                        'position': 'absolute',
                        'bottom': '0px',
                        'right': '20px'
                    }
                )
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
                        'backgroundColor': '#CC0000',
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

# Callback to update the RadioItems styles
@app.callback(
    Output('data-mode', 'options'),
    Input('data-mode', 'value')
)
def update_radio_styles(selected_value):
    options = [
        {'label': 'Live', 'value': 'live'},
        {'label': 'Extract', 'value': 'extract'}
    ]
    for option in options:
        if option['value'] == selected_value:
            option['label'] = html.Span(
                option['label'],
                style={'color': '#FFFFFF', 'backgroundColor': '#CC0000', 'padding': '5px 15px', 'borderRadius': '10px'}
            )
        else:
            option['label'] = html.Span(
                option['label'],
                style={'color': '#000000', 'backgroundColor': '#ECECEC', 'padding': '5px 15px', 'borderRadius': '10px'}
            )
    return options

# Register the layout with the Dash app
app.layout = layout