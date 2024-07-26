import re
import pandas as pd
from dash import Input, Output, State, html, dcc
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


# Callback to update the data types and stored data
@app.callback(
    [Output('data-table', 'data'), Output('stored-data', 'data')],
    Input('typecast-button', 'n_clicks'),
    [State(f'dtype-input-{col}', 'value') for col in df.columns]
)
def change_data_types(n_clicks, *new_data_types):
    if n_clicks > 0:
        updated_df = df.copy()
        for col, dtype in zip(updated_df.columns, new_data_types):
            match_round = re.match(r'^(float|double)\((\d+)\)$', dtype)
            match_round_million = re.match(r'^(float|double)\((\d+)\) M$', dtype)
            match_round_billion = re.match(r'^(float|double)\((\d+)\) B$', dtype)
            match_million_round = re.match(r'^(float|double) M\((\d+)\)$', dtype)
            match_billion_round = re.match(r'^(float|double) B\((\d+)\)$', dtype)
            match_round_million_round = re.match(r'^(float|double)\((\d+)\) M\((\d+)\)$', dtype)
            match_round_billion_round = re.match(r'^(float|double)\((\d+)\) B\((\d+)\)$', dtype)
            match_million = re.match(r'^(float|double) M$', dtype)
            match_billion = re.match(r'^(float|double) B$', dtype)

            if dtype == 'int':
                updated_df[col] = updated_df[col].astype(int)
            elif match_round_million_round:
                initial_rounding = int(match_round_million_round.group(2))
                final_rounding = int(match_round_million_round.group(3))
                updated_df[col] = updated_df[col].astype(float).round(initial_rounding) / 1_000_000
                updated_df[col] = updated_df[col].round(final_rounding).map(lambda x: f"{x:.{final_rounding}f}")
            elif match_round_billion_round:
                initial_rounding = int(match_round_billion_round.group(2))
                final_rounding = int(match_round_billion_round.group(3))
                updated_df[col] = updated_df[col].astype(float).round(initial_rounding) / 1_000_000_000
                updated_df[col] = updated_df[col].round(final_rounding).map(lambda x: f"{x:.{final_rounding}f}")
            elif match_round_million:
                decimal_places = int(match_round_million.group(2))
                updated_df[col] = updated_df[col].astype(float).round(decimal_places) / 1_000_000
            elif match_round_billion:
                decimal_places = int(match_round_billion.group(2))
                updated_df[col] = updated_df[col].astype(float).round(decimal_places) / 1_000_000_000
            elif match_million_round:
                decimal_places = int(match_million_round.group(2))
                updated_df[col] = updated_df[col].astype(float) / 1_000_000
                updated_df[col] = updated_df[col].round(decimal_places).map(lambda x: f"{x:.{decimal_places}f}")
            elif match_billion_round:
                decimal_places = int(match_billion_round.group(2))
                updated_df[col] = updated_df[col].astype(float) / 1_000_000_000
                updated_df[col] = updated_df[col].round(decimal_places).map(lambda x: f"{x:.{decimal_places}f}")
            elif match_round:
                decimal_places = int(match_round.group(2))
                updated_df[col] = updated_df[col].astype(float).round(decimal_places)
                updated_df[col] = updated_df[col].map(lambda x: f"{x:.{decimal_places}f}")
            elif match_million:
                updated_df[col] = updated_df[col].astype(float) / 1_000_000
            elif match_billion:
                updated_df[col] = updated_df[col].astype(float) / 1_000_000_000
            elif dtype == 'float':
                updated_df[col] = updated_df[col].astype(float)
            elif dtype == 'double':
                updated_df[col] = updated_df[col].astype(float)
            elif dtype == 'string':
                updated_df[col] = updated_df[col].astype(str)
        return updated_df.to_dict('records'), updated_df.to_dict('records')
    return df.to_dict('records'), df.to_dict('records')


# Callback to download the DataTable as CSV
@app.callback(
    Output('download-data', 'data'),
    Input('download-button', 'n_clicks'),
    State('stored-data', 'data'),
    prevent_initial_call=True
)
def download_data(n_clicks, data):
    df = pd.DataFrame(data)
    return dcc.send_data_frame(df.to_csv, 'data.csv')