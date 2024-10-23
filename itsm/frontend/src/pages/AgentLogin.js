import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../store/agentSlice';
import { agentLoginApi } from '../services/AuthService';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate(); // Initialize useNavigate

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await agentLoginApi(username, password);
      const { user_type } = response;
      dispatch(login({ user_type }));
      navigate('/agent/dashboard'); // Redirect to dashboard using navigate
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed. Please check your credentials.');
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h1>Agent Login</h1>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;
