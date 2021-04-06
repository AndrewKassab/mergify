let loginButton = document.getElementById('login');

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
    // TODO: Update to just use current URL then add endpoint
    xhr.open("GET", "http://localhost:5000/auth");
=======
    // TODO: Update to just grab current url then add /api/auth
    xhr.open("GET", "http://24.25.205.133/api/auth");
>>>>>>> production
    xhr.send();
});
