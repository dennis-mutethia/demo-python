import os  # Import os module to access environment variables
from psycopg2 import pool  # Import pool from psycopg2 for database connection pooling
        
class Database:
    # Database class to manage PostgreSQL connections and operations
    
    def __init__(self):   
        # Constructor method to initialize the database connection pool
        # Uses environment variables for configuration to keep credentials secure
        self.DB_CONFIG = {
            'host': os.getenv('DB_HOST'),      # Database host address from env variable
            'database': os.getenv('DB_NAME'),  # Database name from env variable
            'port': os.getenv('DB_PORT'),      # Database port from env variable
            'user': os.getenv('DB_USER'),      # Database username from env variable
            'password': os.getenv('DB_PASSWORD')  # Database password from env variable
        }
        
        try:
            # Attempt to create a connection pool with min 1 and max 20 connections
            self.db_pool = pool.SimpleConnectionPool(
                1,          # Minimum number of connections in the pool
                20,         # Maximum number of connections in the pool
                **self.DB_CONFIG  # Unpack DB_CONFIG dictionary as keyword arguments
            )
        except Exception as e:
            # Handle any errors during pool creation
            print(f"Error connecting to database: {e}")  # Print error message
            exit(1)  # Exit the program with an error status code

    def init_db(self):
        # Method to initialize the database by creating necessary tables
        conn = self.db_pool.getconn()  # Get a connection from the pool
        try:
            with conn.cursor() as cur:  # Create a cursor for executing SQL commands
                # Execute SQL to create users table if it doesn't exist
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,        -- Auto-incrementing unique identifier
                        username TEXT UNIQUE NOT NULL, -- Unique username, cannot be null
                        password TEXT NOT NULL        -- Password (hashed), cannot be null
                    )
                """)
                conn.commit()  # Commit the transaction to save changes
        finally:
            # Ensure the connection is returned to the pool, even if an error occurs
            self.db_pool.putconn(conn)  # Return connection to the pool

    def get_connection(self):
        # Method to retrieve a database connection from the pool
        return self.db_pool.getconn()  # Returns a connection object

    def put_connection(self, conn):
        # Method to return a connection back to the pool
        self.db_pool.putconn(conn)  # Puts the connection back into the pool

    def close_all(self):
        # Method to close all connections in the pool
        # Useful for cleanup when shutting down the application
        if self.db_pool:  # Check if pool exists
            self.db_pool.closeall()  # Close all connections in the pool