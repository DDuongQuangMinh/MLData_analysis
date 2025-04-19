import React, { useState } from 'react';
import axios from 'axios';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const login = () => {
    axios.post('http://localhost:8000/api/login/', { username, password })
      .then(res => {
        localStorage.setItem('token', res.data.token);
        window.location = '/upload';
      });
  };

  return (
    <div>
      <h2>Login</h2>
      <input onChange={e => setUsername(e.target.value)} placeholder="Username" />
      <input onChange={e => setPassword(e.target.value)} type="password" placeholder="Password" />
      <button onClick={login}>Login</button>
    </div>
  );
}
