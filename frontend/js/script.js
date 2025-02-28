function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (username === "user" && password === "password") {
        localStorage.setItem("loggedInUser", username);
        window.location.href = "profile.html";
    } else {
        alert("Invalid credentials!");
    }
}

function requestCredits() {
    alert("Credit request sent to admin.");
}

function uploadDocument() {
    const fileInput = document.getElementById("document-upload");
    if (fileInput.files.length > 0) {
        alert("Document uploaded and scanned.");
    } else {
        alert("Please select a file.");
    }
}
