const API_URL = "http://localhost:8000/chat";

function enterApp() {
    document.getElementById('landing-page').style.transform = "translateY(-100%)";
    setTimeout(() => {
        document.getElementById('landing-page').style.display = "none";
        document.getElementById('app-container').classList.remove('hidden');
    }, 500);
}

function handleEnter(e) {
    if (e.key === 'Enter') sendMessage();
}

function sendQuickMsg(text) {
    document.getElementById('user-input').value = text;
    sendMessage();
}

async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const message = inputField.value.trim();
    if (!message) return;

    // Add User Message
    addMessage(message, 'user');
    inputField.value = '';

    // Show Typing Indicator
    const typingId = addTypingIndicator();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        
        // Remove Typing Indicator and Add Bot Message
        removeMessage(typingId);
        addMessage(data.reply, 'bot');
    } catch (error) {
        removeMessage(typingId);
        addMessage("⚠️ Server error. Is the backend running?", 'bot');
    }
}

function addMessage(text, sender) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    
    // Convert markdown bold to HTML bold (Simple regex)
    const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
    
    msgDiv.innerHTML = `<p>${formattedText}</p><span class="time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv.id = 'msg-' + Date.now();
}

function addTypingIndicator() {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message bot`;
    msgDiv.id = 'typing-' + Date.now();
    msgDiv.innerHTML = `<p>Typing... <i class="fas fa-circle-notch fa-spin"></i></p>`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv.id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

async function fetchComplaints() {
    // Simple Admin Fetch for Demo
    const response = await fetch("http://localhost:8000/admin/complaints");
    const data = await response.json();
    let report = "📋 **Active Complaints:**\n";
    data.complaints.forEach(c => {
        report += `- [#${c[0]}] ${c[2]} (Status: ${c[3]})\n`;
    });
    addMessage(report, 'bot');
}

const AUTH_URL = "http://localhost:8000";

// --- Auth Logic (Updated for Email) ---

async function handleLogin() {
    const email = document.getElementById('auth-email').value; // Get the email
    const pass = document.getElementById('auth-password').value;
    const msg = document.getElementById('auth-msg');

    if (!email || !pass) {
        msg.innerText = "Please enter email and password";
        return;
    }

    try {
        const response = await fetch(`${AUTH_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: pass }) // Send 'email'
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('auth-overlay').style.display = 'none';
            // Show the name part of the email (e.g., "pranjal" from "pranjal@college.edu")
            const display_name = email.split('@')[0];
            document.querySelector('.user-info span').innerText = display_name;
        } else {
            msg.style.color = "red";
            msg.innerText = `❌ ${data.detail || "Invalid Credentials"}`;
        }
    } catch (e) {
        msg.innerText = "⚠️ Server Error. Check Backend.";
    }
}

async function handleRegister() {
    const email = document.getElementById('auth-email').value; // Get the email
    const pass = document.getElementById('auth-password').value;
    const msg = document.getElementById('auth-msg');

    if (!email || !pass) { 
        msg.innerText = "Please fill all fields"; 
        return; 
    }

    try {
        const response = await fetch(`${AUTH_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: pass }) // Send 'email'
        });

        const data = await response.json();

        if (response.ok) {
            msg.style.color = "green";
            msg.innerText = "✅ Account Created! Please Sign In.";
        } else {
            msg.style.color = "red";
            msg.innerText = `❌ ${data.detail || "Registration failed"}`;
        }
    } catch (e) {
        console.error(e);
        msg.innerText = "⚠️ Server Error (Check Backend Console)";
    }
}