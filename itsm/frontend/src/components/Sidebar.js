import React from 'react';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Toolbar from '@mui/material/Toolbar';
import Collapse from '@mui/material/Collapse';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import { useNavigate } from 'react-router-dom';
import menuData from '../config/menuData';
import Typography from '@mui/material/Typography';
const drawerWidth = 240;

const Sidebar = ({handleDrawerTransitionEnd, handleDrawerClose,mobileOpen,handleToggle,open,window }) => {
  const navigate = useNavigate();

  const renderMenuItems = (items) => {
    return items.map((item) => (
      <div key={item.title}>
        <ListItem disablePadding>
          <ListItemButton
            onClick={() => {
              if (item.path) {
                navigate(item.path); // Navigate to the specified path
              }
              if (item.children) {
                handleToggle(item.title);
              }
            }}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.title} />
            {item.children && (open[item.title] ? <ExpandLess /> : <ExpandMore />)}
          </ListItemButton>
        </ListItem>
        {item.children && (
          <Collapse in={open[item.title]} timeout="auto" unmountOnExit>
            <List component="div" disablePadding sx={{ pl: 4 }}>
              {renderMenuItems(item.children)}
            </List>
          </Collapse>
        )}
      </div>
    ));
  };

  const drawer = (
    <div>
      <Toolbar sx={{ backgroundColor: '#1976d2' }}>
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h5" component="div" sx={{ color: '#fff' }}>
            Helpdesk
          </Typography>
        </Box>
      </Toolbar>
      <Divider />
      <List>{renderMenuItems(menuData)}</List>
      <Divider />
    </div>
  );

  const container = window !== undefined ? () => window().document.body : undefined;

  return (
    <>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
      >
        <Drawer
          container={container}
          variant="temporary"
          open={mobileOpen}
          onTransitionEnd={handleDrawerTransitionEnd}
          onClose={handleDrawerClose}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
    </>
  );
};

export default Sidebar;
