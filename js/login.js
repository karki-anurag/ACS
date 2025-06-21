// js/login.js

// Helper function to display login errors (optional, similar to auth.js)
function displayLoginError(message) {
    const errorMessageElement = document.getElementById("loginErrorMessage"); // Assuming you add this ID in index.html
    if (errorMessageElement) {
        errorMessageElement.textContent = "❌ " + message;
        errorMessageElement.style.display = "block";
    }
}

// Helper function to clear login errors (optional)
function clearLoginError() {
    const errorMessageElement = document.getElementById("loginErrorMessage");
    if (errorMessageElement) {
        errorMessageElement.textContent = "";
        errorMessageElement.style.display = "none";
    }
}


async function loginUser(event) {
  event.preventDefault();
  clearLoginError(); // Clear previous errors (if implemented)

  const email = document.getElementById("login_email").value;
  const password = document.getElementById("login_password").value;
  // --- NEW/UPDATED: Get the Turnstile token ---
  const turnstileToken = document.querySelector('[name="cf-turnstile-response"]').value;

  // --- NEW/UPDATED: Check if Turnstile token is present ---
  if (!turnstileToken) {
      displayLoginError("Please complete the CAPTCHA challenge."); // Use display function
      if (typeof turnstile !== 'undefined') {
          turnstile.reset();
      }
      return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      // --- NEW/UPDATED: Include the Turnstile token in the request body ---
      body: JSON.stringify({ email, password, turnstile_token: turnstileToken }),
    });

    const result = await response.json();

    if (response.ok) {
      alert(result.message); // Could use a displayLoginSuccess function here
      document.getElementById("otpSection").style.display = "block";
      // --- NEW/UPDATED: Reset Turnstile widget after successful submission ---
      if (typeof turnstile !== 'undefined') {
           turnstile.reset();
      }
    } else {
      displayLoginError(result.error); // Use display function
       // --- NEW/UPDATED: Reset Turnstile widget on failure ---
      if (typeof turnstile !== 'undefined') {
           turnstile.reset();
      }
    }
  } catch (err) {
    displayLoginError("Error connecting to backend or an unknown error occurred.");
    console.error(err);
     // --- NEW/UPDATED: Reset Turnstile widget on error ---
    if (typeof turnstile !== 'undefined') {
         turnstile.reset();
    }
  }
}

async function verifyOTP() {
  // Ensure the email is still accessible, or pass it from loginUser
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