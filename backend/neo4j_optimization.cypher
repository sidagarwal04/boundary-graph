"""
Neo4j Query Optimization Guide for IPL Cricket Database
=======================================================

This file contains optimized queries and indexing strategies to improve performance.
Execute these in Neo4j Browser or using cypher-shell for best performance.
"""

# ==================== INDEXES FOR PERFORMANCE ====================

# Primary indexes on frequently queried fields
CREATE INDEX player_name_index IF NOT EXISTS FOR (p:Player) ON (p.name);
CREATE INDEX team_name_index IF NOT EXISTS FOR (t:Team) ON (t.name);
CREATE INDEX match_season_index IF NOT EXISTS FOR (m:Match) ON (m.season);
CREATE INDEX match_venue_index IF NOT EXISTS FOR (m:Match) ON (m.venue);
CREATE INDEX match_winner_index IF NOT EXISTS FOR (m:Match) ON (m.winner);
CREATE INDEX match_date_index IF NOT EXISTS FOR (m:Match) ON (m.date);

# Composite indexes for complex queries
CREATE INDEX match_season_winner IF NOT EXISTS FOR (m:Match) ON (m.season, m.winner);
CREATE INDEX match_venue_season IF NOT EXISTS FOR (m:Match) ON (m.venue, m.season);

# Delivery indexes for ball-by-ball analysis
CREATE INDEX delivery_over_ball IF NOT EXISTS FOR (d:Delivery) ON (d.over, d.ball);
CREATE INDEX delivery_runs_index IF NOT EXISTS FOR (d:Delivery) ON (d.runs_total);

# ==================== QUERY OPTIMIZATION PATTERNS ====================

# Instead of: MATCH (p:Player) WHERE p.name CONTAINS 'virat'
# Use: MATCH (p:Player) WHERE toLower(p.name) CONTAINS toLower('virat')
# Better: Create fulltext index and use db.index.fulltext.queryNodes()

# For top batsmen - optimized version:
MATCH (p:Player)-[bs:BATTING_STATS]->(m:Match)
WITH p, SUM(bs.runs) as total_runs, COUNT(m) as matches, SUM(bs.balls) as total_balls
WHERE total_runs > 0
RETURN p.name as name, 
       total_runs as runs, 
       matches,
       CASE WHEN total_balls > 0 THEN ROUND(total_runs * 100.0 / total_balls, 2) ELSE 0 END as strike_rate
ORDER BY total_runs DESC
LIMIT 20;

# For venue statistics - optimized version:
MATCH (m:Match)
WHERE m.venue IS NOT NULL AND m.winner IS NOT NULL
WITH m.venue as venue_name, 
     COUNT(m) as total_matches,
     SUM(CASE WHEN m.toss_decision = 'bat' AND m.toss_winner = m.winner THEN 1 ELSE 0 END) as bat_first_wins,
     SUM(CASE WHEN m.toss_decision = 'field' AND m.toss_winner = m.winner THEN 1 ELSE 0 END) as chase_wins
WHERE total_matches >= 5
RETURN venue_name,
       total_matches,
       ROUND(100.0 * bat_first_wins / total_matches, 1) as bat_first_win_pct,
       ROUND(100.0 * chase_wins / total_matches, 1) as chase_win_pct
ORDER BY total_matches DESC;

# ==================== PERFORMANCE MONITORING ====================

# Query to identify slow queries (Neo4j 4.0+)
CALL db.stats.retrieve('query.execution') YIELD data
UNWIND data as row
WITH row
WHERE row.planning + row.cpu > 1000 // queries taking > 1 second
RETURN row.query, row.planning, row.cpu, row.waiting, row.hits;

# Query to check index usage
CALL db.indexes() YIELD name, state, populationPercent, type
RETURN name, state, populationPercent, type
ORDER BY populationPercent DESC;

# ==================== CACHE WARMING QUERIES ====================
# Execute these after system restart to warm up frequently accessed data

# Warm up overview data
MATCH (m:Match) 
WITH COUNT(m) as matches, 
     COUNT(DISTINCT m.season) as seasons,
     COUNT(DISTINCT m.venue) as venues
RETURN matches, seasons, venues;

# Warm up top players
MATCH (p:Player)-[bs:BATTING_STATS]->(m:Match)
WITH p, SUM(bs.runs) as total_runs
WHERE total_runs > 1000
RETURN COUNT(p) as top_batsmen;

MATCH (p:Player)-[bow:BOWLING_STATS]->(m:Match)
WITH p, SUM(bow.wickets) as total_wickets
WHERE total_wickets > 50
RETURN COUNT(p) as top_bowlers;

# ==================== AGGREGATION OPTIMIZATIONS ====================

# Pre-calculate common aggregations and store as properties
# (These would typically be run as scheduled maintenance queries)

# Calculate season-wise team performance
MATCH (t:Team)-[:TEAM_INVOLVED]->(m:Match)
WHERE m.season IS NOT NULL
WITH t, m.season as season, COUNT(m) as matches_played,
     SUM(CASE WHEN t.name = m.winner THEN 1 ELSE 0 END) as wins
SET t:SeasonStats {
    season: season,
    matches: matches_played,
    wins: wins,
    win_percentage: ROUND(100.0 * wins / matches_played, 2)
};

# ==================== MEMORY USAGE OPTIMIZATION ====================

# For large result sets, use pagination
# Instead of returning all results:
MATCH (p:Player)-[bs:BATTING_STATS]->(m:Match)
WITH p, SUM(bs.runs) as total_runs
ORDER BY total_runs DESC
SKIP 0 LIMIT 20  // Paginate results
RETURN p.name, total_runs;

# Use DISTINCT carefully - it can be expensive
# Instead of: MATCH (p:Player) RETURN DISTINCT p.name
# Consider: MATCH (p:Player) WITH p.name as name RETURN name

# ==================== QUERY PROFILING ====================

# Profile slow queries to understand execution plan
PROFILE MATCH (p:Player)-[bs:BATTING_STATS]->(m:Match)
WHERE m.season = 2023
WITH p, SUM(bs.runs) as total_runs
RETURN p.name, total_runs
ORDER BY total_runs DESC
LIMIT 10;

# Explain query execution without running it
EXPLAIN MATCH (p:Player)-[bs:BATTING_STATS]->(m:Match)
WHERE m.season = 2023
RETURN p.name, SUM(bs.runs) as total_runs;