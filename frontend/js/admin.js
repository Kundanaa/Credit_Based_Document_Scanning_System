// admin.js

API_URL = "http://localhost:5000";

// Admin Login
function adminLogin() {
    const username = document.getElementById("adminUsername").value;
    const password = document.getElementById("adminPassword").value;

    fetch(`${API_URL}/admin/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById("adminMessage").innerText = "Login successful!";
            document.querySelector(".container").style.display = "none";
            document.getElementById("dashboard").style.display = "block";
            loadAdminDashboard();
        } else {
            document.getElementById("adminMessage").innerText = "Invalid login credentials.";
        }
    })
    .catch(error => console.error("Error:", error));
}

// Load Admin Dashboard Data
function loadAdminDashboard() {
    fetch(`${API_URL}/admin/analytics`)
    .then(response => response.json())
    .then(data => {
        document.getElementById("totalUsers").innerText = data.total_users;
        document.getElementById("pendingRequests").innerText = data.pending_credit_requests;

        let userCreditList = document.getElementById("userCreditList");
        userCreditList.innerHTML = "";
        data.user_credits.forEach(user => {
            let listItem = document.createElement("li");
            listItem.textContent = `${user.username}: ${user.credits} credits`;
            userCreditList.appendChild(listItem);
        });

        loadPendingCreditRequests();
    });
}

// Load Pending Credit Requests
function loadPendingCreditRequests() {
    fetch(`${API_URL}/admin/analytics`)
    .then(response => response.json())
    .then(data => {
        let tableBody = document.getElementById("creditRequestsTable");
        tableBody.innerHTML = "";

        data.user_credits.forEach(request => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${request.username}</td>
                <td>${request.credits}</td>
                <td>
                    <button onclick="processCreditRequest(${request.id}, 'approve')">Approve</button>
                    <button onclick="processCreditRequest(${request.id}, 'reject')">Reject</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    });
}

// Approve or Reject Credit Request
function processCreditRequest(requestId, action) {
    fetch(`${API_URL}/admin/credits/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ request_id: requestId, action })
    })
    .then(response => response.json())
    .then(() => loadAdminDashboard());
}

/*async function fetchAdminAnalytics() {
    let token = localStorage.getItem("token");

    let response = await fetch("http://localhost:5000/admin/analytics", {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` }
    });

    let data = await response.json();
    if (response.ok) {
        document.getElementById("analyticsDisplay").innerText = JSON.stringify(data, null, 2);
    } else {
        alert("Failed to load analytics.");
    }
}

document.addEventListener("DOMContentLoaded", fetchAdminAnalytics);
*/