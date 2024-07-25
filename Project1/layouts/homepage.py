from dash import dash_table, dcc, html
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
                'backgroundColor': '#E1E1E1',
                'border': '1px solid #ccc',
                'height': '6%',
                'padding': '8px',
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'left',
                'flexWrap': 'nowrap',
                'overflowX': 'auto',
                'position': 'relative', 
                'borderRadius': '10px'
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
                                   'borderRadius': '8px'}
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
                        'bottom': '10px',
                        'right': '20px',
                        'backgroundColor': 'black',
                        'color': 'white',
                        'fontWeight': 'bold'
                    }
                )
            ]
        ),

        # Data Type Change Inputs Container
        html.Div(
            style={
                'backgroundColor': '#E1E1E1',
                'border': '1px solid #ccc',
                'height': '6%',
                'padding': '8px',
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'left',
                'flexWrap': 'nowrap',
                'overflowX': 'auto',
                'position': 'relative',
                'borderRadius': '10px',
                'marginTop': '10px'
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
                            id=f'dtype-input-{col}',
                            type='text',
                            value='string',  # Default data type
                            style={'width': '80px', 
                                   'height': '20px', 
                                   'fontSize': '12px', 
                                   'border': '1px solid #ccc', 
                                   'borderRadius': '8px'}
                        ),
                    ]
                ) for col in df.columns
            ] + [
                html.Button(
                    'Typecast',
                    id='typecast-button',
                    n_clicks=0,
                    style={
                        'fontSize': '12px',
                        'padding': '2px 5px',
                        'position': 'absolute',
                        'bottom': '10px',
                        'right': '20px',
                        'backgroundColor': 'black',
                        'color': 'white',
                        'fontWeight': 'bold'
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