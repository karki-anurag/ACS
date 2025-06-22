# Library System Setup Guide

This guide provides instructions to set up and run the Library System application, which includes a Flask backend and a simple HTML/JavaScript frontend.

## 1. Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.x**: Download from [python.org](https://www.python.org/downloads/)
* **pip**: Python's package installer (usually comes with Python)
* **PostgreSQL**: Database server. Download from [postgresql.org](https://www.postgresql.org/download/)
* **Internet Connection**: Required for Cloudflare Turnstile verification and sending emails.

## 2. Backend Setup (Python Application)

1.  **Navigate to your project directory:**
    Open your terminal or command prompt and go to the folder where your `app.py` and other project files are located.

2.  **Install Python Dependencies:**
    It's highly recommended to use a virtual environment.
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
    Then, install the required Python libraries:
    ```bash
    pip install Flask Flask-Cors bcrypt psycopg2-binary requests pytz
    ```
    *(Note: `psycopg2-binary` is used for simplicity, for production consider `psycopg2` and its system dependencies)*

3.  **Configure `app.py`:**
    Open `app.py` and update the following configuration variables:
    * **Database Credentials:**
        ```python
        DB_USER = "karki" # Your PostgreSQL username
        DB_PASSWORD = "karkisir123" # Your PostgreSQL password
        DB_HOST = "localhost"
        DB_NAME = "anurag" # The name of your database (will be created later)
        ```
    * **Gmail Credentials (for OTP and Password Reset emails):**
        ```python
        GMAIL_USER = "your_email@gmail.com" # Your Gmail address
        GMAIL_APP_PASSWORD = "your_gmail_app_password" # Generated from Google Account Security
        ```
        * **Important for Gmail App Password**: If you use 2-Step Verification on your Gmail, you'll need to generate an "App password" for this application instead of using your regular Gmail password. Go to your Google Account > Security > App passwords.
    * **Cloudflare Turnstile Secret Key:**
        ```python
        CLOUDFLARE_SECRET_KEY = "0x4AAAAAABho5hPgTPE5grJYO_YOUR_SECRET_KEY" # <<--- Get this from Cloudflare Dashboard
        ```
        * **Important**: Log in to your Cloudflare account, go to your Turnstile dashboard, and get the **Secret Key** associated with the site key you are using in `index.html` and `register.html` (`0x4AAAAAABho5hPgTPE5grJY`). This is crucial for CAPTCHA verification.

## 3. Database Setup (PostgreSQL)

1.  **Connect to PostgreSQL:**
    Open your PostgreSQL command-line tool (e.g., `psql`) or a GUI tool (e.g., pgAdmin). Connect as a superuser or the `DB_USER` you configured.

2.  **Create the Database:**
    ```sql
    CREATE DATABASE anurag; -- Use the DB_NAME you configured in app.py
    ```

3.  **Create Tables:**
    Connect to the newly created database (`anurag`). Then, run the following SQL commands to create the necessary tables:

    * **`users` table:**
        ```sql
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            last_password_change TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        ```

    * **`password_history` table:**
        ```sql
        CREATE TABLE password_history (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL REFERENCES users(email) ON DELETE CASCADE,
            password VARCHAR(255) NOT NULL,
            changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        ```

    * **`password_resets` table (for forgot password functionality):**
        ```sql
        CREATE TABLE password_resets (
            id SERIAL PRIMARY KEY,
            token VARCHAR(255) UNIQUE NOT NULL,
            user_email VARCHAR(255) NOT NULL REFERENCES users(email) ON DELETE CASCADE,
            expires_at TIMESTAMP WITH TIME ZONE NOT NULL
        );
        ```

## 4. Frontend Setup

The frontend consists of static HTML, CSS, and JavaScript files. You just need a simple HTTP server to serve them.

1.  **Navigate to your project root directory** (where `index.html` and `register.html` are located).

2.  **Start a simple Python HTTP server:**
    ```bash
    python -m http.server 8000
    ```
    This will serve your frontend files at `http://localhost:8000`.

## 5. Running the Application

1.  **Start the Flask Backend:**
    Open a *new* terminal or command prompt (keep the frontend server terminal open).
    Navigate to your project directory and activate your virtual environment (if you created one).
    ```bash
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
    Then run your Flask application:
    ```bash
    python app.py
    ```
    The Flask server should start, usually on `http://127.0.0.1:5000` (or `http://localhost:5000`).

2.  **Access the Frontend:**
    Open your web browser and go to:
    * **Register:** `http://localhost:8000/register.html`
    * **Login:** `http://localhost:8000/index.html`

## Troubleshooting

* **"CAPTCHA verification failed."**: Double-check your `CLOUDFLARE_SECRET_KEY` in `app.py`. Ensure it's the correct Secret Key from your Cloudflare dashboard and matches the Site Key used in your HTML.
* **Email Sending Issues**: Verify `GMAIL_USER` and `GMAIL_APP_PASSWORD`. If you're using 2-Step Verification for Gmail, you *must* use an App Password. Check your Flask server console for email-related errors.
* **Database Connection Errors**: Ensure PostgreSQL is running, your `DB_USER` and `DB_PASSWORD` are correct, and the `anurag` database exists with the correct tables.
* **`requests` library not found**: Run `pip install requests`.
* **CSS/JS not loading**: Ensure the `css` and `js` folders are in the same directory as your `index.html` and `register.html` files, and that the file paths in your HTML (e.g., `href="css/style.css"`, `src="js/login.js"`) are correct.