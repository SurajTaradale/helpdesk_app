import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import NavBar from '../components/Navbar'
import Sidebar from '../components/Sidebar'

const drawerWidth = 240;

function AgentLayout({ window, children }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isClosing, setIsClosing] = useState(false);
  const [open, setOpen] = useState({});

  const handleDrawerClose = () => {
    setIsClosing(true);
    setMobileOpen(false);
  };

  const handleDrawerTransitionEnd = () => {
    setIsClosing(false);
  };

  const handleDrawerToggle = () => {
    if (!isClosing) {
      setMobileOpen(!mobileOpen);
    }
  };

  const handleToggle = (title) => {
    setOpen((prevState) => ({ ...prevState, [title]: !prevState[title] }));
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <NavBar 
        handleDrawerToggle = {handleDrawerToggle}
        drawerWidth={drawerWidth}
      />
      <Sidebar 
        handleDrawerTransitionEnd={handleDrawerTransitionEnd}
        handleDrawerClose={handleDrawerClose}
        mobileOpen={mobileOpen}
        handleToggle={handleToggle}
        open={open}
        window={window}
      />

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}

AgentLayout.propTypes = {
  window: PropTypes.func,
  children: PropTypes.node,
};

export default AgentLayout;
