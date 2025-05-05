import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Container, 
  Typography, 
  Paper, 
  Box, 
  Button, 
  Grid, 
  Divider, 
  CircularProgress,
  Alert
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { getComparisonData } from '../services/api';
import HighlightText from '../components/HighlightText';

const ComparisonPage = () => {
  const { paperId } = useParams();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [userIdea, setUserIdea] = useState('');
  const [paper, setPaper] = useState(null);
  const [comparisonData, setComparisonData] = useState(null);
  
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError('');
      
      const storedIdea = localStorage.getItem('userIdea');
      const storedResults = localStorage.getItem('searchResults');
      
      if (!storedIdea || !storedResults) {
        navigate('/');
        return;
      }
      
      setUserIdea(storedIdea);
      
      // Find selected papersnpm
      const results = JSON.parse(storedResults);
      const selectedPaper = results.find(p => p.id === paperId);
      
      if (!selectedPaper) {
        setError('Paper not found');
        setIsLoading(false);
        return;
      }
      
      setPaper(selectedPaper);
      
      try {
        // Call API to obtain comparison data
        const comparisonResult = await getComparisonData(storedIdea, selectedPaper.abstract);
        setComparisonData(comparisonResult);
      } catch (err) {
        setError('Error loading comparison data');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchData();
  }, [paperId, navigate]);
  
  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 10 }}>
        <CircularProgress />
      </Box>
    );
  }
  
  if (error || !paper) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">{error || 'Paper not found'}</Alert>
        <Button 
          startIcon={<ArrowBackIcon />} 
          onClick={() => navigate('/results')}
          sx={{ mt: 2 }}
        >
          Back to Results
        </Button>
      </Container>
    );
  }
  
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Button 
        startIcon={<ArrowBackIcon />} 
        onClick={() => navigate('/results')}
        sx={{ mb: 2 }}
      >
        Back to Results
      </Button>
      
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" component="h1" gutterBottom>
          Content Comparison
        </Typography>
        
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
          <Typography variant="h6" component="div" sx={{ 
            bgcolor: 'primary.main', 
            color: 'white', 
            px: 3, 
            py: 1, 
            borderRadius: 2 
          }}>
            {Math.round(paper.similarityScore * 100)}% Overall Similarity
          </Typography>
        </Box>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper variant="outlined" sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Your Research Idea
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              {comparisonData ? (
                <HighlightText 
                  text={userIdea} 
                  highlights={comparisonData.userHighlights} 
                />
              ) : (
                <Typography>{userIdea}</Typography>
              )}
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Paper variant="outlined" sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                {paper.title} ({paper.year})
              </Typography>
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                {paper.authors.join(', ')}
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              {comparisonData ? (
                <HighlightText 
                  text={paper.abstract} 
                  highlights={comparisonData.paperHighlights} 
                />
              ) : (
                <Typography>{paper.abstract}</Typography>
              )}
              
              {paper.url && (
                <Button 
                  variant="outlined" 
                  href={paper.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  sx={{ mt: 2 }}
                >
                  View Full Paper
                </Button>
              )}
            </Paper>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default ComparisonPage;