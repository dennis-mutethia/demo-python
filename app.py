import os  # Import os module to access environment variables
from dotenv import load_dotenv  # Import load_dotenv to load variables from .env file
from flask import (
    Flask,           # Main Flask class for creating the web application
    render_template, # For rendering HTML templates
    redirect,        # For redirecting to different routes
    url_for,         # For generating URLs for routes
    flash,           # For displaying temporary messages to users
    session          # For managing user session data
)
from utils.db import Database        # Import Database class for database operations
from utils.register import Register  # Import Register class for registration handling
from utils.login import Login        # Import Login class for login handling

# Load environment variables from .env file
load_dotenv()  # Reads .env file and adds variables to the environment

# Create Flask application instance
app = Flask(__name__)  # Initialize Flask app with the current module name
app.secret_key = os.getenv('APP_SECRET_KEY')  # Set secret key from environment variable
# Note: APP_SECRET_KEY should be defined in .env file for security

# Initialize database
db = Database()  # Create instance of Database class to manage PostgreSQL connections

# Initialize utility classes with db instance
register_handler = Register(db)  # Create Register instance with database dependency
login_handler = Login(db)       # Create Login instance with database dependency

@app.route('/')
def index():
    # Route handler for the root URL (home page)
    # Returns:
    #     Rendered index.html template
    return render_template('index.html')  # Render the home page template

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Route handler for user registration
    # Accepts both GET and POST requests
    # Returns:
    #     Response from Register.handle() (template or redirect)
    return register_handler.handle()  # Delegate to Register class handler

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Route handler for user login
    # Accepts both GET and POST requests
    # Returns:
    #     Response from Login.handle() (template or redirect)
    return login_handler.handle()  # Delegate to Login class handler

@app.route('/logout')
def logout():
    # Route handler for user logout
    # Returns:
    #     Redirect to index page after logout
    session.pop('user_id', None)    # Remove user_id from session, if it exists
    session.pop('username', None)   # Remove username from session, if it exists
    flash('Logged out successfully')  # Show success message to user
    return redirect(url_for('index'))  # Redirect to home page

if __name__ == '__main__':
    # Entry point for running the application
    db.init_db()  # Initialize database tables before starting the app
    app.run(debug=True)  # Run the Flask app in debug mode
    # debug=True enables auto-reloading and detailed error messages