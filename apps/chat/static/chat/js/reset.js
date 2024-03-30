
document.querySelector('button[type="reset"]').addEventListener('click', function (e) {
    e.preventDefault();
    this.parentElement.reset();
});
