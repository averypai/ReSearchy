import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Container, 
  Typography, 
  Paper, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  CardActions,
  Button,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress
} from '@mui/material';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';

const ResultsPage = () => {
  const [results, setResults] = useState([]);
  const [userIdea, setUserIdea] = useState('');
  const [sortBy, setSortBy] = useState('relevance');
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  
  useEffect(() => {
    // Get result from localStorage
    const storedResults = localStorage.getItem('searchResults');
    const storedIdea = localStorage.getItem('userIdea');
    
    if (storedResults && storedIdea) {
      setResults(JSON.parse(storedResults));
      setUserIdea(storedIdea);
    } else {
      navigate('/');
    }
    
    setIsLoading(false);
  }, [navigate]);
  
  const handleSortChange = (e) => {
    setSortBy(e.target.value);
  };
  
  const sortedResults = [...results].sort((a, b) => {
    if (sortBy === 'relevance') {
      return b.similarityScore - a.similarityScore;
    } else if (sortBy === 'year') {
      return parseInt(b.year) - parseInt(a.year);
    }
    return 0;
  });
  
  const handleCompare = (paperId) => {
    navigate(`/comparison/${paperId}`);
  };
  
  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 10 }}>
        <CircularProgress />
      </Box>
    );
  }
  
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" component="h1" gutterBottom>
          Search Results
        </Typography>
        
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            Your research idea:
          </Typography>
          <Paper variant="outlined" sx={{ p: 2, bgcolor: '#f5f5f5' }}>
            <Typography variant="body2">
              {userIdea.length > 300 ? `${userIdea.substring(0, 300)}...` : userIdea}
            </Typography>
          </Paper>
        </Box>
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h6">
            Similar Papers ({results.length})
          </Typography>
          
          <FormControl variant="outlined" size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Sort by</InputLabel>
            <Select
              value={sortBy}
              onChange={handleSortChange}
              label="Sort by"
            >
              <MenuItem value="relevance">Relevance</MenuItem>
              <MenuItem value="year">Year (newest first)</MenuItem>
            </Select>
          </FormControl>
        </Box>
        
        {results.length === 0 ? (
          <Alert severity="info">
            No similar papers found. Your research idea appears to be unique!
          </Alert>
        ) : (
          <Grid container spacing={3}>
            {sortedResults.map((paper) => (
              <Grid item xs={12} md={6} key={paper.id}>
                <Card elevation={2}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Chip 
                        label={`${Math.round(paper.similarityScore * 100)}% similar`}
                        color={paper.similarityScore > 0.7 ? 'error' : paper.similarityScore > 0.4 ? 'warning' : 'success'}
                        size="small"
                      />
                      <Typography variant="caption" color="text.secondary">
                        {paper.year}
                      </Typography>
                    </Box>
                    
                    <Typography variant="h6" component="h2" gutterBottom>
                      {paper.title}
                    </Typography>
                    
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {paper.authors.join(', ')}
                    </Typography>
                    
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {paper.abstract.substring(0, 200)}...
                    </Typography>
                  </CardContent>
                  
                  <CardActions>
                    <Button 
                      size="small" 
                      color="primary" 
                      startIcon={<CompareArrowsIcon />}
                      onClick={() => handleCompare(paper.id)}
                    >
                      Compare
                    </Button>
                    
                    {paper.url && (
                      <Button 
                        size="small" 
                        href={paper.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                      >
                        View Paper
                      </Button>
                    )}
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Paper>
    </Container>
  );
};

export default ResultsPage;