import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../store/customerSlice';
import { customerLoginApi } from '../services/AuthService';
import { useNavigate } from 'react-router-dom';
import {
  Avatar,
  Box,
  Button,
  Container,
  CssBaseline,
  TextField,
  Typography,
  Paper,
} from '@mui/material';
import PersonOutlineIcon from '@mui/icons-material/PersonOutline';
import { styled } from '@mui/material/styles';

const Background = styled(Box)({
  display: 'flex',
  minHeight: '100vh',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: '#f4f6f8', // Subtle grey for contrast with white card
});

const AnimatedPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  animation: 'fadeIn 0.6s ease-in-out',
  borderRadius: theme.shape.borderRadius,
  maxWidth: 400,
  width: '100%',
  backgroundColor: '#fff', // Set to white
  boxShadow: '0px 10px 20px rgba(0, 0, 0, 0.1)', // Soft shadow for a modern feel
  '@keyframes fadeIn': {
    from: { opacity: 0 },
    to: { opacity: 1 },
  },
}));

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
    <Background>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <AnimatedPaper elevation={3}>
          <Avatar sx={{ m: 1, bgcolor: 'primary.main' }}>
            <PersonOutlineIcon />
          </Avatar>
          <Typography component="h1" variant="h5" sx={{ mb: 2 }}>
            Customer Login
          </Typography>
          <Box
            component="form"
            onSubmit={handleLogin}
            noValidate
            sx={{ mt: 1 }}
          >
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{
                mt: 3,
                mb: 2,
                p: 1.5,
                backgroundColor: '#1976d2',
                color: '#fff',
                '&:hover': {
                  backgroundColor: '#115293',
                },
              }}
            >
              Login
            </Button>
          </Box>
        </AnimatedPaper>
      </Container>
    </Background>
  );
};

export default CustomerLogin;
