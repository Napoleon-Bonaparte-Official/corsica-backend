import threading
from flask import render_template, request, send_from_directory
from flask.cli import AppGroup
from flask_cors import CORS  # Import CORS from flask_cors
from __init__ import app, db
from api.user import user_api
from api.video import video_api
from model.users import initUsers, initVideos
from projects.projects import app_projects

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# Register URIs
app.register_blueprint(user_api)
app.register_blueprint(video_api)
app.register_blueprint(app_projects)

# Define error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Define routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/table/')
def table():
    return render_template("table.html")

@app.route('/videos/<path:path>')
def videos(path):
    return send_from_directory('videos', path)

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initVideos()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# Run the application
if __name__ == "__main__":
    # Initialize CORS with origins and credentials support
    CORS(app, origins=['http://localhost:4100', 'http://127.0.0.1:4100', 'https://napoleon-bonaparte-official.github.io'], supports_credentials=True)
    app.run(debug=True, host="0.0.0.0", port="8069")