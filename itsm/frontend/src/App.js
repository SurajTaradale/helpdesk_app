import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom'; // Import Navigate here
import PrivateRoute from './auth/PrivateRoute';
import PublicRoute from './auth/PublicRoute';
import AgentLogin from './pages/AgentLogin';
import CustomerLogin from './pages/CustomerLogin';
import AgentDashboard from './pages/AgentDashboard';
import AgentLayout from './layout/AgentLayout';
import CustomerDashboard from './pages/CustomerDashboard';
import CustomerLayout from './layout/CustomerLayout';
const App = () => {
  return (
    <div className="App">
      <Routes>
        <Route
          path="/agent/login"
          element={<PublicRoute component={AgentLogin} usertype="agent" />}
        />
        <Route
          path="/agent/dashboard"
          element={
            <PrivateRoute
              component={() => (
                <AgentLayout>
                  <AgentDashboard />
                </AgentLayout>
              )}
              usertype="agent"
            />
          }
        />
        <Route
          path="/customer/login"
          element={
            <PublicRoute component={CustomerLogin} usertype="customer" />
          }
        />
        <Route
          path="/customer/dashboard"
          element={
            <PrivateRoute
              component={() => (
                <CustomerLayout>
                  <CustomerDashboard />
                </CustomerLayout>
              )}
              usertype="customer"
            />
          }
        />
        <Route path="/" element={<Navigate to="/agent/dashboard" />} />{' '}
        {/* Redirect root to dashboard */}
      </Routes>
    </div>
  );
};

export default App;
