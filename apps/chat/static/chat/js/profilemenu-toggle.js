
const profilemenu = document.querySelector('#profile-menu')
const profilemenubutton = document.querySelector('#user-menu-button')

profilemenubutton.addEventListener('click', function myFunction(e) {
  profilemenu.style.display = (profilemenu.style.display === "block") ? "none" : "block"
});
