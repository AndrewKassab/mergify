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
    // DEV URL
    xhr.open("GET", "http://localhost:5000/auth");
    xhr.send();
});
