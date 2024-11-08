import React from 'react';
import { Grid, Card, CardContent, Typography } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { useNavigate } from 'react-router-dom';

const cardData = [
  {
    title: 'User',
    icon: <AccountCircleIcon fontSize="large" />,
    path: '/agent/user', // Define the path for navigation
  },
];

const Admin = () => {
  const navigate = useNavigate(); // Initialize the navigate function

  const handleCardClick = (path) => {
    navigate(path); // Navigate to the specified path
  };

  return (
    <Grid container spacing={2} sx={{ padding: 2 }}>
      {cardData.map((card) => (
        <Grid item xs={6} sm={3} key={card.title}>
          <Card
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              textAlign: 'center',
              cursor: 'pointer', // Change cursor to pointer
              '&:hover': { backgroundColor: '#f5f5f5' }, // Add hover effect
            }}
            onClick={() => handleCardClick(card.path)} // Call handleCardClick on card click
          >
            <CardContent>
              {card.icon}
              <Typography variant="h6" sx={{ marginTop: 1 }}>
                {card.title}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default Admin;
