let loginButton = document.getElementById('login');

var url = window.location.href;
var arr = url.split('/');
var domain = arr[0] + '//' + arr[2];

loginButton.addEventListener('click', function() {
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (this.readyState == XMLHttpRequest.DONE) {
            // TODO: Error handling here
            if (xhr.status != 200) {
                return;
            }
            window.location.href = this.responseText;
        }
    }
<<<<<<< HEAD
    // DEV URL
    xhr.open("GET", "http://localhost:5000/auth");
=======
    xhr.open("GET", domain + "/api/auth");
>>>>>>> 21dbe94b883da4c1bbd7230f7349bc929f60ab71
    xhr.send();
});
