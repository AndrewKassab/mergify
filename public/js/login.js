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
    xhr.open("GET", domain + "/api/auth");
    xhr.send();
});
