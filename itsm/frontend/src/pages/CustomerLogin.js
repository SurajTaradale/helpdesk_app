import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../store/customerSlice';
import { customerLoginApi } from '../services/AuthService';
import { useNavigate } from 'react-router-dom';

const CustomerLogin = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await customerLoginApi(username, password);
      const { user_type } = response;
      dispatch(login({ user_type }));
      navigate('/customer/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed. Please check your credentials.');
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h1>customer login</h1>
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

export default CustomerLogin;
