// import React, { useState } from 'react';
// import axios from 'axios';
// import { Link } from 'react-router-dom';

// const Signup = () => {
//   const [username, setUsername] = useState('');
//   const [password, setPassword] = useState('');
//   const [error, setError] = useState('');
//   const [success, setSuccess] = useState(false);

//   const handleSignup = async (e) => {
//     e.preventDefault();
//     // http://localhost:5000/signup
//     try {
//       const response = await axios.post('/signup', { username, password });
//       setSuccess(true);
//       setError('');
//     } catch (err) {
//       setSuccess(false);
//       setError(err.response.data.error);
//     }
//   };

//   return (
//     <form onSubmit={handleSignup}>
//       <div>
//         <h2>Sign up page</h2>
//         <label htmlFor="username">Username:</label>
//         <input type="text" id="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
//       </div>
//       <div>
//         <label htmlFor="password">Password:</label>
//         <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
//       </div>
//       {error && <div>{error}</div>}
//       {success && <div>Signup successful!</div>}
//       <button type="submit">Signup</button>
//       <h3>
//         Click on <Link to="/">Login</Link> if you already have an account.
//       </h3>
//     </form>
//   );
// };

// export default Signup;

import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Signup = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();
    // http://localhost:5000/signup
    try {
      const response = await axios.post('http://127.0.0.1:5000/signup', { username, password });
      setSuccess(true);
      setError('');
      window.location.href = '/home'; // Redirect to home page
    } catch (err) {
      setSuccess(false);
      setError(err.response.data.error);
    }
  };

  return (
    <form onSubmit={handleSignup}>
      <div>
        <h2>Sign up page</h2>
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
      <h3>
        Click on <Link to="/">Login</Link> if you already have an account.
      </h3>
    </form>
  );
};

export default Signup;
