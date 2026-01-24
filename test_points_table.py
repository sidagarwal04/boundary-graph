#!/usr/bin/env python3
"""
Test script for the points table scraping functionality
Run this to verify the scraping works before launching the full app
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend_api import scrape_points_table

def test_points_table():
    """Test scraping for different seasons"""
    seasons_to_test = ["2025", "2026"]
    
    for season in seasons_to_test:
        print(f"\nTesting season {season}...")
        try:
            result = scrape_points_table(season)
            print(f"✅ Success! Found {len(result.teams)} teams")
            print(f"Season: {result.season}")
            print(f"Last updated: {result.last_updated}")
            print("\nTop 3 teams:")
            for i, team in enumerate(result.teams[:3]):
                print(f"  {team.position}. {team.team} - {team.points} pts (NRR: {team.nrr:+.3f})")
        except Exception as e:
            print(f"❌ Error for season {season}: {e}")

if __name__ == "__main__":
    test_points_table()