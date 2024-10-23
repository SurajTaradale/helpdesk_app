import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const PublicRoute = ({ component: Component, usertype }) => {
  const isAgentAuthenticated = useSelector(
    (state) => state.agent.isAgentAuthenticated
  );
  const isCustomerAuthenticated = useSelector(
    (state) => state.customer.isCustomerAuthenticated
  );
  if (usertype === 'agent') {
    // If authenticated, redirect to dashboard; if not, render the desired component
    return isAgentAuthenticated ? (
      <Navigate to="/agent/dashboard" />
    ) : (
      <Component />
    );
  } else if (usertype === 'customer') {
    return isCustomerAuthenticated ? (
      <Navigate to="/customer/dashboard" />
    ) : (
      <Component />
    );
  }
};

export default PublicRoute;
