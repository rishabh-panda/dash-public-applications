# Import the app object from app.py
from app import app

print("Triggering the application...\n")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)