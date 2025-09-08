# backend/data_loader.py
import pandas as pd
# Assuming Player is a dataclass as defined in backend/models/data_models.py
from backend.models.data_models import Player
import os

def load_all_player_data():
    """
    Loads all static player data from JSON files and converts to Player objects.
    This function simulates loading data that would eventually come from various sources.
    It should align with the structure of your backend/data/flattened-players.json.

    Source: Uses concepts from "Player Model" in KB for player attributes.
    """
    players_data_path = os.path.join(os.path.dirname(__file__), 'data', 'flattened-players.json')
    
    
    # Check if the file exists before attempting to read
    if not os.path.exists(players_data_path):
        print(f"Warning: flattened-players.json not found at {players_data_path}. Returning empty list.")
        return []

    try:
        # Assuming flattened-players.json contains a list of player dictionaries
        players_df = pd.read_json(players_data_path)
    except Exception as e:
        print(f"Error reading or parsing flattened-players.json: {e}. Returning empty list.")
        return []

    # Map DataFrame rows to Player dataclass instances
    # Ensure all attributes for Player dataclass are present in the DataFrame or given defaults
    player_list = [
        Player(
            player_id=row['player_id'],
            player_name=row['name'] if 'name' in row else f"Player {row['player_id']}",
            position=row['display_position'],
            team_abbr=row['editorial_team_abbr'],
            # Provide sensible defaults or calculate these if not in JSON
            projected_points=row.get('projected_points', 0.0),
            adp=int(row.get('average_draft_pick', 999)), # From DraftAnalysis or Player Model
            bye_week=int(row.get('bye', 0)), # From ByeWeeks or Player Model
            tier=int(row.get('tier', 1)),
            vorp=row.get('player_points_value', 0.0) # From PlayerPoints or Player Model
        ) 
        for index, row in players_df.iterrows()
    ]
    
    print(f"Successfully loaded {len(player_list)} players from {players_data_path}.")
    return player_list

# If you have other data loading functions, they would also go here
def load_historical_data(player_id: str):
    """
    Simulates fetching historical data for a player.
    (This is a placeholder as nfl-data-py would handle this. See KB: NFLVerse pbp docs)
    """
    print(f"Loading historical data for player {player_id} (mock).")
    return pd.DataFrame() # Return empty DataFrame or mock data
