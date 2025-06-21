// js/auth.js

// Helper function to display registration errors
function displayRegisterError(message) {
    const errorMessageElement = document.getElementById("registerErrorMessage");
    if (errorMessageElement) {
        errorMessageElement.textContent = "❌ " + message;
        errorMessageElement.style.display = "block";
    }
    // Ensure success message is hidden if an error occurs
    document.getElementById("successMessage").style.display = "none";
}

// Helper function to clear registration errors
function clearRegisterError() {
    const errorMessageElement = document.getElementById("registerErrorMessage");
    if (errorMessageElement) {
        errorMessageElement.textContent = "";
        errorMessageElement.style.display = "none";
    }
}

async function registerUser(event) {
    event.preventDefault();
    clearRegisterError(); // Clear previous errors
    document.getElementById("successMessage").style.display = "none"; // Hide success message on new attempt

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;
    // --- NEW/UPDATED: Get the Turnstile token ---
    const turnstileToken = document.querySelector('[name="cf-turnstile-response"]').value;

    if (password !== confirmPassword) {
        displayRegisterError("Passwords do not match."); // Use display function
        return;
    }

    // --- NEW/UPDATED: Check if Turnstile token is present ---
    if (!turnstileToken) {
        displayRegisterError("Please complete the CAPTCHA challenge.");
        // Optional: Call turnstile.reset() if the challenge didn't even appear properly
        if (typeof turnstile !== 'undefined') {
            turnstile.reset();
        }
        return;
    }

    try {
        const res = await fetch("http://localhost:5000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            // --- NEW/UPDATED: Include the Turnstile token in the request body ---
            body: JSON.stringify({ email, password, turnstile_token: turnstileToken })
        });

        const data = await res.json();

        if (res.ok) {
            document.getElementById("successMessage").style.display = "block";
            document.getElementById("registerForm").reset();
            // --- NEW/UPDATED: Reset Turnstile widget after successful submission ---
            if (typeof turnstile !== 'undefined') {
                turnstile.reset();
            }
        } else {
            displayRegisterError(data.error || "Registration failed."); // Use display function
            // --- NEW/UPDATED: Reset Turnstile widget on failure ---
            if (typeof turnstile !== 'undefined') {
                turnstile.reset();
            }
        }
    } catch (error) {
        displayRegisterError("Error connecting to backend or an unknown error occurred.");
        console.error('Fetch error:', error);
        // --- NEW/UPDATED: Reset Turnstile widget on error ---
        if (typeof turnstile !== 'undefined') {
            turnstile.reset();
        }
    }
}