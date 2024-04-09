// function getGreeting() {
//     var name = document.getElementById("nameInput").value;
//     fetch(`/hello?name=${name}`)
//         .then(response => response.text())
//         .then(data => {
//             document.getElementById("greetingOutput").innerText = data;
//         });
// }

// function addNumbers() {
//     var numbers = document.getElementById("numbersInput").value.split(",").map(Number);
//     fetch('/add', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ "numbers": numbers })
//     })
//         .then(response => response.json())
//         .then(data => {
//             document.getElementById("sumOutput").innerText = `Sum: ${data.result}`;
//         });
// }


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
