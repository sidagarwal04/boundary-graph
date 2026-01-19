"""
FastAPI Backend for IPL Cricket Dashboard
Provides REST API endpoints for Neo4j database queries
Credentials are kept server-side only
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="IPL Cricket Dashboard API",
    description="Professional API for IPL statistics from Neo4j",
    version="1.0.0"
)

# CORS configuration - allow only your Netlify domain in production
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://boundary-graph.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Neo4j Connection
class Neo4jConnection:
    def __init__(self):
        self.driver = None
    
    def connect(self):
        uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        username = os.getenv('NEO4J_USERNAME', 'neo4j')
        password = os.getenv('NEO4J_PASSWORD', 'password')
        
        try:
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
            self.driver.verify_connectivity()
            logger.info("✓ Connected to Neo4j")
        except Exception as e:
            logger.error(f"✗ Neo4j connection failed: {str(e)}")
            self.driver = None
    
    def query(self, cypher: str, params: dict = None) -> List[Dict[str, Any]]:
        """Execute query and return results as list of dicts"""
        if not self.driver:
            raise HTTPException(status_code=503, detail="Database connection failed")
        
        try:
            with self.driver.session() as session:
                result = session.run(cypher, params or {})
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"Query error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    
    def close(self):
        if self.driver:
            self.driver.close()

# Initialize connection
db = Neo4jConnection()
db.connect()

# Pydantic Models
class OverviewStats(BaseModel):
    total_matches: int
    total_players: int
    total_runs: int
    active_teams: int
    defunct_teams: int
    total_deliveries: int

class SeasonStats(BaseModel):
    season: str
    matches: int

class Player(BaseModel):
    name: str
    runs: Optional[int] = None
    matches: Optional[int] = None
    strike_rate: Optional[float] = None
    wickets: Optional[int] = None
    economy: Optional[float] = None

class Team(BaseModel):
    name: str
    franchise_id: Optional[str] = None
    current_name: Optional[str] = None

class Match(BaseModel):
    date: str
    season: str
    winner: str
    venue: str

# ==================== HEALTH CHECK ====================
@app.get("/health")
async def health_check():
    """Check API and database health"""
    return {
        "status": "healthy",
        "database": "connected" if db.driver else "disconnected"
    }

# Standard rebrand mapping for IPL teams
REBRAND_MAP = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiant": "Rising Pune Supergiants" # Merge spelling variants
}

# ==================== OVERVIEW ENDPOINTS ====================
@app.get("/api/overview", response_model=OverviewStats)
async def get_overview():
    """Get database overview statistics"""
    
    matches = db.query("MATCH (m:Match) RETURN COUNT(m) as count")
    players = db.query("MATCH (p:Player) RETURN COUNT(p) as count")
    deliveries = db.query("MATCH (d:Delivery) RETURN COUNT(d) as count")
    runs = db.query("MATCH (d:Delivery) RETURN SUM(d.runs_total) as count")
    
    # Calculate Active vs Defunct Teams logic with Rebranding
    # 1. Get ALL teams ever
    all_teams_result = db.query("MATCH (t:Team) RETURN DISTINCT t.name as name")
    
    # 2. Get Teams active in the LATEST season
    active_teams_result = db.query("""
        MATCH (m:Match)
        WITH MAX(m.season) as latest_season
        MATCH (t:Team)-[:TEAM_INVOLVED]-(:Match {season: latest_season})
        RETURN DISTINCT t.name as name
    """)
    
    # Simple sets to track unique standardized names
    all_franchises = set()
    active_franchises = set()
    
    for row in all_teams_result:
        raw_name = row['name']
        normalized_name = REBRAND_MAP.get(raw_name, raw_name)
        all_franchises.add(normalized_name)
        
    for row in active_teams_result:
        raw_name = row['name']
        normalized_name = REBRAND_MAP.get(raw_name, raw_name)
        active_franchises.add(normalized_name)
        
    active_count = len(active_franchises)
    total_unique_franchises = len(all_franchises)
    defunct_count = total_unique_franchises - active_count

    return OverviewStats(
        total_matches=matches[0]['count'] if matches else 0,
        total_players=players[0]['count'] if players else 0,
        total_runs=runs[0]['count'] if runs else 0,
        active_teams=active_count,
        defunct_teams=defunct_count,
        total_deliveries=deliveries[0]['count'] if deliveries else 0
    )

# Official Player of the Tournament awards (not in match data)
PLAYER_OF_TOURNAMENT_MAP = {
    "2025": "Suryakumar Yadav",
    "2024": "Sunil Narine",  # Fixed - was incorrectly Virat Kohli
    "2023": "Shubman Gill",
    "2022": "Jos Buttler",
    "2021": "Harshal Patel",
    "2020": "Jofra Archer",
    "2019": "Andre Russell",
    "2018": "Sunil Narine",
    "2017": "Ben Stokes",
    "2016": "Virat Kohli",
    "2015": "Andre Russell",
    "2014": "Glenn Maxwell",
    "2013": "Shane Watson",
    "2012": "Sunil Narine",
    "2011": "Chris Gayle",
    "2010": "Sachin Tendulkar",
    "2009": "Adam Gilchrist",
    "2008": "Shane Watson"
}

# Manual overrides for runner-up teams (for cases where database has incomplete data)
RUNNER_UP_OVERRIDE_MAP = {
    "2017": "Rising Pune Supergiant"  # Database has incomplete TEAM_INVOLVED relationship
}

class SeasonDetails(BaseModel):
    season: str
    winner: Optional[str] = None
    runner_up: Optional[str] = None
    venue: Optional[str] = None
    margin: Optional[str] = None
    total_teams: int
    total_matches: int
    player_of_tournament: Optional[str] = None
    player_of_match: Optional[str] = None  # Player of Match from the final

@app.get("/api/seasons/{season_year}", response_model=SeasonDetails)
async def get_season_details(season_year: str):
    """Get detailed stats for a specific season (Final results etc)"""
    
    # 1. Get Summary Stats (Teams count, Matches count)
    summary_query = """
        MATCH (m:Match {season: $season})
        WITH COUNT(DISTINCT m) as total_matches
        MATCH (t:Team)-[:TEAM_INVOLVED]-(m2:Match {season: $season})
        RETURN total_matches, COUNT(DISTINCT t) as total_teams
    """
    summary = db.query(summary_query, {"season": season_year})
    
    if not summary:
        # Fallback if season not found/no matches
        return SeasonDetails(season=season_year, total_teams=0, total_matches=0)
        
    total_matches = summary[0]['total_matches']
    total_teams = summary[0]['total_teams']
    
    # 2. Get Final Match Details (Last match by date - this is the Final)
    final_query = """
        MATCH (m:Match {season: $season})
        WITH m ORDER BY m.date DESC LIMIT 1
        
        // Get all teams involved in the match
        OPTIONAL MATCH (m)-[:TEAM_INVOLVED]-(t:Team)
        WITH m, collect(DISTINCT t.name) as all_teams
        
        // Get player of match
        OPTIONAL MATCH (m)-[:PLAYER_OF_MATCH]->(pom:Player)
        
        RETURN 
            m.winner as winner,
            [team IN all_teams WHERE team <> m.winner][0] as runner_up,
            m.venue as venue,
            m.outcome_margin as margin,
            m.outcome_type as margin_type,
            pom.name as player_of_match
    """
    final_res = db.query(final_query, {"season": season_year})
    
    details = {
        "season": season_year,
        "total_teams": total_teams,
        "total_matches": total_matches
    }
    
    if final_res and final_res[0]:
        row = final_res[0]
        details["winner"] = row.get('winner')
        details["runner_up"] = row.get('runner_up')
        details["venue"] = row.get('venue')
        details["player_of_match"] = row.get('player_of_match')
        
        # Format margin (e.g. "runs" or "wickets")
        margin_val = row.get('margin')
        margin_type = row.get('margin_type')
        if margin_val and margin_type:
             details["margin"] = f"{margin_val} {margin_type}"
    
    # Get official Player of Tournament from mapping
    details["player_of_tournament"] = PLAYER_OF_TOURNAMENT_MAP.get(season_year)
    
    # Apply manual runner-up override if applicable
    if season_year in RUNNER_UP_OVERRIDE_MAP:
        details["runner_up"] = RUNNER_UP_OVERRIDE_MAP[season_year]
    
    return SeasonDetails(**details)

@app.get("/api/seasons", response_model=List[SeasonStats])
async def get_seasons():
    """Get statistics for all seasons"""
    results = db.query("""
        MATCH (m:Match)
        WITH m.season as season_val, COUNT(*) as match_count
        RETURN toString(season_val) as season, match_count as matches
        ORDER BY season DESC
    """)
    return [SeasonStats(**r) for r in results]

# ==================== PLAYER ENDPOINTS ====================
@app.get("/api/batsmen/top", response_model=List[Player])
async def get_top_batsmen(limit: int = 20):
    """Get top run scorers"""
    results = db.query(f"""
        MATCH (p:Player)-[bs:BATTING_STATS]->(m:Match)
        WITH p, SUM(bs.runs) as total_runs, COUNT(m) as matches, 
             SUM(bs.balls) as balls
        WHERE total_runs > 0
        RETURN p.name as name, 
               total_runs as runs, 
               matches as matches,
               CASE WHEN balls > 0 THEN ROUND(total_runs * 100.0 / balls, 2) ELSE 0 END as strike_rate
        ORDER BY total_runs DESC
        LIMIT {limit}
    """)
    return [Player(**r) for r in results]

@app.get("/api/bowlers/top", response_model=List[Player])
async def get_top_bowlers(limit: int = 20):
    """Get top wicket takers"""
    results = db.query(f"""
        MATCH (p:Player)-[bw:BOWLING_STATS]->(m:Match)
        WITH p, SUM(bw.wickets) as total_wickets, COUNT(m) as matches,
             SUM(bw.runs_conceded) as runs_conceded, SUM(bw.balls) as balls
        WHERE total_wickets > 0
        RETURN p.name as name,
               total_wickets as wickets,
               matches as matches,
               CASE WHEN balls > 0 THEN ROUND(runs_conceded * 6.0 / balls, 2) ELSE 0 END as economy
        ORDER BY total_wickets DESC
        LIMIT {limit}
    """)
    return [Player(**r) for r in results]

@app.get("/api/player/{player_name}")
async def get_player_stats(player_name: str):
    """Get detailed stats for a specific player"""
    results = db.query("""
        MATCH (p:Player {name: $name})
        OPTIONAL MATCH (p)-[bs:BATTING_STATS]->(m:Match)
        WITH p, 
             COUNT(DISTINCT m) as batting_matches,
             SUM(bs.runs) as total_runs,
             SUM(bs.balls) as total_balls,
             SUM(bs.fours) as total_fours,
             SUM(bs.sixes) as total_sixes
        OPTIONAL MATCH (p)-[bw:BOWLING_STATS]->(m:Match)
        WITH p, batting_matches, total_runs, total_balls, total_fours, total_sixes,
             COUNT(DISTINCT m) as bowling_matches,
             SUM(bw.wickets) as total_wickets,
             SUM(bw.runs_conceded) as runs_conceded,
             SUM(bw.balls) as bowling_balls
        RETURN p.name as name,
               batting_matches,
               total_runs,
               CASE WHEN total_balls > 0 THEN ROUND(total_runs * 100.0 / total_balls, 2) ELSE 0 END as strike_rate,
               total_fours,
               total_sixes,
               bowling_matches,
               total_wickets,
               runs_conceded,
               CASE WHEN bowling_balls > 0 THEN ROUND(runs_conceded * 6.0 / bowling_balls, 2) ELSE 0 END as economy
    """, {'name': player_name})
    
    if not results:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return results[0]

@app.get("/api/players/search")
async def search_players(query: str, limit: int = 20):
    """Search for players by name"""
    results = db.query(f"""
        MATCH (p:Player)
        WHERE toUpper(p.name) CONTAINS $query
        RETURN p.name as name
        ORDER BY p.name
        LIMIT {limit}
    """, {'query': query.upper()})
    
    return [r['name'] for r in results]

# ==================== TEAM ENDPOINTS ====================
@app.get("/api/teams")
async def get_teams():
    """Get all teams, normalized by rebrands, sorted by active status"""
    # 1. Get ALL teams ever
    all_teams_result = db.query("MATCH (t:Team) RETURN DISTINCT t.name as name")
    
    # 2. Get Teams active in the LATEST season
    active_teams_result = db.query("""
        MATCH (m:Match)
        WITH MAX(m.season) as latest_season
        MATCH (t:Team)-[:TEAM_INVOLVED]-(:Match {season: latest_season})
        RETURN DISTINCT t.name as name
    """)
    
    active_names = {REBRAND_MAP.get(r['name'], r['name']) for r in active_teams_result}
    
    team_map = {}
    for row in all_teams_result:
        raw_name = row['name']
        normalized_name = REBRAND_MAP.get(raw_name, raw_name)
        
        if normalized_name not in team_map:
            team_map[normalized_name] = {
                "name": normalized_name,
                "is_active": normalized_name in active_names,
                "raw_names": [raw_name]
            }
        else:
            if raw_name not in team_map[normalized_name]["raw_names"]:
                team_map[normalized_name]["raw_names"].append(raw_name)

    # Convert to list and sort: Active first (A-Z), then Defunct (A-Z)
    # Using .lower() for case-insensitive alphabetical sorting
    teams = list(team_map.values())
    teams.sort(key=lambda x: (not x['is_active'], x['name'].lower()))
    return teams

@app.get("/api/franchises") # Keep for backward compatibility but redirect logic
async def get_franchises():
    return await get_teams()

@app.get("/api/team/{team_name}/stats")
async def get_team_stats(team_name: str):
    """Get team statistics, including history for rebranded teams"""
    # Find all raw names associated with this normalized name
    raw_names = [team_name]
    for old_name, new_name in REBRAND_MAP.items():
        if new_name == team_name:
            raw_names.append(old_name)
        elif old_name == team_name:
            # If user passed an old name (e.g. DD), search for all related
            target_current = REBRAND_MAP[old_name]
            raw_names = [target_current]
            for o, n in REBRAND_MAP.items():
                if n == target_current:
                    raw_names.append(o)
            break

    results = db.query("""
        MATCH (t:Team)
        WHERE t.name IN $names
        MATCH (t)-[:TEAM_INVOLVED]-(m:Match)
        RETURN COUNT(DISTINCT m) as total_matches,
               SUM(CASE WHEN (m)-[:WON_BY]->(t) THEN 1 ELSE 0 END) as wins
    """, {'names': list(set(raw_names))})
    
    if not results or results[0]['total_matches'] == 0:
        raise HTTPException(status_code=404, detail="Team not found")
    
    stats = results[0]
    matches = stats['total_matches'] or 0
    wins = stats['wins'] or 0
    win_percentage = (wins / matches * 100) if matches > 0 else 0
    
    return {
        "name": team_name,
        "total_matches": matches,
        "wins": wins,
        "win_percentage": round(win_percentage, 2)
    }

@app.get("/api/team/{team_name}/squad")
async def get_team_squad(team_name: str, limit: int = 50):
    """Get team squad (players who played for any variant of the team)"""
    # Find all raw names associated with this normalized name
    raw_names = [team_name]
    for old_name, new_name in REBRAND_MAP.items():
        if new_name == team_name:
            raw_names.append(old_name)
            
    results = db.query(f"""
        MATCH (t:Team)
        WHERE t.name IN $names
        MATCH (t)-[:SELECTED_PLAYER]-(p:Player)
        RETURN DISTINCT p.name as name
        ORDER BY p.name
        LIMIT {limit}
    """, {'names': list(set(raw_names))})
    
    return [r['name'] for r in results]

# ==================== HEAD-TO-HEAD ENDPOINTS ====================
@app.get("/api/h2h/{team1}/{team2}")
async def get_head_to_head(team1: str, team2: str):
    """Get head-to-head record between two teams"""
    # Find all raw names associated with these normalized names
    names1 = [team1]
    for old_name, new_name in REBRAND_MAP.items():
        if new_name == team1:
            names1.append(old_name)
            
    names2 = [team2]
    for old_name, new_name in REBRAND_MAP.items():
        if new_name == team2:
            names2.append(old_name)
            
    results = db.query("""
        MATCH (t1:Team) WHERE t1.name IN $names1
        MATCH (t2:Team) WHERE t2.name IN $names2
        OPTIONAL MATCH (t1)-[r:TEAM_INVOLVED]-(m:Match)-[r2:TEAM_INVOLVED]-(t2)
        WITH t1, m
        RETURN COUNT(DISTINCT m) as total_matches,
               SUM(CASE WHEN (m)-[:WON_BY]->(t1) THEN 1 ELSE 0 END) as team1_wins
    """, {'names1': list(set(names1)), 'names2': list(set(names2))})
    
    if not results or results[0]['total_matches'] == 0:
        return {
            "total_matches": 0,
            "team1": team1,
            "team1_wins": 0,
            "team2": team2,
            "team2_wins": 0
        }
    
    data = results[0]
    total = data['total_matches'] or 0
    team1_wins = data['team1_wins'] or 0
    team2_wins = total - team1_wins
    
    return {
        "total_matches": total,
        "team1": team1,
        "team1_wins": team1_wins,
        "team2": team2,
        "team2_wins": team2_wins
    }

@app.get("/api/h2h/{team1}/{team2}/matches")
async def get_h2h_matches(team1: str, team2: str, limit: int = 50):
    """Get recent matches between two teams"""
    # Find all raw names associated with these normalized names
    names1 = [team1]
    for old_name, new_name in REBRAND_MAP.items():
        if new_name == team1:
            names1.append(old_name)
            
    names2 = [team2]
    for old_name, new_name in REBRAND_MAP.items():
        if new_name == team2:
            names2.append(old_name)

    results = db.query(f"""
        MATCH (t1:Team) WHERE t1.name IN $names1
        MATCH (t2:Team) WHERE t2.name IN $names2
        MATCH (t1)-[r:TEAM_INVOLVED]-(m:Match)-[r2:TEAM_INVOLVED]-(t2)
        MATCH (m)-[:WON_BY]->(winner:Team)
        RETURN m.date as date, m.season as season,
               winner.name as winning_team_name,
               m.venue as venue,
               m.outcome_margin as outcome_margin,
               m.outcome_type as outcome_type
        ORDER BY m.date DESC
        LIMIT {limit}
    """, {'names1': list(set(names1)), 'names2': list(set(names2))})
    
    # Normalize winner name and format margin
    for r in results:
        w_name = r['winning_team_name']
        if w_name in names1:
            r['winner'] = team1
        else:
            r['winner'] = team2
        
        # Format margin (e.g., "12 runs")
        margin_val = r.get('outcome_margin')
        margin_type = r.get('outcome_type')
        if margin_val and margin_type:
            r['margin'] = f"{margin_val} {margin_type}"
        else:
            r['margin'] = "N/A"
            
        del r['winning_team_name']
        del r['outcome_margin']
        del r['outcome_type']
        
    return results

# ==================== TRENDS ENDPOINTS ====================
@app.get("/api/trends/runs-by-season")
async def get_runs_trend():
    """Get total runs scored across seasons"""
    results = db.query("""
        MATCH (p:Player)-[bs:BATTING_STATS]->(m:Match)
        RETURN m.season as season, SUM(bs.runs) as total_runs
        ORDER BY season
    """)
    return results

@app.get("/api/trends/wickets-by-season")
async def get_wickets_trend():
    """Get total wickets across seasons"""
    results = db.query("""
        MATCH (p:Player)-[bw:BOWLING_STATS]->(m:Match)
        RETURN m.season as season, SUM(bw.wickets) as total_wickets
        ORDER BY season
    """)
    return results

# ==================== STARTUP/SHUTDOWN ====================
@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown"""
    db.close()
    logger.info("✓ Database connection closed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
