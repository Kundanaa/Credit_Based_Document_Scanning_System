// credits.js

const API_URL = "http://localhost:5000";

// Request Additional Credits
function requestCredits() {
    const creditsRequested = document.getElementById("creditAmount").value;

    fetch(`${API_URL}/credits/request`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("userToken")}`
        },
        body: JSON.stringify({ credits: parseInt(creditsRequested) })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("creditMessage").innerText = data.message;
    })
    .catch(error => console.error("Error:", error));
}

/*document.getElementById("requestCreditsBtn").addEventListener("click", async function () {
    let token = localStorage.getItem("token");

    let response = await fetch("http://localhost:5000/credits/request", {
        method: "POST",
        headers: { 
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    });

    let data = await response.json();
    if (response.ok) {
        alert("Credit Request Sent! Awaiting Admin Approval.");
    } else {
        alert("Failed to Request Credits: " + data.message);
    }
});*/
