document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            let username = document.getElementById("username").value;
            let password = document.getElementById("password").value;

            try {
                let response = await fetch("http://localhost:5000/auth/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    credentials: "include",  // ✅ Important for sessions
                    body: JSON.stringify({ username, password })
                });

                console.log("Response Status:", response.status); // ✅ Debugging

                let data = await response.json();
                console.log("Login Response:", data);  // ✅ Debugging

                if (response.ok) {
                    if (data.token) {
                        localStorage.setItem("token", data.token);  // ✅ Ensure token is received
                        window.location.href = "profile.html";  
                    } else {
                        alert("Login Failed: Token missing in response.");
                    }
                } else {
                    alert("Login Failed: " + (data.message || "Unknown error"));
                }
            } catch (error) {
                console.error("Error during login:", error);
                alert("Server error. Please try again.");
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            let username = document.getElementById("username").value;
            let email = document.getElementById("email").value;
            let password = document.getElementById("password").value;

            try {
                let response = await fetch("http://localhost:5000/auth/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, email, password })
                });

                console.log("Response Status:", response.status); // ✅ Debugging
                let data = await response.json();
                console.log("Register Response:", data);  // ✅ Debugging

                if (response.ok) {
                    alert("Registration Successful! Please login.");
                    window.location.href = "index.html";  
                } else {
                    alert("Registration Failed: " + (data.message || "Unknown error"));
                }
            } catch (error) {
                console.error("Error during registration:", error);
                alert("Server error. Please try again.");
            }
        });
    }
});
