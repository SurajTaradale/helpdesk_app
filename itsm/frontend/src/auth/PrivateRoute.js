import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const PrivateRoute = ({ component: Component, usertype }) => {
  const isAgentAuthenticated = useSelector(
    (state) => state.agent.isAgentAuthenticated
  );
  const isCustomerAuthenticated = useSelector(
    (state) => state.customer.isCustomerAuthenticated
  );
  if (usertype === 'agent') {
    return isAgentAuthenticated ? (
      <Component />
    ) : (
      <Navigate to="/agent/login" />
    );
  } else if (usertype === 'customer') {
    return isCustomerAuthenticated ? (
      <Component />
    ) : (
      <Navigate to="/customer/login" />
    );
  }
};

export default PrivateRoute;
