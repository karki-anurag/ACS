// js/reset_password.js

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Optional: Password strength check for reset page
function checkStrengthReset() {
    const password = document.getElementById("new_password").value;
    const strengthText = document.getElementById("strengthIndicatorReset");

    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    const levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"];
    // These colors should match your style.css strength indicator colors if you want consistency
    const colors = ["#ff6666", "#ff9966", "#ffff99", "#99ff99", "#66ffcc"]; 

    if (password.length > 0) {
        strengthText.textContent = "Password Strength: " + levels[strength - 1];
        strengthText.style.color = colors[strength - 1];
    } else {
        strengthText.textContent = "";
        strengthText.style.color = "#fdfaf6"; // Default color when empty
    }
}


async function resetUserPassword(event) {
    event.preventDefault();
    const token = getQueryParam('token');
    const newPassword = document.getElementById('new_password').value;
    const confirmNewPassword = document.getElementById('confirm_new_password').value;
    const messageElement = document.getElementById('resetMessage');
    const errorMessageElement = document.getElementById('resetErrorMessage');

    messageElement.style.display = 'none';
    errorMessageElement.style.display = 'none';
    messageElement.textContent = '';
    errorMessageElement.textContent = '';

    if (!token) {
        errorMessageElement.textContent = 'Invalid or missing reset token.';
        errorMessageElement.style.display = 'block';
        return false;
    }

    if (newPassword !== confirmNewPassword) {
        errorMessageElement.textContent = 'Passwords do not match.';
        errorMessageElement.style.display = 'block';
        return false;
    }
    
    // Basic password strength check (you can enhance this using your password.js logic)
    if (newPassword.length < 8) {
        errorMessageElement.textContent = 'Password must be at least 8 characters long.';
        errorMessageElement.style.display = 'block';
        return false;
    }


    try {
        const response = await fetch('http://127.0.0.1:5000/reset-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token, new_password: newPassword }),
        });

        const result = await response.json();

        if (response.ok) {
            messageElement.textContent = result.message + ' Redirecting to login...';
            messageElement.style.display = 'block';
            document.getElementById('resetPasswordForm').reset();
            // Redirect to login page after a short delay
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 3000);
        } else {
            errorMessageElement.textContent = result.error || 'Failed to reset password.';
            errorMessageElement.style.display = 'block';
        }
    } catch (error) {
        errorMessageElement.textContent = 'Error connecting to the server. Please try again.';
        errorMessageElement.style.display = 'block';
        console.error('Fetch error:', error);
    }
    return false; // Prevent default form submission
}