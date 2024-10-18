let socket;
let token;
let currentRoom = null;


function showLogin() {
    document.getElementById('login-container').style.display = 'block';
    document.getElementById('register-container').style.display = 'none';
    document.getElementById('chat-container').style.display = 'none';
}


function showRegister() {
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('register-container').style.display = 'block';
    document.getElementById('chat-container').style.display = 'none';
}


function showChat() {
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('register-container').style.display = 'none';
    document.getElementById('chat-container').style.display = 'flex';
}


document.getElementById('register-link').addEventListener('click', (e) => {
    e.preventDefault();
    showRegister();
});

document.getElementById('login-link').addEventListener('click', (e) => {
    e.preventDefault();
    showLogin();
});


document.getElementById('register-button').addEventListener('click', async () => {
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;

    try {
        const response = await axios.post('/auth/register', {
            username,
            password
        });
        alert('Регистрация успешна! Войдите в систему.');
        showLogin();
    } catch (error) {
        alert('Ошибка регистрации: ' + error.response.data.detail);
    }
});


document.getElementById('login-button').addEventListener('click', async () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post('/auth/login', new URLSearchParams({
            username,
            password
        }));
        token = response.data.access_token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        connectSocket();
        showChat();
        loadRooms();
    } catch (error) {
        alert('Ошибка входа: ' + error.response.data.detail);
    }
});


async function loadRooms() {
    try {
        const response = await axios.get('/chat/rooms');
        const roomsList = document.getElementById('rooms-list');
        roomsList.innerHTML = '';
        response.data.forEach(room => {
            const li = document.createElement('li');
            li.textContent = room.name;
            li.dataset.roomId = room.id;
            li.addEventListener('click', () => {
                joinRoom(room);
            });
            roomsList.appendChild(li);
        });
    } catch (error) {
        alert('Ошибка загрузки комнат: ' + error.response.data.detail);
    }
}


document.getElementById('create-room-button').addEventListener('click', async () => {
    const roomName = document.getElementById('new-room-name').value;
    try {
        const response = await axios.post('/chat/rooms', {
            name: roomName
        });
        loadRooms();
        document.getElementById('new-room-name').value = '';
    } catch (error) {
        alert('Ошибка создания комнаты: ' + error.response.data.detail);
    }
});


function joinRoom(room) {
    if (currentRoom) {
        socket.emit('leave_room', { room: currentRoom.name });
    }
    currentRoom = room;
    document.getElementById('current-room').textContent = `Комната: ${room.name}`;
    document.getElementById('messages-container').innerHTML = '';
    socket.emit('join_room', { room: room.name });
}


document.getElementById('send-button').addEventListener('click', () => {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    if (message && currentRoom) {
        socket.emit('send_message', {
            room: currentRoom.name,
            message: message,
            user_id: 'current_user' 
        });
        messageInput.value = '';
    }
});


document.getElementById('send-private-button').addEventListener('click', () => {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    const recipientUsername = document.getElementById('private-username').value;
    if (message && recipientUsername) {
        socket.emit('private_message', {
            recipient_username: recipientUsername,
            message: message
        });
        messageInput.value = '';
    }
});


function connectSocket() {
    socket = io({
        auth: {
            token: token
        }
    });

    socket.on('connect', () => {
        console.log('Connected to Socket.IO server');
    });

    socket.on('new_message', (data) => {
        displayMessage(data.message, data.user_id);
    });

    socket.on('private_message', (data) => {
        alert(`Приватное сообщение от ${data.sender}: ${data.message}`);
    });

    socket.on('user_joined', (data) => {
        displaySystemMessage(`${data.user} присоединился к комнате.`);
    });
}


function displayMessage(message, userId) {
    const messagesContainer = document.getElementById('messages-container');
    const div = document.createElement('div');
    div.classList.add('message');
    div.textContent = `${userId}: ${message}`;
    messagesContainer.appendChild(div);
}


function displaySystemMessage(message) {
    const messagesContainer = document.getElementById('messages-container');
    const div = document.createElement('div');
    div.classList.add('system-message');
    div.textContent = message;
    messagesContainer.appendChild(div);
}
