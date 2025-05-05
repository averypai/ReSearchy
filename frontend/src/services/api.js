import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const searchSimilarPapers = async (researchIdea, topK = 5) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/search`, { 
      query: researchIdea,
      top_k: topK
    });
    return response.data.results;
  } catch (error) {
    console.error('Error searching papers:', error);
    throw error;
  }
};

export const getComparisonData = async (researchIdea, paperText) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/compare`, {
      query: researchIdea,
      paper_text: paperText
    });
    return response.data;
  } catch (error) {
    console.error('Error getting comparison data:', error);
    throw error;
  }
};