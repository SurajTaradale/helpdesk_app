import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const PrivateRoute = ({ component: Component, ...rest }) => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

  return (
    <Route
      {...rest}
      element={isAuthenticated ? <Component /> : <Navigate to="/login" />}
    />
  );
};

export default PrivateRoute;
