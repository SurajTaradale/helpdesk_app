import { createSlice } from '@reduxjs/toolkit';
import Cookies from 'js-cookie';

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    isAgentAuthenticated: !!Cookies.get('agent_token'),
    user_type: null,
  },
  reducers: {
    login(state, action) {
      state.isAgentAuthenticated = true;
      state.user_type = action.payload.user_type;
    },
    logout(state, action) {
      state.isAgentAuthenticated = false;
      state.user_type = null;
      Cookies.remove(`agent_token`);
    },
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;
