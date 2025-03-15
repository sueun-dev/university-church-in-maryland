(function() {
    var socket;
    var userChatHistory = [];
  
    /**
     * Load chat history from localStorage and display in the chat widget.
     */
    function loadUserChatHistory() {
      var stored = localStorage.getItem('user_chat_history');
      if (stored) {
        try {
          userChatHistory = JSON.parse(stored);
        } catch(e) {
          userChatHistory = [];
        }
      }
      var chatMessages = document.getElementById('chat-messages');
      chatMessages.innerHTML = '';
      userChatHistory.forEach(function(message) {
        var div = document.createElement('div');
        div.textContent = message.sender + ': ' + message.msg;
        chatMessages.appendChild(div);
      });
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  
    /**
     * Save current chat history to localStorage.
     */
    function saveUserChatHistory() {
      localStorage.setItem('user_chat_history', JSON.stringify(userChatHistory));
    }
  
    /**
     * Append a new message to the chat display.
     * @param {Object} data - Message object containing sender and msg.
     */
    function appendUserMessage(data) {
      var chatMessages = document.getElementById('chat-messages');
      var newMessage = document.createElement('div');
      newMessage.textContent = data.sender + ': ' + data.msg;
      chatMessages.appendChild(newMessage);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  
    document.addEventListener("DOMContentLoaded", function() {
      loadUserChatHistory();
  
      document.getElementById("chat-toggle").addEventListener("click", function() {
        var popup = document.getElementById("chat-popup");
        popup.style.display = (popup.style.display === "none" || popup.style.display === "") ? "block" : "none";
      });
  
      document.getElementById("chat-close").addEventListener("click", function() {
        document.getElementById("chat-popup").style.display = "none";
      });
  
      document.getElementById("prechat-form").addEventListener("submit", function(e) {
        e.preventDefault();
        var name = document.getElementById("userName").value.trim();
        var email = document.getElementById("userEmail").value.trim();
        var phone = document.getElementById("userPhone").value.trim();
        if (!name || !email || !phone) {
          alert("Please fill in all fields.");
          return;
        }
        document.getElementById("prechat-form-container").style.display = "none";
        document.getElementById("chat-widget").style.display = "block";
  
        socket = io({ query: 'user_type=user&name=' + encodeURIComponent(name) +
                            '&email=' + encodeURIComponent(email) +
                            '&phone=' + encodeURIComponent(phone) });
  
        socket.on('connect', function() {
          console.log('Connected as ' + name);
        });
  
        socket.on('chat_message', function(data) {
          if (!data.sender) { data.sender = name; }
          userChatHistory.push(data);
          saveUserChatHistory();
          appendUserMessage(data);
        });
  
        socket.on('pastor_status', function(data) {
          var statusDot = document.getElementById("pastor-status-dot");
          statusDot.style.backgroundColor = data.status === 'online' ? 'green' : 'red';
          statusDot.style.display = 'inline-block';
        });
      });
  
      document.getElementById("chatInput").addEventListener("keydown", function(e) {
        if (e.key === "Enter") { sendMessage(); }
      });
    });
  
    /**
     * Send a chat message through the socket.
     */
    window.sendMessage = function() {
      var input = document.getElementById("chatInput");
      var message = input.value.trim();
      if (message && socket) {
        var data = { msg: message };
        socket.emit('chat_message', data);
        input.value = '';
      }
    };
  })();
  