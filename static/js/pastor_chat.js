// pastor_chat.js
(function(){
    // Create a Socket.IO connection for the pastor
    const pastorSocket = io({ query: 'user_type=pastor' });
    let activeUserId = null;
    let users = {};
    let chats = {};
    // Object to track unread messages for each user.
    let unread = {};
  
    // Load state from localStorage
    function loadPastorState() {
      try {
        chats = JSON.parse(localStorage.getItem('pastor_chat_history')) || {};
      } catch(e) { chats = {}; }
      try {
        users = JSON.parse(localStorage.getItem('pastor_users')) || {};
      } catch(e) { users = {}; }
      try {
        unread = JSON.parse(localStorage.getItem('pastor_unread')) || {};
      } catch(e) { unread = {}; }
      activeUserId = localStorage.getItem('pastor_activeUserId') || null;
      updateUserList();
      if (activeUserId) { showChatForUser(activeUserId); }
    }
  
    // Save state to localStorage
    function savePastorState() {
      localStorage.setItem('pastor_chat_history', JSON.stringify(chats));
      localStorage.setItem('pastor_users', JSON.stringify(users));
      localStorage.setItem('pastor_unread', JSON.stringify(unread));
      if (activeUserId) {
        localStorage.setItem('pastor_activeUserId', activeUserId);
      } else {
        localStorage.removeItem('pastor_activeUserId');
      }
    }
  
    // Append a message to the chat window
    function appendMessageToChatWindow(message) {
      const chatWindow = document.getElementById('chat-window');
      const msgDiv = document.createElement('div');
      if (message.user_type === 'user') {
        msgDiv.textContent = `${message.sender} (${message.email}, ${message.phone}): ${message.msg}`;
      } else if (message.user_type === 'pastor') {
        msgDiv.textContent = `Pastor: ${message.msg}`;
      }
      chatWindow.appendChild(msgDiv);
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }
  
    // Update the connected users list
    function updateUserList() {
      const userItems = document.getElementById('user-items');
      userItems.innerHTML = '';
      for (let userId in users) {
        const li = document.createElement('li');
        li.classList.add('user-item');
        // Create container for user info and new badge
        const infoDiv = document.createElement('div');
        infoDiv.textContent = `${users[userId].name} (${users[userId].email}, ${users[userId].phone})`;
        // Add "new" badge if unread messages exist
        if (unread[userId]) {
          const newBadge = document.createElement('span');
          newBadge.textContent = " new";
          newBadge.style.color = 'red';
          newBadge.style.fontWeight = 'bold';
          infoDiv.appendChild(newBadge);
        }
        li.appendChild(infoDiv);
  
        // Create delete button to remove user from the local list.
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = "X";
        deleteBtn.style.marginLeft = '10px';
        deleteBtn.style.cursor = 'pointer';
        deleteBtn.onclick = (function(uid) {
          return function(e) {
            e.stopPropagation();
            delete users[uid];
            delete chats[uid];
            delete unread[uid];
            if (activeUserId === uid) {
              activeUserId = null;
              document.getElementById('chat-user-name').textContent = "Select a user to chat";
              document.getElementById('chat-user-info').textContent = "";
              document.getElementById('chat-window').innerHTML = "";
            }
            updateUserList();
            savePastorState();
          };
        })(userId);
        li.appendChild(deleteBtn);
  
        // When a user is clicked, display their chat and clear unread flag.
        li.onclick = (function(uid) {
          return function() {
            activeUserId = uid;
            unread[uid] = false;
            savePastorState();
            showChatForUser(uid);
          };
        })(userId);
        userItems.appendChild(li);
      }
      savePastorState();
    }
  
    // Display the chat for a specific user
    function showChatForUser(userId) {
      const user = users[userId];
      document.getElementById('chat-user-name').textContent = user.name;
      document.getElementById('chat-user-info').textContent = `Email: ${user.email}, Phone: ${user.phone}`;
      const chatWindow = document.getElementById('chat-window');
      chatWindow.innerHTML = '';
      if (chats[userId]) {
        chats[userId].forEach(appendMessageToChatWindow);
      }
    }
  
    // Socket.IO event handlers
    pastorSocket.on('connect', function(){
      console.log('Pastor connected.');
      loadPastorState();
    });
  
    pastorSocket.on('user_connected', function(data) {
      users[data.user_id] = data;
      if (!chats[data.user_id]) {
        chats[data.user_id] = [];
      }
      updateUserList();
    });
  
    pastorSocket.on('user_disconnected', function(data) {
      delete users[data.user_id];
      delete chats[data.user_id];
      delete unread[data.user_id];
      if (activeUserId === data.user_id) {
        activeUserId = null;
        document.getElementById('chat-user-name').textContent = "Select a user to chat";
        document.getElementById('chat-user-info').textContent = "";
        document.getElementById('chat-window').innerHTML = "";
      }
      updateUserList();
      savePastorState();
    });
  
    pastorSocket.on('chat_message', function(data) {
      const userId = (data.user_type === 'user') ? data.user_id : data.target_user_id;
      if (!userId) return;
      if (!chats[userId]) { chats[userId] = []; }
      chats[userId].push(data);
      if (activeUserId !== userId) {
        unread[userId] = true;
      }
      savePastorState();
      if (activeUserId === userId) {
        appendMessageToChatWindow(data);
      }
      updateUserList();
    });
  
    // Expose the send message function globally for the Send button.
    window.sendPastorMessage = function() {
      if (!activeUserId) {
        alert("Select a user to chat with.");
        return;
      }
      const input = document.getElementById('pastorChatInput');
      const message = input.value.trim();
      if (message) {
        pastorSocket.emit('chat_message', { msg: message, target_user_id: activeUserId });
        input.value = '';
      }
    };
  
    // Expose update functions if needed.
    window.updateUserList = updateUserList;
    window.showChatForUser = showChatForUser;
  })();
  