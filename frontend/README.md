# ReSearchy Frontend

ReSearchy is an innovative research assistant that helps researchers identify potential overlaps in their work with existing literature. This repository contains the frontend implementation of ReSearchy, built with React and Material-UI.

## Features

- 🔍 Semantic search for research papers
- 📊 Similarity scoring and comparison
- 📅 Sort results by relevance or publication year
- 🎯 Highlight matching content between your research and existing papers
- 📱 Responsive design for all devices

## Prerequisites

Before you begin, ensure you have the following installed:

- Node.js (v14.0.0 or higher)
- npm (v6.0.0 or higher)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/averypai/ReSearchy.git
cd ReSearchy/frontend
```

2. Install dependencies:

```bash
npm install
```


## Development

To start the development server:

```bash
npm start
```

This will run the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.


## Project Structure

```
frontend/
├── src/
│   ├── components/    # Reusable UI components
│   ├── pages/         # Page components
│   ├── services/      # API services
│   ├── utils/         # Utility functions
│   ├── App.js         # Main application component
│   └── index.js       # Application entry point
├── public/            # Static files
└── package.json       # Project dependencies and scripts
```

## API Integration

The frontend communicates with the ReSearchy backend API. Make sure the backend server is running and accessible at the URL specified in 'http://127.0.0.1:8000' (You can change it through services/api.js API_BASE_URL as you need). 

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- [React](https://reactjs.org/)
- [Material-UI](https://mui.com/)
- [Axios](https://axios-http.com/)


## Authors

- Shilong Li - Initial work - [GitHub](https://github.com/lon9lll)
