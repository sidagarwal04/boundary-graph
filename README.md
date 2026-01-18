# IPL Cricket Dashboard

A professional full-stack cricket analytics platform featuring a Neo4j graph database backend and a Nuxt.js frontend for visualizing IPL (Indian Premier League) cricket data.

## Overview

This project provides:
- **Backend API**: FastAPI REST API with 20+ endpoints for cricket analytics
- **Frontend**: Modern Nuxt.js 3 dashboard with 6 analytics pages
- **Database**: Neo4j graph database with ball-by-ball match data
- **Deployment Ready**: Docker support and Netlify-ready frontend

## Features

### Analytics Pages
- **Overview**: Database statistics and season breakdown
- **Top Batsmen**: Top 50 run scorers with strike rates
- **Top Bowlers**: Top 50 wicket takers with economy
- **Teams**: Franchise statistics and squad management
- **Head-to-Head**: Compare records between two teams
- **Player Search**: Search and view detailed player statistics

### Database Schema
- **Nodes**: Match, Season, Team, Player, Venue, Official, Innings, Over, Delivery
- **Relationships**: Comprehensive cricket data relationships including batting, bowling, dismissals
- **Statistics**: Aggregated player performance metrics

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ and npm
- Neo4j database running

### 1. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp example.env .env
# Edit .env with your Neo4j credentials

# Start backend server
python -m uvicorn backend_api:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp ../example.env .env

# Start development server
npm run dev
```

Access the dashboard at `http://localhost:3000`

## Project Structure

```
├── backend_api.py          # FastAPI backend with 20+ endpoints
├── main.py                 # Data import script
├── requirements.txt        # Python dependencies
├── example.env            # Environment configuration template
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # Backend containerization
│
├── frontend/              # Nuxt.js 3 dashboard
│   ├── pages/
│   │   ├── index.vue      # Overview page
│   │   ├── batsmen.vue    # Top batsmen
│   │   ├── bowlers.vue    # Top bowlers
│   │   ├── teams.vue      # Team statistics
│   │   ├── h2h.vue        # Head-to-head
│   │   └── player-search.vue  # Player search
│   ├── nuxt.config.ts     # Nuxt configuration
│   ├── tailwind.config.ts # Tailwind CSS config
│   └── package.json       # Frontend dependencies
│
└── ipl_json/              # IPL match data (JSON files)
```

## Configuration

Copy `example.env` to `.env` and update values:

```env
# Backend
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
JSON_FOLDER=./ipl_json

# Frontend
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

## API Endpoints

- `GET /api/overview` - Database statistics
- `GET /api/seasons` - Season breakdown
- `GET /api/teams` - All teams
- `GET /api/batsmen/top?limit=50` - Top batsmen
- `GET /api/bowlers/top?limit=50` - Top bowlers
- `GET /api/franchises` - Franchise list
- `GET /api/team/{id}/stats` - Team statistics
- `GET /api/team/{id}/squad` - Team squad
- `GET /api/h2h/{team1}/{team2}` - Head-to-head stats
- `GET /api/h2h/{team1}/{team2}/matches` - H2H match history
- `GET /api/player/{name}` - Player statistics
- `GET /api/players/search?query=...` - Player search

## Deployment

### Docker Deployment

```bash
docker-compose up
```

### Frontend Deployment (Netlify)

```bash
cd frontend
npm run build
# Deploy the dist/ folder to Netlify
```

### Backend Deployment

Deploy `backend_api.py` to your server with:
```bash
python -m uvicorn backend_api:app --host 0.0.0.0 --port 8000
```

## Technology Stack

- **Backend**: FastAPI 0.104.1, Python 3.12
- **Frontend**: Nuxt 3.17.7, Vue 3.5.26, Tailwind CSS 3.3+
- **Database**: Neo4j (graph database)
- **HTTP**: Uvicorn, Axios
- **Validation**: Pydantic 2.5.0
- **Build**: Vite 6.4.1

## Development

### Running Tests

```bash
# Backend
pytest

# Frontend
npm run test
```

### Build for Production

```bash
# Frontend
npm run build

# Backend (with dependencies)
pip install -r requirements.txt
```

## Data Import

The `main.py` script imports IPL data from JSON files into Neo4j:

```bash
python main.py
```

This creates:
- Graph nodes and relationships
- Database constraints and indexes
- Aggregated statistics
- Logs import errors to `import_errors.log`

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on the GitHub repository.
