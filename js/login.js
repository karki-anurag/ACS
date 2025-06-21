// Helper function to display errors
function displayLoginError(message) {
    const errorMessageElement = document.getElementById("loginErrorMessage");
    if (errorMessageElement) {
        errorMessageElement.textContent = "❌ " + message;
        errorMessageElement.style.display = "block";
    }
}

// Helper function to clear login errors
function clearLoginError() {
    const errorMessageElement = document.getElementById("loginErrorMessage");
    if (errorMessageElement) {
        errorMessageElement.textContent = "";
        errorMessageElement.style.display = "none";
    }
}

// Helper function to display OTP errors
function displayOtpError(message) {
    const errorMessageElement = document.getElementById("otpErrorMessage");
    if (errorMessageElement) {
        errorMessageElement.textContent = "❌ " + message;
        errorMessageElement.style.display = "block";
    }
}

// Helper function to clear OTP errors
function clearOtpError() {
    const errorMessageElement = document.getElementById("otpErrorMessage");
    if (errorMessageElement) {
        errorMessageElement.textContent = "";
        errorMessageElement.style.display = "none";
    }
}

async function loginUser(event) {
  event.preventDefault();
  clearLoginError(); // Clear previous errors
  const email = document.getElementById("login_email").value;
  const password = document.getElementById("login_password").value;

  // Show OTP section immediately and disable login form
  document.getElementById("otpSection").style.display = "block";
  document.getElementById("loginForm").style.pointerEvents = "none";
  document.getElementById("otpMessage").textContent = "Sending OTP...";

  try {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const result = await response.json();

    if (response.ok) {
      document.getElementById("otpMessage").textContent = result.message;
      // The OTP section should already be visible from the line above
    } else {
      displayLoginError(result.error || "Login failed."); // Use display function
      document.getElementById("otpSection").style.display = "none"; // Hide on error
      document.getElementById("loginForm").style.pointerEvents = "auto";
    }
  } catch (err) {
    displayLoginError("Error connecting to backend."); // Use display function
    console.error(err);
    document.getElementById("otpSection").style.display = "none"; // Hide on network error
    document.getElementById("loginForm").style.pointerEvents = "auto";
  }
}

async function verifyOTP() {
  clearOtpError(); // Clear previous OTP errors
  const email = document.getElementById("login_email").value;
  const otp = document.getElementById("otp").value;

  try {
    const response = await fetch("http://127.0.0.1:5000/verify-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, otp }),
    });

    const result = await response.json();

    if (response.ok) {
      alert("✅ Login Successful! Redirecting to dashboard..."); // Still using alert for success
      // window.location.href = 'dashboard.html'; // Redirect to dashboard
    } else {
      displayOtpError(result.error || "OTP verification failed."); // Use display function
    }
  } catch (err) {
    displayOtpError("Error verifying OTP."); // Use display function
    console.error(err);
  }
}