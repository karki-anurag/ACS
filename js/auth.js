// auth.js
// Helper function to display registration errors
function displayRegisterError(message) {
    const errorMessageElement = document.getElementById("registerErrorMessage");
    if (errorMessageElement) {
        errorMessageElement.textContent = "❌ " + message;
        errorMessageElement.style.display = "block";
    }
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

    if (password !== confirmPassword) {
        displayRegisterError("Passwords do not match."); // Use display function
        return;
    }

    const res = await fetch("http://localhost:5000/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (res.ok) {
        document.getElementById("successMessage").style.display = "block";
        document.getElementById("registerForm").reset();
    } else {
        displayRegisterError(data.error || "Registration failed."); // Use display function
    }
}