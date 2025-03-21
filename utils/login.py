# Import necessary Flask components for web functionality
from flask import (
    render_template,  # For rendering HTML templates
    request,         # For accessing request data (e.g., form submissions)
    redirect,        # For redirecting to different routes
    url_for,         # For generating URLs for routes
    flash,           # For displaying temporary messages to users
    session          # For managing user session data
)
from werkzeug.security import check_password_hash  # For verifying hashed passwords

class Login:
    # Class to handle user login functionality
    
    def __init__(self, db):
        # Constructor to initialize the Login class
        # Args:
        #     db: Database instance for querying user data
        self.db = db  # Store the database instance for later use

    def handle(self):
        # Method to handle login requests (both GET and POST)
        # Returns:
        #     Rendered template or redirect response
        
        if request.method == 'POST':  # Check if the request is a form submission
            # Extract form data
            username = request.form['username']  # Get username from form
            password = request.form['password']  # Get password from form
            
            conn = self.db.get_connection()  # Get a database connection from the pool
            try:
                with conn.cursor() as cur:  # Create a cursor for SQL execution
                    # Query the database for user with matching username
                    cur.execute(
                        "SELECT id, password FROM users WHERE username = %s",
                        (username,)  # Use parameterized query to prevent SQL injection
                    )
                    user = cur.fetchone()  # Fetch the first matching row (id, password)
                    
                    # Check if user exists and password matches
                    if user and check_password_hash(user[1], password):
                        # user[1] is the stored hashed password
                        session['user_id'] = user[0]    # Store user ID in session
                        session['username'] = username  # Store username in session
                        flash('Login successful!')      # Show success message
                        return redirect(url_for('index'))  # Redirect to home/dashboard
                    else:
                        flash('Invalid username or password')  # Show error message
                        return redirect(url_for('login'))     # Redirect back to login page
            finally:
                # Ensure the connection is returned to the pool
                self.db.put_connection(conn)  # Return connection to pool
        
        # If GET request or after failed login, render the login page
        return render_template('login.html')  # Display login form