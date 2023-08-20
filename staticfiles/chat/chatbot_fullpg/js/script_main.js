const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage(){
    const userMessage = userInput.value;
    if(userMessage === ""){
        return;
    }
    appendMessage('user', userMessage);
    userInput.value = '';
    apiRequest(userMessage)
}

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.innerHTML = message;
    // const avatar = document.createElement('img');
    // avatar.classList.add('avatar');
    // avatar.classList.add(`avatar-${sender}`);
    // avatar.alt = sender.charAt(0).toUpperCase();
    // if(sender === 'bot'){
    //     avatar.src = "/static/icons/favicon.png";
    // }
    // if(sender === 'user'){
    //     avatar.src = userSrc;
    // }
    // chatMessages.appendChild(avatar);
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    gsap.from(messageElement, { duration: 0.3, y: "-10px", opacity: 0, ease: "power1.in" });
}

function getBotResponse(userMessage) {
    // Replace this with your actual bot logic
    return "I'm a bot. Your message: " + userMessage;
}

// GSAP Animation
gsap.from(".chat-container", { opacity: 0, y: -50, duration: 1, ease: "power3.out" });

window.onload = ()=> {
    apiRequest('init')
}

function apiRequest(userMessage){
    var SendData = {
        message: userMessage,
    };
    var apiUrl = "/support/api/chat_responce/";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", apiUrl, true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
    if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        console.log(response);
        appendMessage('bot', response.response);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    };
    xhr.send(JSON.stringify(SendData));
}