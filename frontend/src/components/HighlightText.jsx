import React from 'react';
import { Typography, Box } from '@mui/material';

const HighlightText = ({ text, highlights }) => {
  if (!highlights || highlights.length === 0) {
    return <Typography>{text}</Typography>;
  }
  
  // Sort highlighted items by start position
  const sortedHighlights = [...highlights].sort((a, b) => a.start - b.start);
  
  // Create a highlighted text snippet
  const segments = [];
  let lastIndex = 0;
  
  sortedHighlights.forEach((highlight, index) => {
    // Normal text before adding highlight
    if (highlight.start > lastIndex) {
      segments.push({
        text: text.substring(lastIndex, highlight.start),
        highlighted: false,
        key: `normal-${index}`
      });
    }
    
    // Add highlighted text
    segments.push({
      text: text.substring(highlight.start, highlight.end),
      highlighted: true,
      key: `highlight-${index}`,
      category: highlight.category || 'default'
    });
    
    lastIndex = highlight.end;
  });
  
  // Add the normal text after the last highlight
  if (lastIndex < text.length) {
    segments.push({
      text: text.substring(lastIndex),
      highlighted: false,
      key: `normal-end`
    });
  }
  
  return (
    <Typography component="div">
      {segments.map((segment) => (
        <Box 
          component="span" 
          key={segment.key}
          sx={{
            backgroundColor: segment.highlighted 
              ? (segment.category === 'methodology' ? '#FFAB91' : '#FFAB91')
              : 'transparent',
            padding: segment.highlighted ? '2px 0' : 0,
            borderRadius: '2px'
          }}
        >
          {segment.text}
        </Box>
      ))}
    </Typography>
  );
};

export default HighlightText;