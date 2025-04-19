import React, { useState } from 'react';
import axios from '../axios';

export default function Login({ setIsLoggedIn }) {
  const [form, setForm] = useState({ username: '', password: '' });

  const login = async () => {
    try {
      const res = await axios.post('auth/login/', form);
      localStorage.setItem('access', res.data.access);
      localStorage.setItem('refresh', res.data.refresh);
      setIsLoggedIn(true);
    } catch (err) {
      alert('Login error');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input placeholder="Username" onChange={e => setForm({...form, username: e.target.value})} />
      <input type="password" placeholder="Password" onChange={e => setForm({...form, password: e.target.value})} />
      <button onClick={login}>Login</button>
    </div>
  );
}