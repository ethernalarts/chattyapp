document.addEventListener('DOMContentLoaded', (event) => {
	//DOM loaded

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/room/'
    );

    const chat = document.querySelector('#chat');
    const input = document.querySelector('#chat-message-input');
    const submitButton = document.querySelector('#chat-message-submit');

    chatSocket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log(data.message)
        chat.innerHTML += '<div class="w-auto md:max-w-2xl float-left rounded-md my-2 bg-gray-400 p-4 text-lg'
                        + ' text-gray-800 font-semibold">'
                        + data.message
                        + '</div>';
        chat.scrollTop = chat.scrollHeight;
    };

    chatSocket.onclose = function(event) {
        console.error('Chat socket closed unexpectedly');
    };

    submitButton.onclick = function(event) {
        const messageInputDom = input.value;
        if(messageInputDom) {
	        chatSocket.send(JSON.stringify({ 'message': messageInputDom }));
	        input.value = "";
	        input.focus();
        }
    };

	input.focus();
    input.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            // cancel the default action, if needed
            event.preventDefault();

            // trigger click event on button
            submitButton.onclick();
        }
    });
});
