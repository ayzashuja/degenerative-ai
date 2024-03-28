// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import { useNavigate, Link } from 'react-router-dom';

// function Login() {
//     const history = useNavigate();
//     const [username, setUsername] = useState('');
//     const [password, setPassword] = useState('');

//     async function submit(e) {
//         e.preventDefault();

//         try {
//             await axios.post('http://localhost:3000', {
//                 username,password
//             })
//             .then(res => {
//                 if(res.data=="exists") {
//                     history("/home",{state:{id:username}})
//                 }
//                 else if(res.data=="does not exist") {
//                     alert("Username is invalid as it does not exist")
//                 }
//             })
//             .catch(e=>{
//                 alert(e)
//             })
//         }
//         catch(err) {
//             console.log(err);
//         }
//     }

//     return (
//         <div className="Login">
//             <h1>Login</h1>
//             <form action="POST">
//                 <input type="text" onChange={(e) => {setUsername(e.target.value)}} placeholder='Username' />
//                 <input type="password" onChange={(e) => {setPassword(e.target.value)}} placeholder='Password' />
//                 <input type="submit" onClick={submit} />
//             </form>
//             <br />
//             <p>OR</p>
//             <br />
//             <Link to="/signup">Signup Page</Link>
//         </div>
//     )
// }

// export default Login;





import React, { useState } from 'react';
import axios from 'axios';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  }

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.post('http://localhost:5000/', { username: username, password: password })
      .then(response => {
        localStorage.setItem('token', response.data.token);
        window.location.href = '/';
      })
      .catch(error => {
        setErrorMessage(error.response.data.error);
      });
  }

  return (
    <div>
      <h2>Login</h2>
      {errorMessage && <div>{errorMessage}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input type="text" id="username" value={username} onChange={handleUsernameChange} />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input type="password" id="password" value={password} onChange={handlePasswordChange} />
        </div>
        <button type="submit">Login</button>
      </form>
      <h1>
        Click on Register if you dont already have an account.
      </h1>
    </div>
  );
}

export default Login;
