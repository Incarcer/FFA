# api_server/services.py
import asyncio
import os
import yaml # To load league_settings.yaml
import pandas as pd
from pathlib import Path


# Import Python modules from sibling or child directories.
# Make sure backend/__init__.py and backend/models/__init__.py exist.
from backend.data_loader import load_all_player_data # This is the function we just added/corrected
from backend.models.data_models import Player, Team, DraftPick # Make sure these dataclasses exist in data_models.py
from backend.models.draft_tracker import DraftTracker
from backend.models.recommendation_engine import RecommendationEngine
from backend.yahoo_api.api_wrapper import YahooApiWrapper # Assuming this exists or is a placeholder


# --- In-Memory State and Singleton Instances ---
DRAFT_TRACKER = None
YAHOO_API = None
RECOMMENDATION_ENGINE = None
POLLING_TASK = None # For background polling if implemented


# Initial data loading for player list
ALL_PLAYERS_LIST = load_all_player_data()


# Mock Teams Data (ensure this matches your league_settings.yaml teams)
TEAMS_DATA = [{"team_id": f"T{i:02d}", "team_name": f"Team {i}", "owner_name": f"Owner {i}"} for i in range(1, 13)]


def initialize_draft_state():
    """
    Initializes or re-initializes the draft tracker, API wrapper, and recommendation engine.
    This function should be called once, e.g., on application startup or when a user
    selects their league.


    Source: Concept from your initial project overview manual, section "api_server/services.py".
    """
    global DRAFT_TRACKER, YAHOO_API, RECOMMENDATION_ENGINE


    # Define a default path relative to this file's location
    DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "backend" / "config" / "league_settings.yaml"
    # Get path from environment variable or use the default
    league_settings_path = os.environ.get("LEAGUE_SETTINGS_PATH", DEFAULT_CONFIG_PATH)


    if not os.path.exists(league_settings_path):
        print(f"Error: league_settings.yaml not found at {league_settings_path}")
        # Fallback to default or raise an error if configuration is critical
        raise FileNotFoundError(f"Configuration file not found: {league_settings_path}")
    
    with open(league_settings_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize DraftTracker
    DRAFT_TRACKER = DraftTracker(
        config_path=league_settings_path, # Pass the path directly if DraftTracker loads it
        teams_data=TEAMS_DATA,
        all_players=ALL_PLAYERS_LIST # Pass the loaded player list
    )


    # Initialize Yahoo API Wrapper (mock or real)
    # The YahooApiWrapper should be able to get player IDs from DRAFT_TRACKER.available_players
    player_ids_for_api = [p.player_id for p in DRAFT_TRACKER.available_players.values()]
    YAHOO_API = YahooApiWrapper(league_id=os.environ.get("YAHOO_LEAGUE_ID", "mock_league"), all_player_ids=player_ids_for_api)


    # Initialize Recommendation Engine
    # It needs a DataFrame of all players, which can be constructed from ALL_PLAYERS_LIST
    all_players_df = pd.DataFrame([p.to_dict() for p in ALL_PLAYERS_LIST])
    RECOMMENDATION_ENGINE = RecommendationEngine(all_players_df=all_players_df)


    print("Draft state initialized successfully.")


# Placeholder for background polling (if needed for real-time updates)
async def start_draft_polling():
    # This function would contain logic to poll the Yahoo API and update DRAFT_TRACKER
    # and broadcast updates via websockets.
    print("Starting draft polling (placeholder).")
    pass # Implement real polling logic here


# Utility for fetching player history (mock example)
def get_player_history(player_id: str):
    print(f"Fetching historical data for {player_id} (mock).")
    # In a real scenario, this might use nfl_data_integration.py
    return [{"week": 1, "points": 20}] # Mock data
