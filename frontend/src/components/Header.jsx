import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import SearchIcon from '@mui/icons-material/Search';

const Header = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            textDecoration: 'none',
            color: 'white',
            flexGrow: 1,
            display: 'flex',
            alignItems: 'center',
          }}
        >
          <SearchIcon sx={{ mr: 1 }} />
          ReSearchy
        </Typography>
        <Box>
          <Button color="inherit" component={RouterLink} to="/">Home</Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;