document.getElementById("scanForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    let fileInput = document.getElementById("documentUpload");
    const userId = localStorage.getItem("user_id"); // Assuming user_id is stored in localStorage
    console.log("Retrieved user_id:", userId); // 🔍 Debugging
    if (!userId) {
        alert("User not logged in");
        return;
    }

    let formData = new FormData();
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload a document first.");
        return;
    }
    formData.append("file", fileInput.files[0]);
    
    //formData.append("user_id", userId);  // Add user_id
    formData.append("user_id", userId);  // ✅ Add user_id to FormData
    console.log("Sending data:", [...formData.entries()]); // ✅ Debugging

    let token = localStorage.getItem("token");
    let loadingIndicator = document.getElementById("loading");
    let resultList = document.getElementById("scanResult");

    if (loadingIndicator) loadingIndicator.style.display = "block";  // Show loading indicator
    if (resultList) resultList.innerHTML = "";   
    let uploadResponse, uploadData; 
    try {
        uploadResponse = await fetch("http://localhost:5000/scan/upload", {
            method: "POST",
            headers: { 
                "Authorization": `Bearer ${token}`,
                "User-ID": userId // ✅ Move user_id to headers
            },
            credentials: 'include',
            body: formData
        });

        uploadData = await uploadResponse.json();
        console.log("Upload Response:", uploadData);

        if (!uploadResponse.ok) {
            alert("Upload Failed: " + uploadData.message);
            return;
        }

        alert("Document Uploaded Successfully!");

        // Step 2: Extract Document Text
        let documentText = uploadData.document_text;  // Make sure backend returns this
        if (!documentText) {
            alert("Failed to retrieve document text.");
            return;
        }
        console.log("Extracted document text:", documentText);


        // Step 3: Fetch Matches
        fetchMatches(documentText);
        // const reader = new FileReader();
        // reader.onload = async function (e) {
        //     const documentText = e.target.result;
        //     document.getElementById("loading").style.display = "block"; // Show loading message
        
        //     await fetchMatches(documentText);

        //     document.getElementById("loading").style.display = "none"; // Hide loading message
        // };
        // reader.readAsText(file);
        
        // try {
        //     let data = JSON.parse(text);  // Try to parse as JSON
        //     if (response.ok) {
        //         alert("Document Scanned Successfully!");
        //         if (data.matches && data.matches.length > 0) {
        //             data.matches.forEach(match => {
        //                 let li = document.createElement("li");
        //                 li.innerText = `${match.filename} (Score: ${match.ai_score.toFixed(2)})`;
        //                 resultList.appendChild(li);
        //             });
        //         } else {
        //             resultList.innerHTML = "<li>No similar documents found.</li>";
        //         }
        //     } else {
        //         alert("Scan Failed: " + data.message);
        //     }
        // } catch (jsonError) {
        //     console.error("Failed to parse JSON:", jsonError);
        //     alert("An error occurred: Invalid response from server.");
        // }
    } catch (error) {
        console.error("Request failed:", error);
        alert("An error occurred: " + error.message);
    } finally {
        loadingIndicator.style.display = "none";
    }
});
// Add fetchMatches function here, outside the form event listener
async function fetchMatches(documentText) {
    console.log("Raw Document Text:", documentText); // 🔍 Debugging

    // Clean up text if necessary
    documentText = documentText.replace(/\.sc\//g, ""); 
    console.log("Cleaned Document Text:", documentText);

    let token = localStorage.getItem("token");
    let userId = localStorage.getItem("user_id");
    //let resultList = document.getElementById("scanResult");

    try {
        let matchResponse = await fetch("http://localhost:5000/scan/match", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            credentials: 'include',
            body: JSON.stringify({ document_text: documentText})
        });

        let matchData = await matchResponse.json();
        console.log("Match API Response:", matchData);

        if (!matchResponse.ok) {
            alert("Matching Failed: " + matchData.error);
            return;
        }
        displayMatches(matchData.matches);
        // Step 4: Display Matched Results
        // Call function to update the UI with match results
        
        // if (matchData.matches && matchData.matches.length > 0) {
        //     resultList.innerHTML = "";
        //     matchData.matches.forEach(match => {
        //         let li = document.createElement("li");
        //         li.innerText = `${match.filename} (AI Score: ${match.ai_score.toFixed(2)}, TF-IDF Score: ${match.tfidf_score.toFixed(2)})`;
        //         resultList.appendChild(li);
        //     });
        // } else {
        //     resultList.innerHTML = "<li>No similar documents found.</li>";
        // }
    } catch (error) {
        console.error("Failed to fetch matches:", error);
        alert("An error occurred while retrieving matches.");
    }
}
// Function to update UI with matches
function displayMatches(matches) {
    const resultsDiv = document.getElementById("matchResults");
    if (!matches || matches.length === 0) {
        resultsDiv.innerHTML = "<p>No matching documents found.</p>";
        return;
    }
    console.log("Updating UI with matches:", matches);
    let resultHTML = "<ul>";
    matches.forEach((match) => {
        resultHTML += `<li><strong>${match.filename}</strong> - TF-IDF Score: ${match.tfidf_score.toFixed(2)}, AI Score: ${match.ai_score.toFixed(2)}</li>`;
    });
    resultHTML += "</ul>";

    resultsDiv.innerHTML = resultHTML;
    console.log("matchResults div:", resultsDiv);
}
// function displayMatches(matches) {
//     console.log("displayMatches function called!");  // Debugging log
//     console.log("Matches received:", matches);  // Log matches received
//     const resultsBody = document.getElementById("matchResults");
//     if (!document.getElementById("matchResults")) console.error("matchResults tbody not found!");

//     // Clear previous results
//     resultsBody.innerHTML = "";
//     if (!resultsBody) {
//         console.error("matchResults tbody not found in the DOM!");
//         return;
//     }

//     if (!matches || matches.length === 0) {
//         resultsBody.innerHTML = `<tr><td colspan="4">No matching documents found.</td></tr>`;
//         return;
//     }

//     console.log("Updating UI with matches:", matches);

//     // Adding rows dynamically based on matches
//     matches.forEach((match) => {
//         const fileLink = match.file_link ? 
//             `<a href="${match.file_link}" target="_blank">View File</a>` : 
//             "N/A";  // Handle missing file links
        
//         const row = `
//             <tr>
//                 <td>${match.filename}</td>
//                 <td>${match.tfidf_score.toFixed(2)}</td>
//                 <td>${match.ai_score.toFixed(2)}</td>
//                 <td>${fileLink}</td>
//             </tr>
//         `;
//         resultsBody.insertAdjacentHTML("beforeend", row);
//     });
//     console.log("Updated UI successfully.");
//     console.log("matchResults tbody updated:", resultsBody);
// }
