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
    // TODO: Update to just grab current url then add /api/auth
    xhr.open("GET", "http://24.25.205.133/api/auth");
    xhr.send();
});
