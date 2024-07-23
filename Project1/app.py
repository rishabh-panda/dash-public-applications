import dash
from dash import dcc, html

# Initialize the Dash app
app = dash.Dash(__name__)

# Import the layout from homepage.py
from layouts.homepage import layout

# Set the layout of the app
app.layout = layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)