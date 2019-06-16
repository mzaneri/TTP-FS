from app import app

@app.route('/')
def blank():
    return "Starting Page"
