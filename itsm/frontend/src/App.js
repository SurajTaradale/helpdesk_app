import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import PrivateRoute from './auth/PrivateRoute';
import PublicRoute from './auth/PublicRoute';
import AgentLogin from './pages/AgentLogin';
import CustomerLogin from './pages/CustomerLogin';
import AgentDashboard from './pages/AgentDashboard';
import UserTable from './pages/user/UserTable';
import UserCreateEdit from './pages/user/UserCreateEdit';
import Admin from './pages/Admin';
import AgentLayout from './layout/AgentLayout';
import CustomerDashboard from './pages/CustomerDashboard';
import CustomerLayout from './layout/CustomerLayout';

const App = () => {
  return (
    <div className="App">
      <Routes>
        {/* Public routes */}
        <Route
          path="/agent/login"
          element={<PublicRoute component={AgentLogin} usertype="agent" />}
        />
        <Route
          path="/customer/login"
          element={
            <PublicRoute component={CustomerLogin} usertype="customer" />
          }
        />

        {/* Agent-specific routes under AgentLayout */}
        <Route
          path="/agent/*"
          element={
            <PrivateRoute
              component={() => (
                <AgentLayout>
                  <Routes>
                    <Route path="dashboard" element={<AgentDashboard />} />
                    <Route path="admin" element={<Admin />} />{' '}
                    <Route path="user" element={<UserTable />} />{' '}
                    <Route path="user/create" element={<UserCreateEdit />} />{' '}
                    <Route path="user/update" element={<UserCreateEdit />} />{' '}
                    {/* New Admin Route */}
                  </Routes>
                </AgentLayout>
              )}
              usertype="agent"
            />
          }
        />

        {/* Customer-specific routes under CustomerLayout */}
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

        {/* Redirect root to /agent/dashboard */}
        <Route path="/" element={<Navigate to="/agent/dashboard" />} />
      </Routes>
    </div>
  );
};

export default App;
