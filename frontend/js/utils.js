// Function to get token from localStorage
function getToken() {
    return localStorage.getItem("token");
}

// Logout function
// document.getElementById("logoutBtn").addEventListener("click", function () {
//     localStorage.removeItem("token");
//     window.location.href = "index.html";
// });
document.addEventListener("DOMContentLoaded", function () {
    let logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function () {
            localStorage.removeItem("token");
            window.location.href = "index.html";  // Redirect to login page
        });
    }
});
