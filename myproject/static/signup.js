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
        // .then(response => response.json())
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url; // Redirect to the channels page
            } else {
                return response.json();
            }
        })
        .then(data => {
            document.getElementById("signupMessage").innerText = data.message;
        });
}

function redirectToLogin() {
  window.location.href = '/login_page';
}