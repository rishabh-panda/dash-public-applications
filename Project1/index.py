# Import the app object from app.py
from app import app
from layouts import homepage
from dash import html
import callbacks.homepage_callbacks

app.layout = html.Div([
    homepage.layout
])

print("Triggering the application...\n")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)