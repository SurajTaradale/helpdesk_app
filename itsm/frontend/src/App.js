import React from 'react';
import { Route, Routes } from 'react-router-dom';
import PrivateRoute from './auth/PrivateRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

const App = () => {
  return (
    <div className="App">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={<PrivateRoute component={Dashboard} />}
        />
      </Routes>
    </div>
  );
};

export default App;
