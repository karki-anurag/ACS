
# Library System Web Application

This project is a basic web application for a Library System, demonstrating secure user registration, login with Multi-Factor Authentication (MFA), password management, and a visually appealing "library vibe" user interface.

## Table of Contents

1.  [Features](#features)
2.  [Technologies Used](#technologies-used)
3.  [Project Structure](#project-structure)
4.  [Setup and Installation](#setup-and-installation)
    * [Database Setup](#database-setup)
    * [Backend Setup](#backend-setup)
    * [Frontend Setup](#frontend-setup)
5.  [How to Run](#how-to-run)
6.  [Screenshots (Optional)](#screenshots-optional)
7.  [Future Enhancements (Optional)](#future-enhancements-optional)

## 1. Features

This system comes equipped with several modern security and usability features:

* **User Registration:**
    * New users can sign up with an email and password.
    * Includes a **Password Policy** with a live strength indicator during registration (checks for length, uppercase, lowercase, numbers, and special characters).
    * Integrated **Cloudflare Turnstile** CAPTCHA for bot protection.
* **User Login with MFA (Multi-Factor Authentication):**
    * Users log in with their email and password.
    * A **One-Time Password (OTP)** is sent to their registered email for secondary authentication.
    * The OTP must be verified to gain access.
    * Integrated **Cloudflare Turnstile** CAPTCHA.
* **Secure Password Storage:**
    * All user passwords are securely stored using **Bcrypt hashing**, ensuring that original passwords are never stored in plain text.
* **Forgot Password Functionality:**
    * Users can request a password reset if they forget their password.
    * A unique, time-limited password reset link is sent to their registered email.
    * Allows users to set a new password securely through the provided link.
* **Consistent User Interface:**
    * The application features a dark, rich "library vibe" aesthetic across all pages (login, registration, dashboard, forgot password, reset password) for a cohesive user experience.
* **Dashboard:**
    * A simple dashboard page that a user reaches after successful login.

## 2. Technologies Used

* **Backend:**
    * **Python 3:** Core programming language.
    * **Flask:** Web framework for building the API.
    * **Flask-CORS:** For handling Cross-Origin Resource Sharing.
    * **Psycopg2:** PostgreSQL adapter for Python.
    * **Bcrypt:** For secure password hashing.
    * **smtplib:** Python's standard library for sending emails (for OTP and password reset links).
    * **Secrets:** For generating cryptographically strong random numbers (for OTP and tokens).
    * **Datetime & pytz:** For handling timestamps and timezone-aware dates for token expiration.
* **Frontend:**
    * **HTML5:** Structure of web pages.
    * **CSS3:** Styling and "library vibe" theme.
    * **JavaScript (ES6+):** Client-side logic for form handling, API calls, and real-time feedback (e.g., password strength).
    * **Cloudflare Turnstile:** CAPTCHA service.
    * **Google Fonts (Poppins):** For modern typography.
* **Database:**
    * **PostgreSQL:** Relational database for storing user and token information.

## 3. Project Structure
# Library System Web Application

This project is a basic web application for a Library System, demonstrating secure user registration, login with Multi-Factor Authentication (MFA), password management, and a visually appealing "library vibe" user interface.

## Table of Contents

1.  [Features](#features)
2.  [Technologies Used](#technologies-used)
3.  [Project Structure](#project-structure)
4.  [Setup and Installation](#setup-and-installation)
    * [Database Setup](#database-setup)
    * [Backend Setup](#backend-setup)
    * [Frontend Setup](#frontend-setup)
5.  [How to Run](#how-to-run)
6.  [Screenshots (Optional)](#screenshots-optional)
7.  [Future Enhancements (Optional)](#future-enhancements-optional)

## 1. Features

This system comes equipped with several modern security and usability features:

* **User Registration:**
    * New users can sign up with an email and password.
    * Includes a **Password Policy** with a live strength indicator during registration (checks for length, uppercase, lowercase, numbers, and special characters).
    * Integrated **Cloudflare Turnstile** CAPTCHA for bot protection.
* **User Login with MFA (Multi-Factor Authentication):**
    * Users log in with their email and password.
    * A **One-Time Password (OTP)** is sent to their registered email for secondary authentication.
    * The OTP must be verified to gain access.
    * Integrated **Cloudflare Turnstile** CAPTCHA.
* **Secure Password Storage:**
    * All user passwords are securely stored using **Bcrypt hashing**, ensuring that original passwords are never stored in plain text.
* **Forgot Password Functionality:**
    * Users can request a password reset if they forget their password.
    * A unique, time-limited password reset link is sent to their registered email.
    * Allows users to set a new password securely through the provided link.
* **Consistent User Interface:**
    * The application features a dark, rich "library vibe" aesthetic across all pages (login, registration, dashboard, forgot password, reset password) for a cohesive user experience.
* **Dashboard:**
    * A simple dashboard page that a user reaches after successful login.

## 2. Technologies Used

* **Backend:**
    * **Python 3:** Core programming language.
    * **Flask-CORS:** For handling Cross-Origin Resource Sharing.
    * **Psycopg2:** PostgreSQL adapter for Python.
    * **Bcrypt:** For secure password hashing.
    * **smtplib:** Python's standard library for sending emails (for OTP and password reset links).
    * **Secrets:** For generating cryptographically strong random numbers (for OTP and tokens).
    * **Datetime & pytz:** For handling timestamps and timezone-aware dates for token expiration.
* **Frontend:**
    * **HTML5:** Structure of web pages.
    * **CSS3:** Styling and "library vibe" theme.
    * **JavaScript (ES6+):** Client-side logic for form handling, API calls, and real-time feedback (e.g., password strength).
    * **Cloudflare Turnstile:** CAPTCHA service.
    * **Google Fonts (Poppins):** For modern typography.
* **Database:**
    * **PostgreSQL:** Relational database for storing user and token information.

## 3. Project Structure
├── app.py                  # backend using Python
├── requirements.txt        # Python dependencies
├── index.html              # Login page
├── register.html           # User registration page
├── dashboard.html          # User dashboard after successful login
├── forgot_password.html    # Page to request password reset email
├── reset_password.html     # Page to set a new password using a token
├── css/
│   └── style.css           # All application-wide CSS for the "library vibe"
├── js/
│   ├── auth.js             # JavaScript for user registration (register.html)
│   ├── login.js            # JavaScript for user login and OTP verification (index.html)
│   ├── password.js         # JavaScript for password strength indicator (register.html)
│   ├── forgot_password.js  # JavaScript for forgot password request (forgot_password.html)
│   └── reset_password.js   # JavaScript for password reset functionality (reset_password.html)
└── static/
└── images/
└── background.jpg  # Background image for the library theme

## 4. Setup and Installation

Follow these steps to get the project running on your local machine.

### Database Setup

1.  **Install PostgreSQL:** If you don't have PostgreSQL installed, download and install it from [postgresql.org](https://www.postgresql.org/download/).
2.  **Create a Database:**
    Open your PostgreSQL client (e.g., `psql` in terminal, or pgAdmin) and create a new database. For this project, the database name is `anurag`.
    ```sql
    CREATE DATABASE anurag;
    ```
3.  **Create Tables:**
    Connect to your `anurag` database and run the following SQL queries to create the necessary tables:

    ```sql
    -- Create users table
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    -- Create password_resets table
    CREATE TABLE IF NOT EXISTS password_resets (
        token VARCHAR(255) PRIMARY KEY,
        user_email VARCHAR(255) NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
    );
    ```
    **Note:** Ensure the `DB_USER` and `DB_PASSWORD` in `app.py` match your PostgreSQL user credentials. The default in `app.py` is `DB_USER = "karki"` and `DB_PASSWORD = "karkisir123"`.

### Backend Setup

1.  **Clone the repository** (if applicable) or ensure you have all project files.
2.  **Navigate to the project root directory** in your terminal.
3.  **Create a Virtual Environment** (recommended):
    ```bash
    python -m venv venv
    ```
4.  **Activate the Virtual Environment:**
    * **Windows:** `.\venv\Scripts\activate`
    * **macOS/Linux:** `source venv/bin/activate`
5.  **Install Dependencies:**
    Install the required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
    Your `requirements.txt` should contain:
    ```
    Flask
    Flask-Cors
    bcrypt
    psycopg2-binary
    pytz
    ```
6.  **Configure Email Settings:**
    Open `app.py` and update the following lines with your Gmail credentials:
    ```python
    GMAIL_USER = "your_email@gmail.com"      # Your Gmail address
    GMAIL_APP_PASSWORD = "your_app_password" # Generated App Password for Gmail
    ```
    **Important:** You need to generate an "App password" for your Gmail account, as direct login with your regular password is often blocked for security reasons. Refer to [Google's help page](https://support.google.com/accounts/answer/185833?hl=en) for instructions on how to generate one.

### Frontend Setup

1.  No special installation is required for the frontend. You just need to serve the HTML files.
2.  Ensure your `static/images/background.jpg` file exists for the "library vibe" background.

## 5. How to Run

Follow these steps to start both the backend and frontend servers:

1.  **Start the Backend Server (Flask API):**
    Open a new terminal window, navigate to your project's root directory, activate your virtual environment, and run:
    ```bash
    # (Ensure virtual environment is activated)
    python app.py
    ```
    The backend will typically run on `http://127.0.0.1:5000/`.

2.  **Start the Frontend Server (HTML/JavaScript):**
    Open *another* new terminal window, navigate to your project's root directory, and run a simple HTTP server:
    ```bash
    python -m http.server 8000
    ```
    The frontend will be accessible at `http://localhost:8000/`.

3.  **Access the Application:**
    Open your web browser and navigate to:
    * **Login Page:** `http://localhost:8000/index.html`
    * **Registration Page:** `http://localhost:8000/register.html`

## 6. Screenshots (Optional)

*(You can add screenshots of your login, register, and dashboard pages here to give a visual overview of your project.)*

## 7. Future Enhancements (Optional)

* Add user session management (e.g., using Flask-Login).
* Implement a proper user dashboard with library functionalities (e.g., Browse books, borrowing, returning).
* Add admin panel for managing users and books.
* Improve frontend error handling and user feedback.
* Integrate proper logging for backend activities.
* More robust password policy enforcement on the backend.
* Implement a rate-limiting mechanism for login attempts and OTP requests.

---
