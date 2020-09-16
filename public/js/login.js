let loginButton = document.getElementById('login');

loginButton.addEventListener('click', function() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "http://localhost:5000/auth")
    xhr.send();
});