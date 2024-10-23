import { createSlice } from '@reduxjs/toolkit';
import Cookies from 'js-cookie';

const customerSlice = createSlice({
  name: 'customer',
  initialState: {
    isCustomerAuthenticated: !!Cookies.get('customeruser_token'),
    user_type: 'customer',
  },
  reducers: {
    login(state, action) {
      state.isCustomerAuthenticated = true;
      Cookies.set('customeruser_token', action.payload.token, {
        expires: 1,
        secure: false,
        sameSite: 'Strict',
      });
    },
    logout(state) {
      state.isCustomerAuthenticated = false;
      Cookies.remove('customeruser_token');
    },
  },
});

export const { login, logout } = customerSlice.actions;
export default customerSlice.reducer;
