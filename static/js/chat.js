(function() {
    // DOM elements
    const chatToggle = document.getElementById("chat-toggle");
    const chatPopup = document.getElementById("chat-popup");
    const chatClose = document.getElementById("chat-close");
    const prechatForm = document.getElementById("prechat-form");
    const chatWidget = document.getElementById("chat-widget");
    const chatMessages = document.getElementById("chat-messages");
    const chatInput = document.getElementById("chatInput");
    let socket;
    let userChatHistory = [];
  
    // Chat history functions
    function loadUserChatHistory() {
      const stored = localStorage.getItem("user_chat_history");
      if (stored) {
        try {
          userChatHistory = JSON.parse(stored);
        } catch (e) {
          userChatHistory = [];
        }
        userChatHistory.forEach(appendMessage);
      }
    }
  
    function saveUserChatHistory() {
      localStorage.setItem("user_chat_history", JSON.stringify(userChatHistory));
    }
  
    function appendMessage(data) {
      const messageDiv = document.createElement("div");
      messageDiv.textContent = `${data.sender}: ${data.msg}`;
      chatMessages.appendChild(messageDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  
    // Chat initialization
    function initChat(name, email, phone) {
      const query = `user_type=user&name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&phone=${encodeURIComponent(phone)}`;
      socket = io({ query });
      socket.on("connect", () => {
        console.log(`Connected to live chat as ${name}`);
      });
      socket.on("chat_message", (data) => {
        data.sender = data.sender || name;
        userChatHistory.push(data);
        saveUserChatHistory();
        appendMessage(data);
      });
      socket.on("pastor_status", (data) => {
        const statusDot = document.getElementById("pastor-status-dot");
        statusDot.style.backgroundColor = (data.status === "online") ? "green" : "red";
        statusDot.style.display = "inline-block";
      });
      loadUserChatHistory();
    }
  
    // Toggle chat popup visibility
    function toggleChat() {
      chatPopup.style.display = (chatPopup.style.display === "none" || chatPopup.style.display === "") ? "block" : "none";
    }
  
    // Event listeners
    chatToggle.addEventListener("click", toggleChat);
    chatClose.addEventListener("click", () => {
      chatPopup.style.display = "none";
    });
    prechatForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = document.getElementById("userName").value.trim();
      const email = document.getElementById("userEmail").value.trim();
      const phone = document.getElementById("userPhone").value.trim();
      if (!name || !email || !phone) {
        alert("Please fill in all fields.");
        return;
      }
      document.getElementById("prechat-form-container").style.display = "none";
      chatWidget.style.display = "block";
      initChat(name, email, phone);
    });
  
    // Global send message function
    window.sendMessage = function() {
      const message = chatInput.value.trim();
      if (message && socket) {
        socket.emit("chat_message", { msg: message });
        chatInput.value = "";
      }
    };
  })();
  