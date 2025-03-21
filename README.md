# Flask Authentication App with Supabase

Welcome to the Flask Authentication App! This is a simple web application built with Python Flask and Supabase, a free, open-source Backend-as-a-Service platform that provides a PostgreSQL database. This app demonstrates user registration, login, logout, and a basic dashboard, all styled with Bootstrap. It’s perfect for learning how to build web applications with Flask and integrate them with a cloud database.

## Project Overview

This app allows users to:
- **Register** with a username and password.
- **Login** to access a personalized dashboard.
- **Logout** to end their session.
- View a **dashboard** with a welcome message and placeholder content.

The app uses Supabase for database storage, Flask for the web framework, and Bootstrap for styling. It’s organized into modular files for better code management.

## Prerequisites

Before running this app, ensure you have:
- **Python 3.8+** installed.
- A **Supabase account** (free tier) and a project set up.
- **Git** (optional, for cloning the repo).

## Setup Instructions

### 1. Clone the Repository
If you’ve shared this code with your students via Git, they can clone it:
```bash
git clone <repository-url>
cd demo-python
code .
```

### 2. Set Up Supabase
Sign up at Supabase and create a new project.

Go to Settings in your Supabase dashboard to get your:
- `SUPABASE_HOST`
- `SUPABASE_PORT`
- `SUPABASE_DATABASE_NAME`
- `SUPABASE_USER`
- `SUPABASE_PASSWORD`

In the SQL Editor, run this query to create the users table:
sql
```
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
```

### 3. Configure Environment Variables
Create a .env file in the project root with the following:
```
APP_SECRET_KEY=your-secret-key-here
DB_HOST=aws-0-eu-xxxx-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.xxxxxxx
DB_PASSWORD=xxxxx
```
Replace placeholders with your Supabase credentials.

### 5. Project Structure
```
flask-supabase-app/
├── app.py
├── .env
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
└── utils/
    ├── __init__.py
    ├── db.py
    ├── login.py
    └── register.py
```

### Code Breakdown
`app.py`
The main Flask application file:
- Sets up routes for the dashboard, registration, login, and logout.
- Uses environment variables for configuration.

`utils/db.py`
Handles Supabase client initialization:
- Connects to Supabase using the supabase-py library.
- Creates the users table if it doesn’t exist.

`utils/register.py`
Manages user registration:
- Checks for existing usernames.
- Hashes passwords and inserts new users into Supabase.

`utils/login.py`
Handles user login:
- Verifies credentials and sets session data.
- Redirects to the dashboard on success.

`templates/`
Contains HTML files with Bootstrap styling:
- `dashboard.html`: User dashboard with navbar and cards.
- `login.html`: Login form.
`register.html`: Registration form.


### Dev Containers
- Ensure that you have installed dev containers in your vs-code
- Reopen the application as a dev- container

### Running the App
1. Start the Flask server:
    ```
    bash
    python app.py
    ```
2. Open your browser to http://127.0.0.1:5000/.
3. Register a user, log in, and explore the dashboard!

### Next Steps
- Add more dashboard features (e.g. charts, user profile editing).

