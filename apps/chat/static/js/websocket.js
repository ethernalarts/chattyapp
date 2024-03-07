document.addEventListener('DOMContentLoaded', (event) => {
	//DOM loaded
    const url = 'ws://' + window.location.host + '/ws/chat/';
    const chatSocket = new WebSocket(url);

    chatSocket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const chat = document.getElementById('chat');
        chat.innerHTML += data.message;
        chat.scrollTop = chat.scrollHeight;
    };

    chatSocket.onclose = function(event) {
        console.error('Chat socket closed unexpectedly');
    };

    const input = document.getElementById('chat-message-input');
    const submitButton = document.getElementById('chat-message-submit');

    submitButton.addEventListener('click', function(event) {
        const message = input.value;
        if(message) {
            // send message in JSON format
            chatSocket.send(JSON.stringify({'message': message}));
            // clear input
            input.value = '';
            input.focus();
        }
    });

    input.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            // cancel the default action, if needed
            event.preventDefault();
            // trigger click event on button
            submitButton.click();
            input.value = '';
            input.focus();
        }
    });
});
