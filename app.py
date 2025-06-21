# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import psycopg2
import secrets
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import pytz
import requests # <--- NEW: Import requests library

app = Flask(__name__)
CORS(app)

DB_USER = "karki"
DB_PASSWORD = "karkisir123"
DB_HOST = "localhost"
DB_NAME = "anurag"

GMAIL_USER = "anuragkarki2004@gmail.com"
GMAIL_APP_PASSWORD = "zbsmjsqdvuymkbth"

# <--- NEW: Cloudflare Turnstile Secret Key (replace with your actual secret key)
# Get this from your Cloudflare Turnstile dashboard for your site.
CLOUDFLARE_SECRET_KEY = "0x4AAAAAABho5r4yvWGIVblav4Dx0tdTAGk" # <<--- IMPORTANT: REPLACE THIS!

OTP_STORE = {}

def db_conn():
    return psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        dbname=DB_NAME
    )

def send_email(to_email, subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email failed to {to_email}:", e)
        return False

def send_otp_email(to_email, otp_code):
    subject = "Library Login OTP"
    content = f"Your OTP is: {otp_code}"
    return send_email(to_email, subject, content)

def send_password_reset_email(to_email, reset_link):
    subject = "Library System Password Reset Request"
    content = f"You requested a password reset. Click the following link to reset your password:\n\n{reset_link}\n\nThis link will expire in 1 hour."
    return send_email(to_email, subject, content)

# <--- NEW: Function to verify Cloudflare Turnstile token
def verify_turnstile(token):
    if not token:
        print("Turnstile token is missing.")
        return False

    try:
        response = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": CLOUDFLARE_SECRET_KEY,
                "response": token
            }
        )
        result = response.json()
        if result.get("success"):
            print("Turnstile verification successful.")
            return True
        else:
            print(f"Turnstile verification failed: {result.get('error-codes')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Cloudflare Turnstile API: {e}")
        return False
    except ValueError as e: # For JSON decoding errors
        print(f"Failed to decode Turnstile API response: {e}")
        return False


@app.route('/')
def home():
    return "✅ Flask backend is running!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    turnstile_token = data.get('turnstile_token') # <--- NEW: Get token from request

    # <--- NEW: Validate Turnstile token
    if not verify_turnstile(turnstile_token):
        return jsonify({"error": "CAPTCHA verification failed. Please try again."}), 400

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        conn = db_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already registered"}), 409

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed))

        conn.commit()
        return jsonify({"message": "✅ Registered successfully!"}), 200

    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    turnstile_token = data.get('turnstile_token') # <--- NEW: Get token from request

    # <--- NEW: Validate Turnstile token
    if not verify_turnstile(turnstile_token):
        return jsonify({"error": "CAPTCHA verification failed. Please try again."}), 400

    try:
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result or not bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            return jsonify({"error": "Invalid credentials"}), 401

        otp = str(secrets.randbelow(1000000)).zfill(6)
        OTP_STORE[email] = otp

        if not send_otp_email(email, otp):
            return jsonify({"error": "Failed to send OTP email"}), 500

        return jsonify({"message": "OTP sent to your email"}), 200

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data['email']
    otp = data['otp']

    if OTP_STORE.get(email) == otp:
        del OTP_STORE[email] # OTP consumed
        return jsonify({"message": "✅ Login Successful!"}), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 401

# --- New Forgot Password functionality ---

@app.route('/forgot-password-request', methods=['POST'])
def forgot_password_request():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        conn = db_conn()
        cursor = conn.cursor()

        # Check if email exists
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        user_exists = cursor.fetchone()
        if not user_exists:
            # For security, don't confirm if email exists or not
            return jsonify({"message": "If the email is registered, a password reset link has been sent."}), 200

        # Generate a unique token
        token = secrets.token_urlsafe(32) # Generate a secure URL-safe token
        
        # Set expiration time (e.g., 1 hour from now)
        # Make datetime objects timezone-aware to avoid comparison issues with PostgreSQL
        utc_now = datetime.now(pytz.utc)
        expires_at = utc_now + timedelta(hours=1)

        # Store token in database
        cursor.execute(
            "INSERT INTO password_resets (token, user_email, expires_at) VALUES (%s, %s, %s)",
            (token, email, expires_at)
        )
        conn.commit()

        # Construct the reset link (adjust 'http://localhost:8000' to your frontend URL)
        reset_link = f"http://localhost:8000/reset_password.html?token={token}"

        # Send email with reset link
        if send_password_reset_email(email, reset_link):
            return jsonify({"message": "If the email is registered, a password reset link has been sent."}), 200
        else:
            return jsonify({"error": "Failed to send password reset email."}), 500

    except Exception as e:
        print(f"Forgot password request error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    try:
        conn = db_conn()
        cursor = conn.cursor()

        # Find the token and check expiration
        cursor.execute(
            "SELECT user_email, expires_at FROM password_resets WHERE token = %s",
            (token,)
        )
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Invalid or expired token."}), 400

        user_email, expires_at_db = result
        
        # Make expires_at_db timezone-aware if it's not already from the DB
        # Assume DB stores UTC, convert to UTC timezone-aware object for comparison
        if expires_at_db.tzinfo is None:
            expires_at_db = pytz.utc.localize(expires_at_db)

        utc_now = datetime.now(pytz.utc)

        if utc_now > expires_at_db:
            # Delete expired token
            cursor.execute("DELETE FROM password_resets WHERE token = %s", (token,))
            conn.commit()
            return jsonify({"error": "Invalid or expired token."}), 400

        # Hash new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Update user's password
        cursor.execute(
            "UPDATE users SET password = %s WHERE email = %s",
            (hashed_password, user_email)
        )

        # Invalidate/delete the token after successful use
        cursor.execute("DELETE FROM password_resets WHERE token = %s", (token,))
        conn.commit()

        return jsonify({"message": "Password reset successfully!"}), 200

    except Exception as e:
        print(f"Reset password error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)