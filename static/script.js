console.log("JS Loaded 🚀");


// -------------------------------
// SEND MESSAGE
// -------------------------------
function sendMessage() {
    let input = document.getElementById("messageInput");
    let msg = input.value.trim();

    if (msg === "") return;

    // show user message
    addMessage(msg, "user");

    // clear input
    input.value = "";

    fetch("/api/chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: msg,
            user_id: "rahul"
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("API RESPONSE:", data);

        if (data.response) {
            addMessage(data.response, "bot");
        } else {
            addMessage("No response from server ❌", "bot");
        }
    })
    .catch(error => {
        console.error("Chat Error:", error);
        addMessage("Server error 😢", "bot");
    });
}


// -------------------------------
// ADD MESSAGE TO CHAT
// -------------------------------
function addMessage(msg, type) {
    let chatBox = document.getElementById("chatBox");

    let div = document.createElement("div");

    div.className = (type === "user") ? "user-message" : "bot-message";
    div.innerText = msg;

    chatBox.appendChild(div);

    // smooth scroll
    chatBox.scrollTop = chatBox.scrollHeight;
}


// -------------------------------
// FILE UPLOAD
// -------------------------------
function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select a file ❗");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    fetch("/api/upload/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Upload Response:", data);

        alert("File uploaded successfully ✅");

        // 👇 show message in chat UI
        addMessage("📄 File uploaded successfully!", "bot");
    })
    .catch(error => {
        console.error("Upload Error:", error);
        alert("Upload failed ❌");
    });
}


// -------------------------------
// ENTER KEY SUPPORT
// -------------------------------
document.getElementById("messageInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});