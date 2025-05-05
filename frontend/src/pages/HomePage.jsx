import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Container, 
  Typography, 
  Paper, 
  Box, 
  TextField, 
  Button, 
  CircularProgress 
} from '@mui/material';
import { searchSimilarPapers } from '../services/api';

const HomePage = () => {
  const [researchIdea, setResearchIdea] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (researchIdea.trim().length < 10) {
      setError('Please enter a more detailed research idea (at least 10 characters)');
      return;
    }
    
    setIsLoading(true);
    setError('');
    
    try {
      const results = await searchSimilarPapers(researchIdea);
      // Store the result to localStorage
      localStorage.setItem('searchResults', JSON.stringify(results));
      localStorage.setItem('userIdea', researchIdea);
      navigate('/results');
    } catch (err) {
      setError('Error searching for similar papers. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          ReSearchy: Guarding Novelty, Guiding Ideas
        </Typography>
        
        <Typography variant="body1" paragraph sx={{ mt: 2 }}>
          Input your research idea or abstract below, and we'll help you discover 
          potentially overlapping research, saving you time and ensuring your work is novel.
        </Typography>
        
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <TextField
            fullWidth
            multiline
            rows={8}
            variant="outlined"
            label="Your Research Idea or Abstract"
            placeholder="Enter your research idea or abstract here..."
            value={researchIdea}
            onChange={(e) => setResearchIdea(e.target.value)}
            error={!!error}
            helperText={error}
            required
          />
          
          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
            <Button 
              type="submit" 
              variant="contained" 
              color="primary" 
              size="large"
              disabled={isLoading}
              startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : null}
            >
              {isLoading ? 'Searching...' : 'Find Similar Research'}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default HomePage;