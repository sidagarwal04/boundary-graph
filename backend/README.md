# IPL Cricket Dashboard - Backend API

FastAPI backend with advanced caching and performance optimization for the IPL Cricket Dashboard.

## Features

- 🚀 **Advanced Caching**: Redis + Memory caching with intelligent TTL strategies
- ⚡ **Performance Optimized**: Connection pooling, query optimization, response compression
- 📊 **Neo4j Integration**: Efficient graph database queries with caching layers
- 🔍 **Monitoring**: Built-in performance monitoring and cache analytics
- 🛡️ **Production Ready**: Health checks, error handling, and scalable architecture

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp example.env .env
   # Edit .env with your Neo4j and Redis credentials
   ```

3. **Start the API:**
   ```bash
   uvicorn backend_api:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Development

```bash
# From project root
docker-compose up -d
```

This starts:
- FastAPI backend on port 8000
- Redis cache on port 6379
- Auto-reload for development

## API Endpoints

### Core Statistics
- `GET /api/overview` - Database overview statistics
- `GET /api/seasons` - Season statistics
- `GET /api/venues` - Venue performance data

### Player & Team Data  
- `GET /api/batsmen/top` - Top batsmen leaderboard
- `GET /api/bowlers/top` - Top bowlers leaderboard
- `GET /api/players/{name}/stats` - Individual player statistics
- `GET /api/team/{name}/stats` - Team performance data

### Search & Discovery
- `GET /api/search?q={query}` - Search players, teams, venues
- `GET /api/players/all` - Complete player database

### Performance & Monitoring
- `GET /health` - Health check with cache status
- `GET /api/cache/stats` - Cache performance metrics
- `POST /api/cache/clear` - Clear all caches (dev/debug)

## Caching Strategy

### Cache Layers
1. **Redis Cache**: Distributed caching (30min - 4hr TTL)
2. **Memory Cache**: Application-level caching (5-30min TTL)  
3. **Query Cache**: Database result caching (5min TTL)

### TTL Strategy by Data Type
- **Overview/Historical**: 1-4 hours (changes infrequently)
- **Player/Team Stats**: 15-30 minutes (moderate updates)
- **Search Results**: 5 minutes (dynamic content)
- **Live Data**: No cache (real-time requirements)

## Database Optimization

### Required Neo4j Indexes
Execute these commands in Neo4j Browser for optimal performance:

```cypher
CREATE INDEX player_name_index IF NOT EXISTS FOR (p:Player) ON (p.name);
CREATE INDEX team_name_index IF NOT EXISTS FOR (t:Team) ON (t.name);
CREATE INDEX match_season_index IF NOT EXISTS FOR (m:Match) ON (m.season);
CREATE INDEX match_venue_index IF NOT EXISTS FOR (m:Match) ON (m.venue);
```

See `neo4j_optimization.cypher` for complete indexing strategy.

### Connection Pool Settings
- **Max Pool Size**: 50 connections
- **Connection Timeout**: 60 seconds
- **Retry Strategy**: Exponential backoff with jitter
- **Connection Lifetime**: 1 hour

## Configuration

### Environment Variables

#### Database
- `NEO4J_URI` - Neo4j connection URI
- `NEO4J_USERNAME` - Neo4j username  
- `NEO4J_PASSWORD` - Neo4j password

#### Caching
- `REDIS_URL` - Redis connection URL
- `ENABLE_REDIS` - Enable/disable Redis caching
- `CACHE_TTL` - Default cache TTL in seconds

#### Performance
- `WORKERS` - Number of Uvicorn workers
- `MAX_POOL_SIZE` - Neo4j connection pool size
- `REQUEST_TIMEOUT` - API request timeout

See `example.env.production` for complete production configuration.

## Performance Monitoring

### Built-in Analytics
- **Cache Hit Rates**: Memory, Redis, and database cache performance
- **Response Times**: API endpoint performance tracking
- **Error Rates**: Success/failure monitoring by endpoint
- **Resource Usage**: Connection pool and memory utilization

### Accessing Metrics
```bash
curl http://localhost:8000/api/cache/stats
curl http://localhost:8000/health
```

## Production Deployment

### Environment Setup
1. Copy `example.env.production` to `.env`
2. Configure Neo4j and Redis connection strings
3. Set appropriate cache TTL values for your use case
4. Configure CORS origins for your frontend domains

### Performance Tuning
- **Workers**: Set to 2x CPU cores for optimal throughput
- **Memory**: Allocate 512MB+ for Redis cache
- **Connections**: Tune Neo4j pool size based on concurrent load
- **TTL**: Adjust cache expiration based on data freshness requirements

### Health Monitoring
The `/health` endpoint provides comprehensive system status:
- Database connectivity
- Cache system status  
- Performance metrics
- Error rates

## Development

### Adding New Endpoints
1. Add route function with `@cache_response()` decorator
2. Define appropriate TTL for the data type
3. Add to API documentation
4. Test cache behavior with different TTL values

### Cache Management
- Use `@cache_response(ttl=seconds)` for automatic caching
- Access cache stats via `/api/cache/stats`
- Clear cache during development with `/api/cache/clear`

### Database Queries
- Use read transactions for better performance
- Implement query result caching for expensive operations
- Monitor query performance with Neo4j query logs
- Follow indexing guidelines in `neo4j_optimization.cypher`

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │────│   FastAPI       │────│   Neo4j DB      │
│   (Nuxt.js)     │    │   Backend       │    │   (Graph DB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                       ┌─────────────────┐
                       │   Redis Cache   │
                       │   (Memory Store) │
                       └─────────────────┘
```

**Data Flow:**
1. Frontend requests data from FastAPI
2. FastAPI checks Redis cache first
3. On cache miss, queries Neo4j database  
4. Results cached in Redis + memory
5. Response compressed and sent to frontend
6. Frontend caches in localStorage with stale-while-revalidate

## License

This project is licensed under the MIT License - see the LICENSE file for details.