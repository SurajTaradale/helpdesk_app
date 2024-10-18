import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom'; // Import Navigate here
import PrivateRoute from './auth/PrivateRoute';
import PublicRoute from './auth/PublicRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

const App = () => {
  return (
    <div className="App">
      <Routes>
        {/* Use PublicRoute for Login */}
        <Route path="/login" element={<PublicRoute component={Login} />} />
        {/* Use PrivateRoute for Dashboard */}
        <Route
          path="/dashboard"
          element={<PrivateRoute component={Dashboard} />}
        />
        {/* Add other routes here, e.g. for public access */}
        <Route path="/" element={<Navigate to="/dashboard" />} />{' '}
        {/* Redirect root to dashboard */}
      </Routes>
    </div>
  );
};

export default App;
