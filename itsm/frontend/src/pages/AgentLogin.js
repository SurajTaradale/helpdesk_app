import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../store/agentSlice';
import { agentLoginApi } from '../services/AuthService';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Avatar,
  Typography,
  TextField,
  Button,
  CssBaseline,
  Grid,
  Paper,
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { useNotification } from '../context/NotificationContext';
const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const showNotification = useNotification();
  const handleLogin = async (e) => {
    e.preventDefault();
    if(!username || !password){
      showNotification('UserName and Password is required', 'info');
      return;
    }
    try {
      const response = await agentLoginApi(username, password);
      const { user_type } = response;
      showNotification('Login successfully', 'success');
      dispatch(login({ user_type }));
      navigate('/agent/dashboard');
    } catch (error) {
      showNotification('Login failed. Please check your credentials.', 'warning');
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <Paper elevation={6} sx={{ padding: 4, mt: 8, borderRadius: 3 }}>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Agent Login
          </Typography>
          <Box
            component="form"
            onSubmit={handleLogin}
            noValidate
            sx={{ mt: 1 }}
          >
            <TextField
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
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item xs>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  align="center"
                >
                  Forgot password?
                </Typography>
              </Grid>

            </Grid>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default Login;
