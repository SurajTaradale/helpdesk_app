import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const PublicRoute = ({ component: Component }) => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

  // If authenticated, redirect to dashboard; if not, render the desired component
  return isAuthenticated ? <Navigate to="/dashboard" /> : <Component />;
};

export default PublicRoute;
