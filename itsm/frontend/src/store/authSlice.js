import { createSlice } from '@reduxjs/toolkit';
import Cookies from 'js-cookie';

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    isAuthenticated: !!Cookies.get('token'),
  },
  reducers: {
    login(state) {
      state.isAuthenticated = true;
    },
    logout(state) {
      state.isAuthenticated = false;
      Cookies.remove('token');
    },
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;
