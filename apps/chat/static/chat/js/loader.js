
 const signInText = document.getElementById('sign-in');
 const spinner = document.getElementById('spinner');
 const submitButton = document.getElementById('submit-button');

 submitButton.onclick = function(event) {
        signInText.style.display = "none";
        spinner.style.display = "block";
 };