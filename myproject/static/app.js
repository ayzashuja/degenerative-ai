function signup() {
    var username = document.getElementById("signupUsername").value;
    var password = document.getElementById("signupPassword").value;
    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "username": username, "password": password })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("signupMessage").innerText = data.message;
        });
}

function login() {
    var username = document.getElementById("loginUsername").value;
    var password = document.getElementById("loginPassword").value;
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "username": username, "password": password })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("loginMessage").innerText = data.message;
        });
}
