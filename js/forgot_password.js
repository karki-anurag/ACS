// js/forgot_password.js

async function requestPasswordReset(event) {
    event.preventDefault();
    const email = document.getElementById('forgot_email').value;
    const messageElement = document.getElementById('forgotMessage');
    const errorMessageElement = document.getElementById('forgotErrorMessage');

    messageElement.style.display = 'none';
    errorMessageElement.style.display = 'none';
    messageElement.textContent = '';
    errorMessageElement.textContent = '';

    try {
        const response = await fetch('http://127.0.0.1:5000/forgot-password-request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email }),
        });

        const result = await response.json();

        if (response.ok) {
            messageElement.textContent = result.message;
            messageElement.style.display = 'block';
            document.getElementById('forgotPasswordForm').reset();
        } else {
            errorMessageElement.textContent = result.error || 'Failed to send reset link.';
            errorMessageElement.style.display = 'block';
        }
    } catch (error) {
        errorMessageElement.textContent = 'Error connecting to the server. Please try again.';
        errorMessageElement.style.display = 'block';
        console.error('Fetch error:', error);
    }
    return false; // Prevent default form submission
}