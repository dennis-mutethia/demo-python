# Import necessary Flask components for web functionality
from flask import (
    render_template,  # For rendering HTML templates
    request,         # For accessing request data (e.g., form submissions)
    redirect,        # For redirecting to different routes
    url_for,         # For generating URLs for routes
    flash            # For displaying temporary messages to users
)
from werkzeug.security import generate_password_hash  # For creating secure password hashes

class Register:
    # Class to handle user registration functionality
    
    def __init__(self, db):
        # Constructor to initialize the Register class
        # Args:
        #     db: Database instance for querying and storing user data
        self.db = db  # Store the database instance for later use

    def handle(self):
        # Method to handle registration requests (both GET and POST)
        # Returns:
        #     Rendered template or redirect response
        
        if request.method == 'POST':  # Check if the request is a form submission
            # Extract form data
            username = request.form['username']  # Get username from form
            password = request.form['password']  # Get password from form
            
            conn = self.db.get_connection()  # Get a database connection from the pool
            try:
                with conn.cursor() as cur:  # Create a cursor for SQL execution
                    # Check if username already exists in the database
                    cur.execute(
                        "SELECT id FROM users WHERE username = %s",
                        (username,)  # Use parameterized query to prevent SQL injection
                    )
                    if cur.fetchone():  # If a row is returned, username is taken
                        flash('Username already exists')  # Show error message
                        return redirect(url_for('register'))  # Redirect back to register page
                    
                    # If username is available, create new user
                    hashed_password = generate_password_hash(password)  # Hash the password securely
                    cur.execute(
                        "INSERT INTO users (username, password) VALUES (%s, %s)",
                        (username, hashed_password)  # Insert username and hashed password
                    )
                    conn.commit()  # Commit the transaction to save the new user
                    flash('Registration successful! Please login.')  # Show success message
                    return redirect(url_for('login'))  # Redirect to login page
            except Exception as e:
                # Handle any database errors during registration
                conn.rollback()  # Undo any changes if an error occurs
                flash('Error occurred during registration')  # Show error message
                return redirect(url_for('register'))  # Redirect back to register page
            finally:
                # Ensure the connection is returned to the pool
                self.db.put_connection(conn)  # Return connection to pool
        
        # If GET request or after failed registration, render the register page
        return render_template('register.html')  # Display registration form