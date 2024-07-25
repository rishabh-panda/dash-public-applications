from dash import Input, Output, State, html
from app import app
from data.data_loader import df

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