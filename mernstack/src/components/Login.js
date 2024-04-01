// import React, { useState } from 'react';
// import axios from 'axios';
// import { Link } from 'react-router-dom';

// function Login() {
//   const [username, setUsername] = useState('');
//   const [password, setPassword] = useState('');
//   const [errorMessage, setErrorMessage] = useState('');

//   const handleUsernameChange = (event) => {
//     setUsername(event.target.value);
//   }

//   const handlePasswordChange = (event) => {
//     setPassword(event.target.value);
//   }

//   const handleSubmit = (event) => {
//     event.preventDefault();
//     // http://localhost:5000/
//     axios.post('/login', { username: username, password: password })
//       .then(response => {
//         localStorage.setItem('token', response.data.token);
//         window.location.href = '/';
//       })
//       .catch(error => {
//         setErrorMessage(error.response.data.error);
//       });
//   }

//   return (
//     <div>
//       <h2>Login</h2>
//       {errorMessage && <div>{errorMessage}</div>}
//       <form onSubmit={handleSubmit}>
//         <div>
//           <label htmlFor="username">Username:</label>
//           <input type="text" id="username" value={username} onChange={handleUsernameChange} />
//         </div>
//         <div>
//           <label htmlFor="password">Password:</label>
//           <input type="password" id="password" value={password} onChange={handlePasswordChange} />
//         </div>
//         <button type="submit">Login</button>
//       </form>
//       <h3>
//         Click on <Link to="/signup">Signup</Link> if you dont already have an account.
//       </h3>
//     </div>
//   );
// }

// export default Login;

import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

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
    // http://localhost:5000/
    axios.post('http://127.0.0.1:5000/login', { username: username, password: password })
      .then(response => {
        localStorage.setItem('token', response.data.token);
        window.location.href = '/home'; // Redirect to home page
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
      <h3>
        Click on <Link to="/signup">Signup</Link> if you dont already have an account.
      </h3>
    </div>
  );
}

export default Login;
