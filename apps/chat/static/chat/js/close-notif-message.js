// Get the error message popup
var message = document.getElementsByClassName("error-message");

// Get the X <button> element that closes the error message
var closebutton = document.getElementsByClassName("close-error-message");

// Get the X <button> to close each error message
for (let i = 0; i < message.length; i++) {
    for (let i = 0; i < closebutton.length; i++) {
        closebutton[i].onclick = function () {
            message[i].style.display = "none";
        }
    }
}