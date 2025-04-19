import React, { useState } from 'react';
import axios from '../axios';

export default function Register() {
  const [form, setForm] = useState({ username: '', password: '' });

  const register = async () => {
    try {
      await axios.post('auth/register/', form);
      alert('Registered successfully! Please login.');
    } catch (err) {
      alert('Registration error');
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <input placeholder="Username" onChange={e => setForm({...form, username: e.target.value})} />
      <input type="password" placeholder="Password" onChange={e => setForm({...form, password: e.target.value})} />
      <button onClick={register}>Register</button>
    </div>
  );
}