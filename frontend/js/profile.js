document.addEventListener("DOMContentLoaded", () => {
    fetchUserProfile();
});

async function fetchUserProfile() {
    const token = localStorage.getItem("token");
    if (!token) {
        console.error("🚨 No token found. Redirecting to login...");
        window.location.href = "index.html";  
        return;
    }
    try {
        // Decode the JWT Token
        let tokenPayload = JSON.parse(atob(token.split(".")[1]));
        let userId = tokenPayload.user_id; // Extract user_id from token

        if (userId) {
            localStorage.setItem("user_id", userId);
            console.log("User ID set:", userId);
        } else {
            console.error("User ID not found in token.");
        }
    } catch (error) {
        console.error("Error decoding token:", error);
    }

    console.log("📢 Sending Token:", token);  

    try {
        let response = await fetch("http://127.0.0.1:5000/user/profile", {
            method: "GET",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            credentials: "include"
        });

        console.log("📢 Response Status:", response.status);
        let textResponse = await response.text();
        console.log("📢 Raw Response:", textResponse);

        if (!response.ok) {
            throw new Error("Unauthorized access.");
        }

        let data = JSON.parse(textResponse);
        console.log("📢 User Profile Data:", data);

        document.getElementById("usernameDisplay").textContent = data.username;
        document.getElementById("creditsDisplay").textContent = `Credits: ${data.credits}`;
    } catch (error) {
        console.error("🚨 Error fetching profile:", error);
        alert("Session expired. Please log in again.");
        localStorage.removeItem("token");  
        window.location.href = "index.html";  
    }
}



