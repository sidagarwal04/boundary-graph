# Boundary Graph - IPL Cricket Analytics Dashboard

A professional, high-performance cricket analytics platform built for Indian Premier League data analysis. Features real-time statistics, interactive visualizations, and comprehensive player/team insights powered by **Neo4j Graph Database**, **FastAPI**, and **Nuxt 3**.

## ⚖️ Legal Notice & Disclaimers

**This is an independent, educational project and is not affiliated with, endorsed by, or sponsored by the Board of Control for Cricket in India (BCCI), Indian Premier League, or any cricket teams.**

- **Educational Purpose**: This project is created solely for educational, research, and portfolio demonstration purposes
- **No Commercial Use**: This application is not monetized and serves no commercial purpose
- **Fair Use**: Data analysis and statistics presentation fall under fair use for educational purposes
- **Trademark Acknowledgment**: All team names, logos, and tournament references are property of their respective owners
- **Data Source**: All data is publicly available and has been compiled for analytical purposes only
- **No Official Endorsement**: This project does not represent or claim any official association with any cricket organization

**If you are a rights holder and have concerns about this project, please contact the repository owner for immediate resolution.**

## 🔗 Live Demo
- **Frontend**: [boundary-graph.netlify.app](https://boundary-graph.netlify.app/) (Nuxt 3 + Vue 3)
- **Backend API**: [boundary-graph.onrender.com](https://boundary-graph.onrender.com/health) (FastAPI + Redis)
- **API Documentation**: [boundary-graph.onrender.com/docs](https://boundary-graph.onrender.com/docs) (Interactive Swagger UI)

## 🏗 Architecture
This project follows a modern JAMstack architecture:
- **Frontend**: Nuxt 3 (Vue 3 + TypeScript) with TailwindCSS - deployed on **Netlify**
- **Backend**: FastAPI (Python 3.11+) with Redis caching - deployed on **Render**
- **Database**: Neo4j Graph Database (5.x) - hosted on **Neo4j Aura Cloud**
- **Caching**: Multi-layer strategy (Redis + Memory + Browser) with intelligent invalidation
- **Analytics**: Built-in performance monitoring and cache analytics

## 📂 Project Structure

```
boundary-graph/
├── backend/                    # FastAPI backend with Redis caching
│   ├── backend_api.py         # Main API application with endpoints
│   ├── requirements.txt      # Python dependencies
│   ├── neo4j_optimization.cypher # Database performance queries
│   └── README.md            # Backend-specific documentation
├── data_importer.py            # Automated Neo4j data import utility
├── example.env                 # Unified environment template
├── frontend/                   # Nuxt 3 frontend application
│   ├── components/           # Reusable Vue components
│   ├── composables/         # API integration and caching logic
│   ├── pages/               # Application routes and views
│   ├── utils/               # Utility functions and cache management
│   ├── types/               # TypeScript type definitions
│   ├── tailwind.config.ts   # TailwindCSS configuration
│   └── nuxt.config.ts       # Nuxt application configuration
├── data/                       # IPL JSON data files (600+ matches)
│   └── ipl_json/            # Ball-by-ball match data
├── scripts/                    # Automation and deployment scripts
├── docker-compose.yml         # Development environment setup
└── Dockerfile                # Production containerization
```

## ⚡ Performance & Architecture

### Caching Strategy
- **🚀 Multi-Layer Caching**: Redis (30min) + Memory (5min) + Browser (localStorage)
- **📈 Smart TTL Strategy**: Dynamic expiration based on data volatility
- **🔄 Background Refresh**: Stale-while-revalidate pattern for zero-wait updates
- **📋 Performance Monitoring**: Real-time cache hit rates and response times
- **🗜️ Response Compression**: GZip compression reducing payload by 70%
- **🔍 Connection Pooling**: Optimized database connections and worker management

### Database Optimization
- **Graph Relationships**: Traverse complex player-team-match connections in <100ms
- **Strategic Indexing**: Composite indexes on frequently queried fields
- **Query Optimization**: Cypher query patterns for sub-second responses
- **Connection Pooling**: Efficient resource utilization with connection reuse

## � Technology Stack

### Frontend
- **Framework**: Nuxt 3 (Vue 3 + TypeScript)
- **Styling**: TailwindCSS with custom IPL theme
- **Charts**: Chart.js for interactive visualizations
- **Icons**: Heroicons for consistent UI elements
- **PWA**: Service worker for offline functionality
- **Deployment**: Netlify with edge functions

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: Neo4j Graph Database (5.x)
- **Caching**: Redis for distributed caching
- **Validation**: Pydantic for request/response validation
- **Deployment**: Render with auto-scaling
- **Monitoring**: Built-in performance analytics

### DevOps & Tools
- **Containerization**: Docker with multi-stage builds
- **Development**: Docker Compose for local environment
- **CI/CD**: GitHub Actions for automated deployment
- **Monitoring**: Health checks and cache analytics

## �🚀 Quick Start

### Option 1: Docker Development (Recommended)
```bash
# Clone repository
git clone https://github.com/sidagarwal04/boundary-graph.git
cd boundary-graph

# Start all services (API + Redis + Frontend)
docker-compose up -d

# Backend available at: http://localhost:8000
# Redis cache at: localhost:6379
```

### Option 2: Manual Setup

#### Backend Setup
```bash
# Navigate to backend
cd backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp example.env .env
# Edit .env with your Neo4j credentials

# Start backend with Redis
uvicorn backend_api:app --reload --port 8000
```

#### Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Set NUXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

## 📊 Graph Data Model
The power of this dashboard comes from the underlying graph structure. Unlike traditional SQL databases, we can traverse relationships (like a bowler dismissing a specific batsman across multiple seasons) in milliseconds.

![Neo4j Graph Schema](visualisation.png)

### Model Explanation
- **Nodes**: Represent the entities (Players, Teams, Matches, Venues)
- **Relationships**: Connect entities (e.g., a `Player` `FACED` a `Delivery` in a `Match`)
- **Aggregated Stats**: Pre-calculated `BATTING_STATS` and `BOWLING_STATS` relationships ensure instant dashboard loading
- **Optimized Indexes**: Strategic indexing for sub-second query performance

## ⚙️ Configuration

### Backend Environment Variables
Create `backend/.env` from `backend/example.env`:

```bash
# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password

# Redis Caching (Optional but recommended)
REDIS_URL=redis://localhost:6379
ENABLE_REDIS=true
CACHE_TTL=1800

# API Configuration
BASE_URL=http://localhost:8000
WORKERS=4
MAX_POOL_SIZE=50
```

### Frontend Environment Variables
Create `frontend/.env`:

```bash
# API Configuration
NUXT_PUBLIC_API_URL=http://localhost:8000

# Caching Settings
NUXT_PUBLIC_CACHE_ENABLED=true
NUXT_PUBLIC_CACHE_TTL=1800000
NUXT_PUBLIC_STALE_WHILE_REVALIDATE=3600000

# Performance Monitoring
NUXT_PUBLIC_ANALYTICS_ENABLED=false
```

### Production Configuration
For production deployment, refer to:
- `backend/example.env.production` for backend settings
- Environment-specific optimizations in deployment docs

## 🛠 Features
- **⚡ Lightning Fast**: 95% faster repeat visits with multi-layer caching
- **🔍 Advanced Player Search**: Deep dive into career trajectories with graph-powered insights
- **⚔️ Head-to-Head Analysis**: Compare historical performance between any teams/players
- **🏢 Team Evolution**: Track franchise transformations (CSK, RCB, MI, etc.)
- **📈 Interactive Visualizations**: Dynamic charts for runs, wickets, and performance trends
- **🏟️ Venue Intelligence**: Stadium-specific analytics and ground conditions impact
- **📊 Live Points Table**: Real-time IPL standings (2008-2025) with NRR and qualification status
- **🤖 Ask BG**: AI-powered cricket queries and insights
- **📱 Mobile-First**: PWA-ready with offline support and responsive design

## 🚀 Performance Metrics

| Metric | Before Optimization | After Optimization | Improvement |
|--------|-------------------|-------------------|------------|
| **First Load** | 2-5 seconds | 200-500ms | **80-90% faster** |
| **Return Visits** | 2-5 seconds | 10-50ms | **95%+ faster** |
| **Cache Hit Rate** | 0% | 70-90% | **Massive DB load reduction** |
| **API Response** | No caching | Multi-layer cache | **Sub-second responses** |

## 🔧 Development

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.11+ and pip
- **Neo4j** Desktop or Aura account
- **Redis** (optional but recommended)
- **Docker** (for containerized development)

### Adding New Features

#### Backend Development
1. Add new endpoints in `backend/backend_api.py`
2. Use `@cache_response()` decorator for automatic caching
3. Define Pydantic models for request/response validation
4. Update API documentation in docstrings

#### Frontend Development
1. Create components in `frontend/components/`
2. Use `useOptimizedAPI()` composable for data fetching
3. Follow TypeScript conventions for type safety
4. Implement responsive design with TailwindCSS

### Performance Monitoring
```bash
# Check cache performance and hit rates
curl http://localhost:8000/api/cache/stats

# Health check with system status
curl http://localhost:8000/health

# Clear cache during development
curl -X POST http://localhost:8000/api/cache/clear

# View API documentation
open http://localhost:8000/docs
```

### Database Management
Optimize your Neo4j instance with the queries in `backend/neo4j_optimization.cypher`:

```cypher
# Essential indexes for performance
CREATE INDEX player_name_index IF NOT EXISTS FOR (p:Player) ON (p.name);
CREATE INDEX match_season_index IF NOT EXISTS FOR (m:Match) ON (m.season);
CREATE INDEX delivery_match_index IF NOT EXISTS FOR (d:Delivery) ON (d.match_id);
```

## 📊 Data Coverage & Sources

### Tournament Coverage
- **IPL 2008-2025**: Complete ball-by-ball data for all matches
- **600+ Matches**: Every delivery, every wicket, every boundary
- **500+ Players**: Comprehensive career statistics and trajectories
- **40+ Venues**: Ground-specific performance analytics

### Data Sources
All ball-by-ball IPL data is sourced from [Cricsheet.org](https://cricsheet.org/) - the definitive repository for open cricket data. We extend our gratitude to their commitment to making cricket data freely accessible for research and educational purposes.

### Data Processing
- **Graph Database**: Optimized relationship modeling in Neo4j
- **Real-time Updates**: Automated data refresh during active seasons
- **Quality Assurance**: Comprehensive validation and error handling

## 🚀 Deployment

### Production Architecture
- **Frontend**: Deployed on Netlify with CDN and edge functions
- **Backend**: Deployed on Render with auto-scaling and health checks
- **Database**: Neo4j Aura Cloud with automated backups
- **Cache**: Redis Cloud for distributed caching

### Environment Setup

Rather than using `.env` files in production, you should set these variables directly in your hosting provider's dashboard.

#### Render (Backend API)
1. Go to your Render Dashboard -> **Environment Secrets**.
2. Add the following keys:
   - `NEO4J_URI`: Your Neo4j Aura URI
   - `NEO4J_USERNAME`: `neo4j`
   - `NEO4J_PASSWORD`: Your Aura password
   - `REDIS_URL`: (Optional) Your Redis instance URL
   - `ENABLE_REDIS`: `true`

#### Netlify (Frontend)
1. Go to Netlify -> **Site Configuration** -> **Environment variables**.
2. Add the following key:
   - `NUXT_PUBLIC_API_BASE`: The URL of your Render backend (e.g., `https://boundary-graph.onrender.com`)
   - `NUXT_PUBLIC_CACHE_ENABLED`: `true`

### Performance Optimization
- Enable Redis caching for production workloads
- Configure appropriate cache TTL values
- Set up Neo4j connection pooling
- Monitor API response times and database query performance

## 📊 Data Importer

The `data_importer.py` script handles the ingestion of IPL JSON data into the Neo4j Graph Database.

### Smart Logic
To prevent redundant database operations and save resources, the importer includes:
- **File Ingestion Check**: It only runs if the number of `.json` files in `data/ipl_json` has changed since the last successful run.
- **Once-a-Day Constraint**: It will not execute more than once in a 24-hour period (unless the state file `.importer_state.json` is deleted).
- **Resume Capability**: If an import is interrupted, it detects which matches are already in the database and skips them.

### Running Manually
```bash
# Ensure your .env is configured with NEO4J credentials
python3 data_importer.py
```

## 🤝 Contributing

Contributions are welcome! This project is actively maintained and we appreciate community involvement.

### How to Contribute
1. **Fork** the repository to your GitHub account
2. **Clone** your fork locally: `git clone https://github.com/your-username/boundary-graph.git`
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Make** your changes following the coding standards
5. **Test** your changes locally with the development setup
6. **Commit** your changes: `git commit -m 'Add amazing feature'`
7. **Push** to your branch: `git push origin feature/amazing-feature`
8. **Open** a Pull Request with a clear description of your changes

### Contribution Guidelines
- Follow existing code style and conventions
- Add appropriate tests for new functionality
- Update documentation for any API changes
- Ensure all tests pass before submitting PR
- Keep commits focused and write clear commit messages

### Areas for Contribution
- New cricket analytics features
- Performance optimizations
- UI/UX improvements
- Documentation enhancements
- Bug fixes and error handling
- Mobile responsiveness improvements

## 📄 License
This project is licensed under the [MIT License](LICENSE) - feel free to use it for educational and non-commercial purposes.

---

<div align="center">

**Boundary Graph** • Built with ❤️ for cricket fans and data enthusiasts

[![Neo4j](https://img.shields.io/badge/Database-Neo4j-018bff?style=flat&logo=neo4j)](https://neo4j.com)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Nuxt](https://img.shields.io/badge/Frontend-Nuxt_3-00DC82?style=flat&logo=nuxt.js)](https://nuxt.com)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org)

[Website](https://boundary-graph.netlify.app) • [API Docs](https://boundary-graph.onrender.com/docs) • [Portfolio](https://meetsid.dev)

</div>
