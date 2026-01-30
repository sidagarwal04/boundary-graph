import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Set
from datetime import datetime
from neo4j import GraphDatabase
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging with unbuffered output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)
logger = logging.getLogger(__name__)

# Ensure output is unbuffered
sys.stdout = sys.stderr if sys.stdout.isatty() else sys.stdout

class IPLNeo4jImporter:
    """
    Imports IPL JSON match data into Neo4j graph database with ball-by-ball granularity.
    Tracks and logs any skipped/unmapped JSON fields.
    """
    
    # Define all JSON paths we're explicitly handling in our model
    MAPPED_PATHS = {
        'meta.data_version', 'meta.created', 'meta.revision',
        'info.balls_per_over', 'info.city', 'info.dates', 
        'info.event.name', 'info.event.match_number',
        'info.gender', 'info.match_type', 'info.outcome.winner',
        'info.outcome.by.runs', 'info.outcome.by.wickets',
        'info.overs', 'info.player_of_match', 'info.players',
        'info.registry.people', 'info.season', 'info.team_type',
        'info.teams', 'info.toss.decision', 'info.toss.winner',
        'info.venue', 'info.officials.match_referees',
        'info.officials.reserve_umpires', 'info.officials.tv_umpires',
        'info.officials.umpires',
        'innings.team', 'innings.overs', 'innings.powerplays',
        'innings.powerplays.from', 'innings.powerplays.to', 'innings.powerplays.type',
        'innings.target.overs', 'innings.target.runs',
        'innings.overs.over', 'innings.overs.deliveries',
        'innings.overs.deliveries.batter', 'innings.overs.deliveries.bowler',
        'innings.overs.deliveries.non_striker', 'innings.overs.deliveries.runs',
        'innings.overs.deliveries.runs.batter', 'innings.overs.deliveries.runs.extras',
        'innings.overs.deliveries.runs.total', 'innings.overs.deliveries.extras',
        'innings.overs.deliveries.wickets', 'innings.overs.deliveries.wickets.player_out',
        'innings.overs.deliveries.wickets.kind', 'innings.overs.deliveries.wickets.fielders',
        'innings.overs.deliveries.review', 'innings.overs.deliveries.replacements',
        'innings.overs.deliveries.runs.non_boundary'
    }
    
    def __init__(self, uri: str, username: str, password: str, json_folder: str):
        """
        Initialize the importer.
        
        Args:
            uri: Neo4j connection URI (e.g., 'bolt://localhost:7687')
            username: Neo4j username
            password: Neo4j password
            json_folder: Path to folder containing IPL JSON files
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.json_folder = Path(json_folder)
        self.skipped_fields_log = "skipped_json_fields.txt"
        self.skipped_fields: Set[str] = set()
        
    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()
        
    def create_constraints_and_indexes(self):
        """Create database constraints and indexes for performance."""
        with self.driver.session() as session:
            constraints_indexes = [
                # Constraints for uniqueness
                "CREATE CONSTRAINT match_id IF NOT EXISTS FOR (m:Match) REQUIRE m.match_id IS UNIQUE",
                "CREATE CONSTRAINT player_id IF NOT EXISTS FOR (p:Player) REQUIRE p.player_id IS UNIQUE",
                "CREATE CONSTRAINT team_name IF NOT EXISTS FOR (t:Team) REQUIRE t.name IS UNIQUE",
                "CREATE CONSTRAINT venue_name IF NOT EXISTS FOR (v:Venue) REQUIRE v.name IS UNIQUE",
                "CREATE CONSTRAINT season_year IF NOT EXISTS FOR (s:Season) REQUIRE s.year IS UNIQUE",
                "CREATE CONSTRAINT official_name IF NOT EXISTS FOR (o:Official) REQUIRE o.name IS UNIQUE",
                
                # Indexes for performance
                "CREATE INDEX delivery_match IF NOT EXISTS FOR (d:Delivery) ON (d.match_id)",
                "CREATE INDEX delivery_innings IF NOT EXISTS FOR (d:Delivery) ON (d.innings_number)",
                "CREATE INDEX innings_match IF NOT EXISTS FOR (i:Innings) ON (i.match_id)",
                "CREATE INDEX over_match IF NOT EXISTS FOR (o:Over) ON (o.match_id)",
                "CREATE INDEX match_season IF NOT EXISTS FOR (m:Match) ON (m.season)",
                "CREATE INDEX match_date IF NOT EXISTS FOR (m:Match) ON (m.date)",
                "CREATE INDEX partnership_match IF NOT EXISTS FOR ()-[p:PARTNERSHIP]-() ON (p.match_id)",
            ]
            
            for statement in constraints_indexes:
                try:
                    session.run(statement)
                    logger.info(f"Executed: {statement[:60]}...")
                except Exception as e:
                    logger.warning(f"Constraint/Index may already exist: {e}")
    
    def track_json_path(self, obj: Any, prefix: str = ""):
        """
        Recursively track all JSON paths to identify unmapped fields.
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                path = f"{prefix}.{key}" if prefix else key
                if path not in self.MAPPED_PATHS:
                    # Check if any child path is mapped
                    is_parent_mapped = any(mp.startswith(path + ".") for mp in self.MAPPED_PATHS)
                    if not is_parent_mapped and not isinstance(value, (dict, list)):
                        self.skipped_fields.add(path)
                self.track_json_path(value, path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self.track_json_path(item, prefix)
    
    def log_skipped_fields(self, match_id: str, data: Dict):
        """Log any JSON fields not mapped in our model."""
        self.track_json_path(data)
        
        if self.skipped_fields:
            with open(self.skipped_fields_log, 'a') as f:
                timestamp = datetime.now().isoformat()
                f.write(f"\n{'='*80}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Match ID: {match_id}\n")
                f.write(f"Skipped Fields:\n")
                for field in sorted(self.skipped_fields):
                    f.write(f"  - {field}\n")
            
            # Clear for next match
            self.skipped_fields.clear()
    
    def get_sorted_json_files(self) -> List[Path]:
        """
        Sort JSON files by season and match date based on README.txt pattern.
        Returns files in chronological order from Season 1, Match 1 onwards.
        """
        json_files = []
        
        # Parse README to get chronological order
        readme_path = self.json_folder / "README.txt"
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                for line in f:
                    if line.strip() and ' - club - IPL - male - ' in line:
                        parts = line.strip().split(' - ')
                        if len(parts) >= 5:
                            match_id = parts[4].strip()
                            json_file = self.json_folder / f"{match_id}.json"
                            if json_file.exists():
                                json_files.append(json_file)
        else:
            # Fallback: sort by filename (match_id)
            json_files = sorted(self.json_folder.glob("*.json"))
        
        # Reverse to get chronological order (oldest first)
        json_files.reverse()
        
        logger.info(f"Found {len(json_files)} JSON files to import")
        return json_files
    
    def import_match(self, session, match_data: Dict, match_id: str):
        """Import a single match with all its ball-by-ball data."""
        
        info = match_data.get('info', {})
        
        # 1. Create/Merge Season
        # 1. Create/Merge Season
        raw_season = info.get('season', 'Unknown')
        
        # Normalize season
        season_mapping = {
            "2007/08": "2008",
            "2009/10": "2010",
            "2020/21": "2020"
        }
        season = str(raw_season)
        if season in season_mapping:
            season = season_mapping[season]

        session.run("""
            MERGE (s:Season {year: $year})
        """, year=season)
        
        # 2. Create/Merge Venue
        venue_name = info.get('venue', 'Unknown')
        city = info.get('city', 'Unknown')
        session.run("""
            MERGE (v:Venue {name: $venue})
            ON CREATE SET v.city = $city
        """, venue=venue_name, city=city)
        
        # 3. Create/Merge Teams (batch)
        teams = info.get('teams', [])
        if teams:
            team_type = info.get('team_type', 'club')
            session.run("""
                UNWIND $teams as team_name
                MERGE (t:Team {name: team_name})
                ON CREATE SET t.team_type = $team_type
            """, teams=teams, team_type=team_type)
        
        # 4. Create/Merge Players (batch)
        registry = info.get('registry', {}).get('people', {})
        if registry:
            players_list = [{'name': name, 'id': pid} for name, pid in registry.items()]
            session.run("""
                UNWIND $players as player
                MERGE (p:Player {player_id: player.id})
                ON CREATE SET p.name = player.name
            """, players=players_list)
        
        # 5. Create/Merge Officials (batch)
        officials = info.get('officials', {})
        if officials:
            officials_list = [{'name': name, 'role': role} 
                            for role, names in officials.items() 
                            for name in names]
            session.run("""
                UNWIND $officials as official
                MERGE (o:Official {name: official.name})
                ON CREATE SET o.role = official.role
            """, officials=officials_list)
        
        # 6. Create Match Node
        outcome = info.get('outcome', {})
        toss = info.get('toss', {})
        event = info.get('event', {})
        
        session.run("""
            MERGE (m:Match {match_id: $match_id})
            ON CREATE SET m.match_id = $match_id,
                m.date = $date,
                m.season = $season,
                m.venue = $venue,
                m.city = $city,
                m.match_number = $match_number,
                m.match_type = $match_type,
                m.gender = $gender,
                m.winner = $winner,
                m.outcome_type = $outcome_type,
                m.outcome_margin = $outcome_margin,
                m.toss_winner = $toss_winner,
                m.toss_decision = $toss_decision,
                m.balls_per_over = $balls_per_over,
                m.overs = $overs
            ON MATCH SET m.date = $date,
                m.season = $season,
                m.venue = $venue,
                m.city = $city,
                m.match_number = $match_number,
                m.match_type = $match_type,
                m.gender = $gender,
                m.winner = $winner,
                m.outcome_type = $outcome_type,
                m.outcome_margin = $outcome_margin,
                m.toss_winner = $toss_winner,
                m.toss_decision = $toss_decision,
                m.balls_per_over = $balls_per_over,
                m.overs = $overs
        """, 
            match_id=match_id,
            date=info.get('dates', ['Unknown'])[0],
            season=season,
            venue=venue_name,
            city=city,
            match_number=event.get('match_number'),
            match_type=info.get('match_type', 'T20'),
            gender=info.get('gender', 'male'),
            winner=outcome.get('winner'),
            outcome_type='runs' if 'runs' in outcome.get('by', {}) else 'wickets' if 'wickets' in outcome.get('by', {}) else None,
            outcome_margin=outcome.get('by', {}).get('runs') or outcome.get('by', {}).get('wickets'),
            toss_winner=toss.get('winner'),
            toss_decision=toss.get('decision'),
            balls_per_over=info.get('balls_per_over', 6),
            overs=info.get('overs', 20)
        )
        
        # 7. Link Match to entities
        session.run("""
            MATCH (m:Match {match_id: $match_id})
            MATCH (s:Season {year: $season})
            MATCH (v:Venue {name: $venue})
            MERGE (m)-[:PLAYED_IN]->(s)
            MERGE (m)-[:HELD_AT]->(v)
        """, match_id=match_id, season=season, venue=venue_name)
        
        # Link teams
        for i, team_name in enumerate(teams):
            role = 'team1' if i == 0 else 'team2'
            session.run("""
                MATCH (m:Match {match_id: $match_id})
                MATCH (t:Team {name: $team})
                MERGE (m)-[:TEAM_INVOLVED {role: $role}]->(t)
            """, match_id=match_id, team=team_name, role=role)
        
        # Link winner
        if outcome.get('winner'):
            session.run("""
                MATCH (m:Match {match_id: $match_id})
                MATCH (t:Team {name: $winner})
                MERGE (m)-[:WON_BY]->(t)
            """, match_id=match_id, winner=outcome['winner'])
        
        # Link toss winner
        if toss.get('winner'):
            session.run("""
                MATCH (m:Match {match_id: $match_id})
                MATCH (t:Team {name: $toss_winner})
                MERGE (m)-[:TOSS_WON_BY]->(t)
            """, match_id=match_id, toss_winner=toss['winner'])
        
        # Link player of match
        pom_list = info.get('player_of_match', [])
        for pom in pom_list:
            player_id = registry.get(pom)
            if player_id:
                session.run("""
                    MATCH (m:Match {match_id: $match_id})
                    MATCH (p:Player {player_id: $player_id})
                    MERGE (m)-[:PLAYER_OF_MATCH]->(p)
                """, match_id=match_id, player_id=player_id)
        
        # Link officials
        for role, names in officials.items():
            for name in names:
                session.run("""
                    MATCH (m:Match {match_id: $match_id})
                    MATCH (o:Official {name: $name})
                    MERGE (m)-[:OFFICIATED_BY {role: $role}]->(o)
                """, match_id=match_id, name=name, role=role)
        
        # Link squad players
        players_dict = info.get('players', {})
        for team_name, player_names in players_dict.items():
            for player_name in player_names:
                player_id = registry.get(player_name)
                if player_id:
                    session.run("""
                        MATCH (t:Team {name: $team})
                        MATCH (p:Player {player_id: $player_id})
                        MERGE (t)-[:SELECTED_PLAYER {match_id: $match_id, season: $season}]->(p)
                    """, team=team_name, player_id=player_id, match_id=match_id, season=season)
        
        # 8. Import Innings and ball-by-ball data
        self.import_innings_data(session, match_data, match_id, registry)
        
    def import_innings_data(self, session, match_data: Dict, match_id: str, registry: Dict):
        """Import innings, overs, and deliveries (ball-by-ball data)."""
        
        innings_list = match_data.get('innings', [])
        
        for innings_idx, innings_data in enumerate(innings_list, 1):
            batting_team = innings_data.get('team')
            target = innings_data.get('target', {})
            powerplays = innings_data.get('powerplays', [])
            
            # Enhanced powerplay handling - store all powerplay phases
            powerplay_data = []
            pp_from = None
            pp_to = None
            for pp in powerplays:
                powerplay_info = {
                    'from_over': pp.get('from'),
                    'to_over': pp.get('to'),
                    'type': pp.get('type', 'mandatory')
                }
                powerplay_data.append(powerplay_info)
                
                # Keep first powerplay for backward compatibility
                if pp_from is None:
                    pp_from = pp.get('from')
                    pp_to = pp.get('to')
            
            # Create Innings node
            innings_id = f"{match_id}_innings_{innings_idx}"
            session.run("""
                MERGE (i:Innings {innings_id: $innings_id})
                ON CREATE SET i.innings_id = $innings_id,
                    i.match_id = $match_id,
                    i.innings_number = $innings_number,
                    i.batting_team = $batting_team,
                    i.total_runs = $total_runs,
                    i.total_wickets = $total_wickets,
                    i.target_runs = $target_runs,
                    i.target_overs = $target_overs,
                    i.powerplay_from = $pp_from,
                    i.powerplay_to = $pp_to,
                    i.powerplay_phases = $powerplay_data
                ON MATCH SET i.match_id = $match_id,
                    i.innings_number = $innings_number,
                    i.batting_team = $batting_team,
                    i.total_runs = $total_runs,
                    i.total_wickets = $total_wickets,
                    i.target_runs = $target_runs,
                    i.target_overs = $target_overs,
                    i.powerplay_from = $pp_from,
                    i.powerplay_to = $pp_to,
                    i.powerplay_phases = $powerplay_data
            """, 
                innings_id=innings_id,
                match_id=match_id,
                innings_number=innings_idx,
                batting_team=batting_team,
                total_runs=0,
                total_wickets=0,
                target_runs=target.get('runs'),
                target_overs=target.get('overs'),
                pp_from=pp_from,
                pp_to=pp_to,
                powerplay_data=powerplay_data
            )
            
            # Link Innings to Match and Team
            session.run("""
                MATCH (m:Match {match_id: $match_id})
                MATCH (i:Innings {innings_id: $innings_id})
                MATCH (t:Team {name: $batting_team})
                MERGE (m)-[:HAS_INNINGS {innings_number: $innings_number}]->(i)
                MERGE (i)-[:BATTING_TEAM]->(t)
            """, match_id=match_id, innings_id=innings_id, batting_team=batting_team, innings_number=innings_idx)
            
            # Import overs and deliveries
            overs_list = innings_data.get('overs', [])
            delivery_counter = 0
            
            for over_data in overs_list:
                over_number = over_data.get('over')
                over_id = f"{innings_id}_over_{over_number}"
                
                # Create Over node
                session.run("""
                    MERGE (o:Over {over_id: $over_id})
                    ON CREATE SET o.over_id = $over_id,
                        o.innings_id = $innings_id,
                        o.match_id = $match_id,
                        o.over_number = $over_number
                    ON MATCH SET o.innings_id = $innings_id,
                        o.match_id = $match_id,
                        o.over_number = $over_number
                """, over_id=over_id, innings_id=innings_id, match_id=match_id, over_number=over_number)
                
                # Link Over to Innings
                session.run("""
                    MATCH (i:Innings {innings_id: $innings_id})
                    MATCH (o:Over {over_id: $over_id})
                    MERGE (i)-[:HAS_OVER {over_number: $over_number}]->(o)
                """, innings_id=innings_id, over_id=over_id, over_number=over_number)
                
                # Import deliveries (batch all at once for speed)
                deliveries = over_data.get('deliveries', [])
                
                if deliveries:
                    # Build delivery list for batch processing
                    delivery_list = []
                    relationships = []  # Track relationships to create later
                    
                    for ball_idx, delivery in enumerate(deliveries, 1):
                        delivery_counter += 1
                        delivery_id = f"{over_id}_ball_{ball_idx}"
                        
                        # Determine which powerplay phase this delivery is in
                        current_powerplay = None
                        for pp in powerplay_data:
                            if pp['from_over'] <= over_number <= pp['to_over']:
                                current_powerplay = pp['type']
                                break
                        
                        runs = delivery.get('runs', {})
                        extras = delivery.get('extras', {})
                        wickets = delivery.get('wickets', [])
                        review = delivery.get('review', {})
                        
                        extras_type = list(extras.keys())[0] if extras else None
                        is_wicket = len(wickets) > 0
                        wicket_kind = wickets[0].get('kind') if wickets else None
                        
                        delivery_list.append({
                            'delivery_id': delivery_id,
                            'match_id': match_id,
                            'innings_id': innings_id,
                            'over_id': over_id,
                            'delivery_number': delivery_counter,
                            'over_number': over_number,
                            'ball_in_over': ball_idx,
                            'powerplay_phase': current_powerplay,
                            'runs_batter': runs.get('batter', 0),
                            'runs_extras': runs.get('extras', 0),
                            'runs_total': runs.get('total', 0),
                            'extras_type': extras_type,
                            'is_wicket': is_wicket,
                            'wicket_kind': wicket_kind,
                            'is_boundary': runs.get('batter', 0) == 4,
                            'is_six': runs.get('batter', 0) == 6,
                            'is_non_boundary': runs.get('non_boundary', False),
                            'review_by': review.get('by'),
                            'review_umpire': review.get('umpire'),
                            'review_decision': review.get('decision'),
                            'review_type': review.get('type'),
                            'umpires_call': review.get('umpires_call')
                        })
                        
                        # Track relationships
                        batter = delivery.get('batter')
                        bowler = delivery.get('bowler')
                        non_striker = delivery.get('non_striker')
                        
                        batter_id = registry.get(batter)
                        bowler_id = registry.get(bowler)
                        non_striker_id = registry.get(non_striker)
                        
                        # Add HAS_DELIVERY relationship
                        relationships.append({
                            'type': 'HAS_DELIVERY',
                            'from_id': over_id,
                            'to_id': delivery_id,
                            'from_type': 'Over',
                            'to_type': 'Delivery',
                            'position': ball_idx
                        })
                        
                        # Add player relationships
                        if bowler_id:
                            relationships.append({
                                'type': 'BOWLED_BY',
                                'from_id': delivery_id,
                                'to_id': bowler_id,
                                'from_type': 'Delivery',
                                'to_type': 'Player'
                            })
                        
                        if batter_id:
                            relationships.append({
                                'type': 'FACED_BY',
                                'from_id': delivery_id,
                                'to_id': batter_id,
                                'from_type': 'Delivery',
                                'to_type': 'Player'
                            })
                        
                        if non_striker_id:
                            relationships.append({
                                'type': 'NON_STRIKER',
                                'from_id': delivery_id,
                                'to_id': non_striker_id,
                                'from_type': 'Delivery',
                                'to_type': 'Player'
                            })
                        
                        # Add dismissal relationships
                        if is_wicket and wickets:
                            player_out = wickets[0].get('player_out')
                            player_out_id = registry.get(player_out) if player_out else None
                            
                            if player_out_id:
                                relationships.append({
                                    'type': 'DISMISSED',
                                    'from_id': delivery_id,
                                    'to_id': player_out_id,
                                    'from_type': 'Delivery',
                                    'to_type': 'Player',
                                    'kind': wicket_kind
                                })
                                
                                # Add fielder relationships
                                fielders = wickets[0].get('fielders', [])
                                for fielder_info in fielders:
                                    fielder_name = fielder_info.get('name')
                                    fielder_id = registry.get(fielder_name)
                                    
                                    if fielder_id:
                                        if wicket_kind == 'caught':
                                            relationships.append({
                                                'type': 'CAUGHT_BY',
                                                'from_id': delivery_id,
                                                'to_id': fielder_id,
                                                'from_type': 'Delivery',
                                                'to_type': 'Player',
                                                'substitute': fielder_info.get('substitute', False)
                                            })
                                        elif wicket_kind == 'stumped':
                                            relationships.append({
                                                'type': 'STUMPED_BY',
                                                'from_id': delivery_id,
                                                'to_id': fielder_id,
                                                'from_type': 'Delivery',
                                                'to_type': 'Player',
                                                'substitute': fielder_info.get('substitute', False)
                                            })
                                        elif wicket_kind == 'run out':
                                            relationships.append({
                                                'type': 'RUN_OUT_BY',
                                                'from_id': delivery_id,
                                                'to_id': fielder_id,
                                                'from_type': 'Delivery',
                                                'to_type': 'Player',
                                                'substitute': fielder_info.get('substitute', False)
                                            })
                    
                    # Batch create all deliveries
                    if delivery_list:
                        session.run("""
                            UNWIND $deliveries as d
                            MERGE (del:Delivery {delivery_id: d.delivery_id})
                            ON CREATE SET 
                                del.delivery_id = d.delivery_id,
                                del.match_id = d.match_id,
                                del.innings_id = d.innings_id,
                                del.over_id = d.over_id,
                                del.delivery_number = d.delivery_number,
                                del.over_number = d.over_number,
                                del.ball_in_over = d.ball_in_over,
                                del.runs_batter = d.runs_batter,
                                del.runs_extras = d.runs_extras,
                                del.runs_total = d.runs_total,
                                del.extras_type = d.extras_type,
                                del.is_wicket = d.is_wicket,
                                del.wicket_kind = d.wicket_kind,
                                del.is_boundary = d.is_boundary,
                                del.is_six = d.is_six,
                                del.is_non_boundary = d.is_non_boundary,
                                del.review_by = d.review_by,
                                del.review_umpire = d.review_umpire,
                                del.review_decision = d.review_decision,
                                del.review_type = d.review_type,
                                del.umpires_call = d.umpires_call
                            ON MATCH SET 
                                del.match_id = d.match_id,
                                del.innings_id = d.innings_id,
                                del.over_id = d.over_id,
                                del.delivery_number = d.delivery_number,
                                del.over_number = d.over_number,
                                del.ball_in_over = d.ball_in_over,
                                del.runs_batter = d.runs_batter,
                                del.runs_extras = d.runs_extras,
                                del.runs_total = d.runs_total,
                                del.extras_type = d.extras_type,
                                del.is_wicket = d.is_wicket,
                                del.wicket_kind = d.wicket_kind,
                                del.is_boundary = d.is_boundary,
                                del.is_six = d.is_six,
                                del.is_non_boundary = d.is_non_boundary,
                                del.review_by = d.review_by,
                                del.review_umpire = d.review_umpire,
                                del.review_decision = d.review_decision,
                                del.review_type = d.review_type,
                                del.umpires_call = d.umpires_call
                        """, deliveries=delivery_list)
                    
                    # Batch create relationships
                    if relationships:
                        # HAS_DELIVERY relationships
                        has_delivery_rels = [r for r in relationships if r['type'] == 'HAS_DELIVERY']
                        if has_delivery_rels:
                            session.run("""
                                UNWIND $relationships as r
                                MATCH (o:Over {over_id: r.from_id})
                                MATCH (d:Delivery {delivery_id: r.to_id})
                                MERGE (o)-[:HAS_DELIVERY {position: r.position}]->(d)
                            """, relationships=has_delivery_rels)
                        
                        # BOWLED_BY relationships
                        bowled_by_rels = [r for r in relationships if r['type'] == 'BOWLED_BY']
                        if bowled_by_rels:
                            session.run("""
                                UNWIND $relationships as r
                                MATCH (d:Delivery {delivery_id: r.from_id})
                                MATCH (p:Player {player_id: r.to_id})
                                MERGE (d)-[:BOWLED_BY]->(p)
                            """, relationships=bowled_by_rels)
                        
                        # FACED_BY relationships
                        faced_by_rels = [r for r in relationships if r['type'] == 'FACED_BY']
                        if faced_by_rels:
                            session.run("""
                                UNWIND $relationships as r
                                MATCH (d:Delivery {delivery_id: r.from_id})
                                MATCH (p:Player {player_id: r.to_id})
                                MERGE (d)-[:FACED_BY]->(p)
                            """, relationships=faced_by_rels)
                        
                        # NON_STRIKER relationships
                        non_striker_rels = [r for r in relationships if r['type'] == 'NON_STRIKER']
                        if non_striker_rels:
                            session.run("""
                                UNWIND $relationships as r
                                MATCH (d:Delivery {delivery_id: r.from_id})
                                MATCH (p:Player {player_id: r.to_id})
                                MERGE (d)-[:NON_STRIKER]->(p)
                            """, relationships=non_striker_rels)
                        
                        # DISMISSED relationships
                        dismissed_rels = [r for r in relationships if r['type'] == 'DISMISSED']
                        if dismissed_rels:
                            session.run("""
                                UNWIND $relationships as r
                                MATCH (d:Delivery {delivery_id: r.from_id})
                                MATCH (p:Player {player_id: r.to_id})
                                MERGE (d)-[:DISMISSED {kind: r.kind}]->(p)
                            """, relationships=dismissed_rels)
                        
                        # CAUGHT_BY relationships
                        caught_by_rels = [r for r in relationships if r['type'] == 'CAUGHT_BY']
                        if caught_by_rels:
                            session.run("""
                                UNWIND $relationships as r
                                MATCH (d:Delivery {delivery_id: r.from_id})
                                MATCH (p:Player {player_id: r.to_id})
                                MERGE (d)-[:CAUGHT_BY {substitute: r.substitute}]->(p)
                            """, relationships=caught_by_rels)
                        
                        # STUMPED_BY relationships
                        stumped_by_rels = [r for r in relationships if r['type'] == 'STUMPED_BY']
                        if stumped_by_rels:
                            session.run("""
                                UNWIND $relationships as r
                                MATCH (d:Delivery {delivery_id: r.from_id})
                                MATCH (p:Player {player_id: r.to_id})
                                MERGE (d)-[:STUMPED_BY {substitute: r.substitute}]->(p)
                            """, relationships=stumped_by_rels)
                        
                        # RUN_OUT_BY relationships
                        run_out_by_rels = [r for r in relationships if r['type'] == 'RUN_OUT_BY']
                        if run_out_by_rels:
                            session.run("""
                                UNWIND $relationships as r
                                MATCH (d:Delivery {delivery_id: r.from_id})
                                MATCH (p:Player {player_id: r.to_id})
                                MERGE (d)-[:RUN_OUT_BY {substitute: r.substitute}]->(p)
                            """, relationships=run_out_by_rels)
    
    def import_delivery(self, session, delivery: Dict, over_id: str, match_id: str, 
                       innings_id: str, over_number: int, ball_in_over: int, 
                       delivery_number: int, registry: Dict):
        """Import a single delivery (ball) with all its details."""
        
        # Extract delivery data
        batter = delivery.get('batter')
        bowler = delivery.get('bowler')
        non_striker = delivery.get('non_striker')
        runs = delivery.get('runs', {})
        extras = delivery.get('extras', {})
        wickets = delivery.get('wickets', [])
        review = delivery.get('review', {})
        replacements = delivery.get('replacements', {})
        
        # Get player IDs
        batter_id = registry.get(batter)
        bowler_id = registry.get(bowler)
        non_striker_id = registry.get(non_striker)
        
        # Determine extras type
        extras_type = None
        if extras:
            extras_type = list(extras.keys())[0] if extras else None
        
        # Wicket info
        is_wicket = len(wickets) > 0
        wicket_kind = wickets[0].get('kind') if wickets else None
        player_out = wickets[0].get('player_out') if wickets else None
        player_out_id = registry.get(player_out) if player_out else None
        
        # Create Delivery node
        delivery_id = f"{over_id}_ball_{ball_in_over}"
        
        session.run("""
            MERGE (d:Delivery {delivery_id: $delivery_id})
            ON CREATE SET d.delivery_id = $delivery_id,
                d.match_id = $match_id,
                d.innings_id = $innings_id,
                d.over_id = $over_id,
                d.delivery_number = $delivery_number,
                d.over_number = $over_number,
                d.ball_in_over = $ball_in_over,
                d.runs_batter = $runs_batter,
                d.runs_extras = $runs_extras,
                d.runs_total = $runs_total,
                d.extras_type = $extras_type,
                d.is_wicket = $is_wicket,
                d.wicket_kind = $wicket_kind,
                d.is_boundary = $is_boundary,
                d.is_six = $is_six,
                d.is_non_boundary = $is_non_boundary,
                d.review_by = $review_by,
                d.review_umpire = $review_umpire,
                d.review_decision = $review_decision,
                d.review_type = $review_type,
                d.umpires_call = $umpires_call
            ON MATCH SET d.match_id = $match_id,
                d.innings_id = $innings_id,
                d.over_id = $over_id,
                d.delivery_number = $delivery_number,
                d.over_number = $over_number,
                d.ball_in_over = $ball_in_over,
                d.runs_batter = $runs_batter,
                d.runs_extras = $runs_extras,
                d.runs_total = $runs_total,
                d.extras_type = $extras_type,
                d.is_wicket = $is_wicket,
                d.wicket_kind = $wicket_kind,
                d.is_boundary = $is_boundary,
                d.is_six = $is_six,
                d.is_non_boundary = $is_non_boundary,
                d.review_by = $review_by,
                d.review_umpire = $review_umpire,
                d.review_decision = $review_decision,
                d.review_type = $review_type,
                d.umpires_call = $umpires_call
        """,
            delivery_id=delivery_id,
            match_id=match_id,
            innings_id=innings_id,
            over_id=over_id,
            delivery_number=delivery_number,
            over_number=over_number,
            ball_in_over=ball_in_over,
            runs_batter=runs.get('batter', 0),
            runs_extras=runs.get('extras', 0),
            runs_total=runs.get('total', 0),
            extras_type=extras_type,
            is_wicket=is_wicket,
            wicket_kind=wicket_kind,
            is_boundary=(runs.get('batter', 0) == 4),
            is_six=(runs.get('batter', 0) == 6),
            is_non_boundary=runs.get('non_boundary', False),
            review_by=review.get('by'),
            review_umpire=review.get('umpire'),
            review_decision=review.get('decision'),
            review_type=review.get('type'),
            umpires_call=review.get('umpires_call')
        )
        
        # Link Delivery to Over
        session.run("""
            MATCH (o:Over {over_id: $over_id})
            MATCH (d:Delivery {delivery_id: $delivery_id})
            MERGE (o)-[:HAS_DELIVERY {position: $ball_in_over}]->(d)
        """, over_id=over_id, delivery_id=delivery_id, ball_in_over=ball_in_over)
        
        # Link bowler, batter, non-striker
        if bowler_id:
            session.run("""
                MATCH (d:Delivery {delivery_id: $delivery_id})
                MATCH (p:Player {player_id: $player_id})
                MERGE (d)-[:BOWLED_BY]->(p)
            """, delivery_id=delivery_id, player_id=bowler_id)
        
        if batter_id:
            session.run("""
                MATCH (d:Delivery {delivery_id: $delivery_id})
                MATCH (p:Player {player_id: $player_id})
                MERGE (d)-[:FACED_BY]->(p)
            """, delivery_id=delivery_id, player_id=batter_id)
        
        if non_striker_id:
            session.run("""
                MATCH (d:Delivery {delivery_id: $delivery_id})
                MATCH (p:Player {player_id: $player_id})
                MERGE (d)-[:NON_STRIKER]->(p)
            """, delivery_id=delivery_id, player_id=non_striker_id)
        
        # Handle wickets
        if is_wicket and player_out_id:
            session.run("""
                MATCH (d:Delivery {delivery_id: $delivery_id})
                MATCH (p:Player {player_id: $player_id})
                MERGE (d)-[:DISMISSED {kind: $kind}]->(p)
            """, delivery_id=delivery_id, player_id=player_out_id, kind=wicket_kind)
            
            # Link fielders involved in dismissal
            fielders = wickets[0].get('fielders', [])
            for fielder_info in fielders:
                fielder_name = fielder_info.get('name')
                fielder_id = registry.get(fielder_name)
                is_substitute = fielder_info.get('substitute', False)
                
                if fielder_id:
                    if wicket_kind == 'caught':
                        session.run("""
                            MATCH (d:Delivery {delivery_id: $delivery_id})
                            MATCH (p:Player {player_id: $player_id})
                            MERGE (d)-[:CAUGHT_BY {substitute: $sub}]->(p)
                        """, delivery_id=delivery_id, player_id=fielder_id, sub=is_substitute)
                    elif wicket_kind == 'stumped':
                        session.run("""
                            MATCH (d:Delivery {delivery_id: $delivery_id})
                            MATCH (p:Player {player_id: $player_id})
                            MERGE (d)-[:STUMPED_BY {substitute: $sub}]->(p)
                        """, delivery_id=delivery_id, player_id=fielder_id, sub=is_substitute)
                    elif wicket_kind == 'run out':
                        session.run("""
                            MATCH (d:Delivery {delivery_id: $delivery_id})
                            MATCH (p:Player {player_id: $player_id})
                            MERGE (d)-[:RUN_OUT_BY {substitute: $sub}]->(p)
                        """, delivery_id=delivery_id, player_id=fielder_id, sub=is_substitute)
        
        # Handle impact player replacements
        if replacements:
            match_replacements = replacements.get('match', [])
            for replacement in match_replacements:
                player_in = replacement.get('in')
                player_out = replacement.get('out')
                reason = replacement.get('reason')
                team = replacement.get('team')
                
                player_in_id = registry.get(player_in)
                player_out_id = registry.get(player_out)
                
                if player_in_id:
                    session.run("""
                        MATCH (p:Player {player_id: $player_in_id})
                        MATCH (m:Match {match_id: $match_id})
                        MERGE (p)-[:IMPACT_SUB_IN {
                            match_id: $match_id,
                            replaced_player: $player_out,
                            reason: $reason,
                            team: $team,
                            over: $over_number,
                            delivery: $delivery_number
                        }]->(m)
                    """, player_in_id=player_in_id, match_id=match_id, 
                         player_out=player_out, reason=reason, team=team,
                         over_number=over_number, delivery_number=delivery_number)
                
                if player_out_id:
                    session.run("""
                        MATCH (p:Player {player_id: $player_out_id})
                        MATCH (m:Match {match_id: $match_id})
                        MERGE (p)-[:IMPACT_SUB_OUT {
                            match_id: $match_id,
                            replaced_by: $player_in,
                            reason: $reason,
                            team: $team,
                            over: $over_number,
                            delivery: $delivery_number
                        }]->(m)
                    """, player_out_id=player_out_id, match_id=match_id,
                         player_in=player_in, reason=reason, team=team,
                         over_number=over_number, delivery_number=delivery_number)
    
    def compute_and_store_aggregated_stats(self, session, match_id: str):
        """
        Compute aggregated batting and bowling statistics from ball-by-ball data.
        Creates BATTING_STATS and BOWLING_STATS relationships.
        """
        
        # Batting Statistics
        session.run("""
            MATCH (m:Match {match_id: $match_id})
            MATCH (d:Delivery {match_id: $match_id})-[:FACED_BY]->(p:Player)
            WITH m, p, 
                 SUM(d.runs_batter) as runs,
                 COUNT(d) as balls,
                 SUM(CASE WHEN d.runs_batter = 4 THEN 1 ELSE 0 END) as fours,
                 SUM(CASE WHEN d.runs_batter = 6 THEN 1 ELSE 0 END) as sixes,
                 SUM(CASE WHEN d.runs_batter = 0 AND d.runs_extras = 0 THEN 1 ELSE 0 END) as dots,
                 MAX(CASE WHEN d.is_wicket AND (d)-[:DISMISSED]->(p) THEN d.wicket_kind ELSE null END) as dismissal_type
            WHERE balls > 0
            MERGE (p)-[bs:BATTING_STATS]->(m)
            SET bs.runs = runs,
                bs.balls = balls,
                bs.fours = fours,
                bs.sixes = sixes,
                bs.dots = dots,
                bs.strike_rate = CASE WHEN balls > 0 THEN toFloat(runs) / balls * 100 ELSE 0 END,
                bs.dismissal_type = dismissal_type,
                bs.out = (dismissal_type IS NOT NULL)
        """, match_id=match_id)
        
        # Bowling Statistics
        session.run("""
            MATCH (m:Match {match_id: $match_id})
            MATCH (d:Delivery {match_id: $match_id})-[:BOWLED_BY]->(p:Player)
            WITH m, p,
                 COUNT(DISTINCT d.over_id) as overs_bowled,
                 COUNT(d) as balls,
                 SUM(d.runs_total) as runs_conceded,
                 SUM(CASE WHEN d.is_wicket THEN 1 ELSE 0 END) as wickets,
                 SUM(CASE WHEN d.runs_total = 0 THEN 1 ELSE 0 END) as dots,
                 SUM(CASE WHEN d.runs_batter = 4 THEN 1 ELSE 0 END) as fours_conceded,
                 SUM(CASE WHEN d.runs_batter = 6 THEN 1 ELSE 0 END) as sixes_conceded
            WHERE balls > 0
            MERGE (p)-[bw:BOWLING_STATS]->(m)
            SET bw.overs = toFloat(overs_bowled) + toFloat(balls % 6) / 10.0,
                bw.balls = balls,
                bw.runs_conceded = runs_conceded,
                bw.wickets = wickets,
                bw.economy = CASE WHEN balls > 0 THEN toFloat(runs_conceded) / balls * 6 ELSE 0 END,
                bw.dots = dots,
                bw.fours_conceded = fours_conceded,
                bw.sixes_conceded = sixes_conceded,
                bw.strike_rate = CASE WHEN wickets > 0 THEN toFloat(balls) / wickets ELSE null END
        """, match_id=match_id)
        
        logger.info(f"Computed aggregated stats for match {match_id}")
    
    def compute_and_store_partnership_stats(self, session, match_id: str):
        """
        Compute partnership statistics between batting pairs.
        Creates PARTNERSHIP relationships with runs, balls, and wicket_ended properties.
        """
        
        session.run("""
            MATCH (m:Match {match_id: $match_id})
            MATCH (d:Delivery {match_id: $match_id})-[:FACED_BY]->(batter:Player)
            MATCH (d)-[:NON_STRIKER]->(non_striker:Player)
            WITH m, batter, non_striker, d
            ORDER BY d.delivery_number
            WITH m, batter, non_striker,
                 COLLECT(d) as deliveries,
                 SUM(d.runs_total) as partnership_runs,
                 COUNT(d) as partnership_balls,
                 MAX(d.delivery_number) as last_delivery
            WHERE partnership_balls > 0
            WITH m, batter, non_striker, partnership_runs, partnership_balls, last_delivery,
                 deliveries[0].innings_id as innings_id,
                 CASE 
                   WHEN ANY(d IN deliveries WHERE d.is_wicket AND (d)-[:DISMISSED]->(batter)) THEN true 
                   ELSE false 
                 END as wicket_ended
            MERGE (batter)-[p:PARTNERSHIP {
                match_id: $match_id,
                innings_id: innings_id
            }]->(non_striker)
            SET p.runs = partnership_runs,
                p.balls = partnership_balls,
                p.wicket_ended = wicket_ended
        """, match_id=match_id)
        
        logger.info(f"Computed partnership stats for match {match_id}")
    
    def cleanup_database(self):
        """Delete all data from the database to ensure clean import."""
        with self.driver.session() as session:
            logger.info("Cleaning up existing data...")
            try:
                session.run("MATCH (n) DETACH DELETE (n)")
                logger.info("✓ Database cleaned successfully")
                sys.stdout.flush()
            except Exception as e:
                logger.warning(f"Failed to cleanup database: {str(e)}")
    
    def get_imported_match_ids(self) -> Set[str]:
        """Get the set of match IDs already imported in the database."""
        with self.driver.session() as session:
            result = session.run("MATCH (m:Match) RETURN m.match_id as match_id")
            return {record['match_id'] for record in result}
    
    def get_available_match_ids(self) -> Set[str]:
        """Get the set of match IDs available in JSON files."""
        json_files = self.get_sorted_json_files()
        return {f.stem for f in json_files}
    
    def get_missing_match_ids(self) -> tuple[List[Path], Set[str]]:
        """
        Get matches that need to be imported.
        
        Returns:
            Tuple of (sorted list of missing JSON files, set of missing match IDs)
        """
        imported_ids = self.get_imported_match_ids()
        available_files = {f: f.stem for f in self.get_sorted_json_files()}
        
        missing_files = [f for f, match_id in available_files.items() 
                        if match_id not in imported_ids]
        missing_ids = {match_id for match_id in available_files.values() 
                      if match_id not in imported_ids}
        
        return missing_files, missing_ids
    
    def get_partial_match_ids(self) -> List[str]:
        """
        Detect partially imported matches (Match node exists but incomplete data).
        
        A match is considered complete if it has:
        - At least 1 Innings created
        - Deliveries created for all its innings
        
        Returns:
            List of match IDs that are incomplete
        """
        with self.driver.session() as session:
            # Find matches where innings exist but have no deliveries (incomplete import)
            result = session.run("""
                MATCH (m:Match)
                OPTIONAL MATCH (i:Innings {match_id: m.match_id})
                WITH m, count(i) as innings_count, COLLECT(i.innings_id) as innings_ids
                WHERE innings_count > 0
                WITH m, innings_count, innings_ids
                OPTIONAL MATCH (d:Delivery {match_id: m.match_id})
                WITH m, innings_count, COUNT(d) as delivery_count
                WHERE delivery_count = 0
                RETURN m.match_id as match_id, innings_count
            """)
            
            partial_matches = []
            for record in result:
                match_id = record['match_id']
                innings_count = record['innings_count']
                partial_matches.append(match_id)
                logger.warning(f"Partial import detected: {match_id} (innings: {innings_count} created but 0 deliveries)")
            
            return partial_matches
    
    def delete_partial_matches(self, match_ids: List[str]):
        """Delete partially imported matches to allow re-import."""
        if not match_ids:
            return
        
        with self.driver.session() as session:
            for match_id in match_ids:
                try:
                    # Delete all deliveries for this match
                    session.run("""
                        MATCH (d:Delivery {match_id: $match_id})
                        DETACH DELETE d
                    """, match_id=match_id)
                    
                    # Delete all overs for this match
                    session.run("""
                        MATCH (o:Over {match_id: $match_id})
                        DETACH DELETE o
                    """, match_id=match_id)
                    
                    # Delete all innings for this match
                    session.run("""
                        MATCH (i:Innings {match_id: $match_id})
                        DETACH DELETE i
                    """, match_id=match_id)
                    
                    # Delete the match node itself
                    session.run("""
                        MATCH (m:Match {match_id: $match_id})
                        DETACH DELETE m
                    """, match_id=match_id)
                    
                    logger.info(f"Deleted partial import data for match {match_id}")
                except Exception as e:
                    logger.warning(f"Failed to delete partial data for {match_id}: {str(e)}")
    
    def compute_all_stats(self, session, match_ids: List[str]):
        """Compute and store stats for multiple matches."""
        for match_id in match_ids:
            try:
                self.compute_and_store_aggregated_stats(session, match_id)
                self.compute_and_store_partnership_stats(session, match_id)
            except Exception as e:
                logger.warning(f"Failed to compute stats for {match_id}: {str(e)}")
    
    def import_all_matches(self, batch_size: int = 10):
        """
        Import all matches in chronological order.
        Resumes from where it left off if partially imported.
        
        Args:
            batch_size: Number of matches to commit per transaction
        """
        # Check if any matches are already imported
        imported_ids = self.get_imported_match_ids()
        available_files = self.get_sorted_json_files()
        
        if imported_ids:
            # Resume mode: only import missing matches
            logger.info("=" * 80)
            logger.info(f"Found {len(imported_ids)} matches already imported in database")
            logger.info("=" * 80)
            
            # Check for partial imports (incomplete matches)
            logger.info("Checking for partial imports...")
            partial_matches = self.get_partial_match_ids()
            
            if partial_matches:
                logger.warning(f"\n⚠️  Found {len(partial_matches)} partially imported matches!")
                logger.info(f"Matches: {', '.join(partial_matches[:10])}{'...' if len(partial_matches) > 10 else ''}")
                logger.info("These will be deleted and re-imported...")
                self.delete_partial_matches(partial_matches)
                logger.info("✓ Partial imports cleaned up\n")
            
            missing_files, missing_ids = self.get_missing_match_ids()
            
            # Add partial matches back to the import list
            partial_files = [f for f in available_files if f.stem in partial_matches]
            json_files = sorted(missing_files + partial_files, key=lambda x: int(x.stem))
            
            total_files = len(json_files)
            
            if total_files == 0:
                logger.info("✓ All matches already imported! Database is complete.")
                sys.stdout.flush()
                
                # Still compute stats as they might be missing
                logger.info("\nVerifying aggregated statistics...")
                with self.driver.session() as session:
                    result = session.run("MATCH (m:Match) RETURN m.match_id as match_id")
                    match_ids = [record['match_id'] for record in result]
                
                # Check if stats are computed
                with self.driver.session() as session:
                    result = session.run("MATCH (p:Player)-[bs:BATTING_STATS]->(m:Match) RETURN COUNT(bs) as count")
                    stats_count = result.single()['count']
                    
                    if stats_count == 0:
                        logger.info("Stats not computed yet. Computing now...")
                        self.compute_all_stats(session, match_ids)
                    else:
                        logger.info(f"✓ Stats already computed: {stats_count} batting stats relationships found")
                
                return
            
            logger.info(f"Resuming import: {total_files} matches remaining")
            logger.info(f"Already imported: {', '.join(sorted(imported_ids)[:5])}...")
            
        else:
            # Fresh start: clean database
            logger.info("=" * 80)
            json_files = available_files
            total_files = len(json_files)
            
            logger.info(f"Starting import of {total_files} matches...")
            logger.info("=" * 80)
            self.cleanup_database()
            logger.info("=" * 80)
            
            # Clear skipped fields log
            if os.path.exists(self.skipped_fields_log):
                os.remove(self.skipped_fields_log)
        
        # Create constraints and indexes first
        logger.info("Creating constraints and indexes...")
        self.create_constraints_and_indexes()
        
        # Import matches
        imported_count = 0
        failed_count = 0
        
        # Open a single session for the entire import
        with self.driver.session() as session:
            for i, json_file in enumerate(json_files, 1):
                try:
                    with open(json_file, 'r') as f:
                        match_data = json.load(f)
                    
                    match_id = json_file.stem
                    
                    # Import the match
                    logger.info(f"[{i}/{total_files}] Importing match {match_id}...")
                    sys.stdout.flush()
                    
                    self.import_match(session, match_data, match_id)
                    logger.info(f"  ✓ Match {match_id} created")
                    sys.stdout.flush()
                    
                    # Log any skipped fields
                    self.log_skipped_fields(match_id, match_data)
                    
                    imported_count += 1
                    
                    if imported_count % 10 == 0:
                        logger.info(f"Progress: {imported_count}/{total_files} matches imported")
                        sys.stdout.flush()
                        
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to import {json_file.name}: {str(e)}")
                    # Log the error
                    with open("import_errors.log", 'a') as f:
                        f.write(f"{datetime.now().isoformat()} - {json_file.name}: {str(e)}\n")
        
        # Compute all stats after matches are imported
        logger.info("\nComputing aggregated statistics...")
        with self.driver.session() as session:
            # Get all match IDs for stats computation
            result = session.run("MATCH (m:Match) RETURN m.match_id as match_id")
            match_ids = [record['match_id'] for record in result]
            self.compute_all_stats(session, match_ids)
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Import completed!")
        logger.info(f"Successfully imported: {imported_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info(f"Skipped fields logged to: {self.skipped_fields_log}")
        logger.info(f"{'='*80}\n")
        
        # Print summary statistics
        self.print_import_summary()
    
    def print_import_summary(self):
        """Print summary statistics of imported data."""
        with self.driver.session() as session:
            # Count nodes
            result = session.run("""
                MATCH (m:Match) RETURN count(m) as matches
            """)
            matches = result.single()['matches']
            
            result = session.run("""
                MATCH (p:Player) RETURN count(p) as players
            """)
            players = result.single()['players']
            
            result = session.run("""
                MATCH (t:Team) RETURN count(t) as teams
            """)
            teams = result.single()['teams']
            
            result = session.run("""
                MATCH (d:Delivery) RETURN count(d) as deliveries
            """)
            deliveries = result.single()['deliveries']
            
            result = session.run("""
                MATCH (s:Season) RETURN count(s) as seasons
            """)
            seasons = result.single()['seasons']
            
            logger.info("\nDatabase Summary:")
            logger.info(f"  Seasons: {seasons}")
            logger.info(f"  Matches: {matches}")
            logger.info(f"  Teams: {teams}")
            logger.info(f"  Players: {players}")
            logger.info(f"  Deliveries (Balls): {deliveries}")


def main():
    """Main execution function with smart skipping and once-a-day check."""
    from datetime import date
    
    # Load configuration from .env file
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    JSON_FOLDER = os.getenv("JSON_FOLDER", "./data/ipl_json")
    
    # State check for smart skipping
    state_file = ".importer_state.json"
    today = date.today().isoformat()
    
    # Get current file count
    try:
        current_files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json")]
        current_count = len(current_files)
    except Exception as e:
        logger.error(f"Could not access JSON folder {JSON_FOLDER}: {e}")
        return

    # Check previous state
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
                last_run_date = state.get("last_run_date")
                last_file_count = state.get("last_file_count")
                
                # Rule 1: Don't run more than once a day
                if last_run_date == today:
                    logger.info(f"⏭️ Skipping: Importer already ran today ({today}).")
                    return
                
                # Rule 2: Only run if files were added
                if last_file_count == current_count:
                    logger.info(f"⏭️ Skipping: No new files added since last run (Count: {current_count}).")
                    return
        except Exception as e:
            logger.warning(f"⚠️ Could not read state file: {e}. Proceeding with check.")

    # Create importer instance
    importer = IPLNeo4jImporter(
        uri=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        json_folder=JSON_FOLDER
    )
    
    try:
        # Import all matches
        importer.import_all_matches(batch_size=10)
        
        # Save state after successful check/run
        with open(state_file, 'w') as f:
            json.dump({
                "last_run_date": today,
                "last_file_count": current_count
            }, f)
            
    except Exception as e:
        logger.error(f"❌ Importer failed: {e}")
    finally:
        # Always close the connection
        importer.close()
        logger.info("Neo4j connection closed.")


if __name__ == "__main__":
    main()