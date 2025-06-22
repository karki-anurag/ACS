from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import psycopg2
import secrets
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import pytz # Import pytz for timezone aware datetime
import requests # Import requests library for Turnstile verification

app = Flask(__name__)
CORS(app)

# Database Credentials - IMPORTANT: Update these with your actual details
DB_USER = "karki"
DB_PASSWORD = "karkisir123"
DB_HOST = "localhost"
DB_NAME = "anurag"

# Email Credentials - IMPORTANT: Update these
GMAIL_USER = "anuragkarki2004@gmail.com"
GMAIL_APP_PASSWORD = "zbsmjsqdvuymkbth" # Use an App Password if 2FA is enabled on Gmail

# Cloudflare Turnstile Secret Key - IMPORTANT: Update this with YOUR SECRET KEY
CLOUDFLARE_SECRET_KEY = "0x4AAAAAABho5r4yvWGIVblav4Dx0tdTAGk" # <<--- REPLACE THIS WITH YOUR ACTUAL SECRET KEY!

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

# Function to verify Cloudflare Turnstile token
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

# --- Helper to check password history ---
def is_password_reused(email, new_password, cursor):
    """Checks if the new_password is among the last 3 used by the user."""
    cursor.execute(
        "SELECT password FROM password_history WHERE email = %s ORDER BY changed_at DESC LIMIT 3",
        (email,)
    )
    rows = cursor.fetchall()
    for old_hashed_password in rows:
        if bcrypt.checkpw(new_password.encode('utf-8'), old_hashed_password[0].encode('utf-8')):
            return True
    return False


@app.route('/')
def home():
    return "✅ Flask backend is running!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    turnstile_token = data.get('turnstile_token')

    # Validate Turnstile token
    if not verify_turnstile(turnstile_token):
        return jsonify({"error": "CAPTCHA verification failed. Please try again."}), 400

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        conn = db_conn()
        cursor = conn.cursor()

        # Check if email already registered
        cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already registered"}), 409

        # --- Check password reuse during registration ---
        # First, check if the user exists to get their password history.
        # If user doesn't exist yet, there's no history to check against.
        # This prevents an error if password_history table is empty for new user.
        cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        user_exists_in_users = cursor.fetchone()
        if user_exists_in_users: # Only check history if user already exists
            if is_password_reused(email, password, cursor):
                return jsonify({"error": "Cannot reuse last 3 passwords"}), 400

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert/Update user and record last_password_change
        # Use ON CONFLICT if you plan to re-register existing emails for some reason,
        # otherwise a simple INSERT is fine if you've already checked for existence.
        cursor.execute("""
            INSERT INTO users (email, password, created_at, last_password_change)
            VALUES (%s, %s, NOW(), NOW())
            ON CONFLICT (email) DO UPDATE SET password = EXCLUDED.password, last_password_change = NOW()
        """, (email, hashed))

        # Record password in history
        cursor.execute("""
            INSERT INTO password_history (email, password, changed_at)
            VALUES (%s, %s, NOW())
        """, (email, hashed))

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
    email = data.get('email')
    password = data.get('password')
    turnstile_token = data.get('turnstile_token')

    # Validate Turnstile token
    if not verify_turnstile(turnstile_token):
        return jsonify({"error": "CAPTCHA verification failed. Please try again."}), 400

    try:
        conn = db_conn()
        cursor = conn.cursor()
        # Retrieve password AND last_password_change
        cursor.execute("SELECT password, last_password_change FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result or not bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            return jsonify({"error": "Invalid credentials"}), 401

        user_hashed_password, last_password_change = result

        # --- NEW: Check for 90-day password expiry ---
        utc_now = datetime.now(pytz.utc)
        # Ensure last_password_change is timezone-aware for correct comparison
        # Assuming last_password_change from DB is UTC or converted to UTC without tzinfo for simplicity
        if last_password_change.tzinfo is None:
            last_password_change = pytz.utc.localize(last_password_change)

        if (utc_now - last_password_change) > timedelta(days=90):
            return jsonify({"error": "Your password has expired. Please reset your password."}), 403

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
    email = data.get('email')
    otp = data.get('otp')

    if OTP_STORE.get(email) == otp:
        del OTP_STORE[email] # OTP consumed
        return jsonify({"message": "✅ Login Successful!"}), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 401

@app.route('/forgot-password-request', methods=['POST'])
def forgot_password_request():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        conn = db_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        user_exists = cursor.fetchone()
        if not user_exists:
            return jsonify({"message": "If the email is registered, a password reset link has been sent."}), 200

        token = secrets.token_urlsafe(32)
        
        utc_now = datetime.now(pytz.utc)
        expires_at = utc_now + timedelta(hours=1)

        cursor.execute(
            "INSERT INTO password_resets (token, user_email, expires_at) VALUES (%s, %s, %s)",
            (token, email, expires_at)
        )
        conn.commit()

        reset_link = f"http://localhost:8000/reset_password.html?token={token}"

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

        cursor.execute(
            "SELECT user_email, expires_at FROM password_resets WHERE token = %s",
            (token,)
        )
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Invalid or expired token."}), 400

        user_email, expires_at_db = result
        
        if expires_at_db.tzinfo is None:
            expires_at_db = pytz.utc.localize(expires_at_db)

        utc_now = datetime.now(pytz.utc)

        if utc_now > expires_at_db:
            cursor.execute("DELETE FROM password_resets WHERE token = %s", (token,))
            conn.commit()
            return jsonify({"error": "Invalid or expired token."}), 400

        # --- NEW: Check password reuse during password reset ---
        if is_password_reused(user_email, new_password, cursor):
            return jsonify({"error": "Cannot reuse last 3 passwords"}), 400

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute(
            "UPDATE users SET password = %s, last_password_change = NOW() WHERE email = %s", # <--- UPDATED: Set last_password_change to NOW()
            (hashed_password, user_email)
        )

        cursor.execute("""
            INSERT INTO password_history (email, password, changed_at)
            VALUES (%s, %s, NOW())
        """, (user_email, hashed_password)) # <--- NEW: Add new password to history

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