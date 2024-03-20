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
    const requestUser = JSON.parse(document.getElementById('request-user').textContent);

    chatSocket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        const dateOptions = {hour: 'numeric', minute: 'numeric', hour12: true};
		const datetime = new Date(data.datetime).toLocaleString('en', dateOptions);
		const isMe = data.user === requestUser;
		const source = isMe ? 'ml-auto mr-4 text-gray-100 bg-green-800' : 'float-left ml-4 text-gray-800 bg-gray-400';
		const name = isMe ? 'Me' : data.user;

        chat.innerHTML += '<div class="w-full max-w-md md:max-w-2xl rounded-md mb-2 p-4 pb-2 pt-2'
                        + ' text-md font-semibold ' + source + '">'
                        + '<span class="font-bold">' + name + '</span><br>'
                        + data.message
                        + '<br><span class="text-gray-50 text-sm italic float-right">' + datetime + '</span><br>'
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
            event.preventDefault();
            submitButton.onclick();
        }
    });
});
