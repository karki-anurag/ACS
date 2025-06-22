// js/login.js

// Helper function to display login errors
function displayLoginError(message) {
    const errorMessageElement = document.getElementById("loginErrorMessage");
    // Ensure you have a <p id="loginErrorMessage" style="color: red;"></p> in your index.html
    if (errorMessageElement) {
        errorMessageElement.textContent =  message;
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


async function loginUser(event) {
  event.preventDefault();
  clearLoginError(); // Clear previous errors

  const email = document.getElementById("login_email").value;
  const password = document.getElementById("login_password").value;
  // Get the Turnstile token
  const turnstileToken = document.querySelector('[name="cf-turnstile-response"]').value;

  // Check if Turnstile token is present
  if (!turnstileToken) {
      displayLoginError("Please complete the CAPTCHA challenge.");
      if (typeof turnstile !== 'undefined') {
          turnstile.reset();
      }
      return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, turnstile_token: turnstileToken }),
    });

    const result = await response.json();

    if (response.ok) {
      alert(result.message);
      document.getElementById("otpSection").style.display = "block";
      // Reset Turnstile widget after successful submission
      if (typeof turnstile !== 'undefined') {
           turnstile.reset();
      }
    } else {
      // --- NEW/UPDATED: Specific handling for password expiry ---
      if (response.status === 403 && result.error === "Your password has expired. Please reset your password.") {
        displayLoginError("Your password has expired. Please reset it.");
        alert("Your password has expired. You will be redirected to the password reset page.");
        // Redirect to the forgot password page
        window.location.href = 'forgot_password.html'; // Make sure you have this HTML file
      } else {
        // General error handling
        displayLoginError(result.error);
      }
      
      // Reset Turnstile widget on failure
      if (typeof turnstile !== 'undefined') {
           turnstile.reset();
      }
    }
  } catch (err) {
    displayLoginError("Error connecting to backend or an unknown error occurred.");
    console.error(err);
    // Reset Turnstile widget on error
    if (typeof turnstile !== 'undefined') {
         turnstile.reset();
    }
  }
}

async function verifyOTP() {
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
      alert("✅ Login Successful!");
      window.location.href = 'dashboard.html'; // Redirect to dashboard
    } else {
      alert("❌ " + result.error);
    }
  } catch (err) {
    alert("❌ Error verifying OTP.");
    console.error(err);
  }
}