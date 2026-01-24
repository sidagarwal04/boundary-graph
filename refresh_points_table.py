#!/usr/bin/env python3
"""
Auto-refresh script for IPL 2026 points table
This script should be run via cron job during the IPL season
to keep the points table data fresh

Add to crontab:
# Refresh every hour during IPL season (March-May)
0 * * 3-5 * /path/to/boundary-graph/refresh_points_table.py

# Or refresh every 4 hours
0 */4 * * * /path/to/boundary-graph/refresh_points_table.py
"""

import sys
import os
import requests
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('points_table_refresh.log'),
        logging.StreamHandler()
    ]
)

def refresh_points_table():
    """Refresh the points table by calling the API endpoint"""
    try:
        # Configure the API URL - adjust this based on your deployment
        api_url = os.getenv('API_URL', 'http://localhost:8000')
        
        # Call the API to refresh 2026 data
        response = requests.get(f"{api_url}/api/points-table/2026", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"✅ Successfully refreshed points table for 2026")
            logging.info(f"Found {len(data['teams'])} teams")
            
            # Log top 3 teams
            for i, team in enumerate(data['teams'][:3]):
                logging.info(f"  {team['position']}. {team['team']} - {team['points']} pts")
                
        else:
            logging.error(f"❌ Failed to refresh: HTTP {response.status_code}")
            
    except requests.RequestException as e:
        logging.error(f"❌ Network error during refresh: {e}")
    except Exception as e:
        logging.error(f"❌ Unexpected error during refresh: {e}")

def should_refresh():
    """Check if we should refresh based on current date/time"""
    now = datetime.now()
    
    # Only refresh during IPL season (March-June)
    if now.month not in [3, 4, 5, 6]:
        logging.info("Outside IPL season, skipping refresh")
        return False
    
    # Only refresh during reasonable hours (6 AM to 11 PM IST)
    # Assuming server runs in UTC, IST is UTC+5:30
    ist_hour = (now.hour + 5) % 24 + (1 if now.minute >= 30 else 0)
    
    if ist_hour < 6 or ist_hour > 23:
        logging.info("Outside active hours, skipping refresh")
        return False
    
    return True

if __name__ == "__main__":
    logging.info("Points table refresh job started")
    
    if should_refresh():
        refresh_points_table()
    else:
        logging.info("Refresh not needed at this time")
    
    logging.info("Points table refresh job completed")