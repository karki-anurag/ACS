
function checkStrength() {
    const password = document.getElementById("password").value;
    const strengthText = document.getElementById("strengthIndicator");

    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    const levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"];
    const colors = ["#ff4d4d", "#ff944d", "#ffff66", "#99e699", "#66ff99"];

    strengthText.textContent = "Password Strength: " + levels[strength - 1] || "Too Short";
    strengthText.style.color = colors[strength - 1] || "#ccc";
}
