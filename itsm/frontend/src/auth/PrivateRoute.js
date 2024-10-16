import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const PrivateRoute = ({ component: Component }) => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

  // If authenticated, render the desired component; if not, redirect to login
  return isAuthenticated ? <Component /> : <Navigate to="/login" />;
};

export default PrivateRoute;
