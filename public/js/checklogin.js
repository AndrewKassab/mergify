function getCookie(name) {
    var b = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return b ? b.pop() : '';
}

// If auth_token is in our cookies, we are considered logged in
if (window.location.href != "http://localhost:5500/login.html"){
    if (!getCookie('auth_token')){
        window.location.href = "http://localhost:5500/login.html";
    }
}
