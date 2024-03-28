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
