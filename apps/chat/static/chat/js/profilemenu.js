
const profilemenu = document.querySelector('#profile-menu')
const profilemenubutton = document.querySelector('#user-menu-button')

//OpenProfileMenuButton.addEventListener('click', function myFunction(e) {
//    if (ProfileMenu.style.display = 'hidden'){
//        ProfileMenu.style.display = 'block';
//    } else if (ProfileMenu.style.display = 'block') {
//        ProfileMenu.classList.add('closed');
//    }
//});

//OpenProfileMenuButton.addEventListener('click', () => {
//  profile.classList.add('closed');
//});

//var burgerMenu = document.querySelector('#user-menu-button');
//
//var overlay = document.querySelector('#profile-menu');
//
//burgerMenu.addEventListener('click', function() {
//  this.classList.toggle("close");
//  overlay.classList.toggle("overlay");
//});

profilemenubutton.onclick = function () {
	if (profilemenu.style.display = 'hidden'){
        profilemenu.style.display = 'block';
    }
    else if (profilemenu.style.display = 'block') {
        profilemenu.style.display = 'none';
    }
}
