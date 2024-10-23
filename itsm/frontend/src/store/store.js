import { configureStore } from '@reduxjs/toolkit';
import customerReducer from './customerSlice';
import agentReducer from './agentSlice';

const store = configureStore({
  reducer: {
    customer: customerReducer,
    agent: agentReducer,
  },
});

export default store;
