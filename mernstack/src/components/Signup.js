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
//             await axios.post('http://localhost:3000/signup', {
//                 username,password
//             })
//             .then(res => {
//                 if(res.data=="username already exists") {
//                     alert("Username already exist");
//                 }
//                 else if(res.data=="valid username") {
//                     history("/home",{state:{id:username}});
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
//             <h1>Signup</h1>
//             <form action="POST">
//                 <input type="text" onChange={(e) => {setUsername(e.target.value)}} placeholder='Username' />
//                 <input type="password" onChange={(e) => {setPassword(e.target.value)}} placeholder='Password' />
//                 <input type="submit" onClick={submit} />
//             </form>
//             <br />
//             <p>OR</p>
//             <br />
//             <Link to="/">Login Page</Link>
//         </div>
//     )
// }

// export default Login;






import React, { useState } from 'react';
import axios from 'axios';

const Signup = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/signup', { username, password });
      setSuccess(true);
      setError('');
    } catch (err) {
      setSuccess(false);
      setError(err.response.data.error);
    }
  };

  return (
    <form onSubmit={handleSignup}>
      <div>
        <h1>Sign up page</h1>
        <label htmlFor="username">Username:</label>
        <input type="text" id="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      </div>
      {error && <div>{error}</div>}
      {success && <div>Signup successful!</div>}
      <button type="submit">Signup</button>
    </form>
  );
};

export default Signup;
