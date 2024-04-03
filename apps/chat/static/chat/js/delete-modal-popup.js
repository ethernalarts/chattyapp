// Get the modal
var delete_modal = document.getElementById("delete-modal");

// Get the button that opens the modal
var open_modal_btn = document.getElementById("open-delete-modal");

// Get the button (X) element that closes the modal
var close_button_x = document.getElementById("closemodal-x");

// Get the second <button> element, 'No, Cancel' that closes the modal
var close_button_no = document.getElementById("closemodal-no");

// When the user clicks the button, open the modal
open_modal_btn.onclick = function () {
    delete_modal.style.display = "block";
}

// When the user clicks on <button> (x), close the modal
close_button_x.onclick = function () {
    delete_modal.style.display = "none";
}

// When the user clicks on 'No, Cancel' button, close the modal
close_button_no.onclick = function () {
    delete_modal.style.display = "none";
}