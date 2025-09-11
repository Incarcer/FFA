# api_server/routers/player.py

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from backend.yahoo_api.api_wrapper import YahooApiWrapper
from backend.models.data_models import Player # For return type hinting/validation

router = APIRouter(prefix="/players", tags=["players"])

# Initialize the YahooApiWrapper here.
# It uses environment variables and previously obtained OAuth tokens.
yahoo_api = YahooApiWrapper()

@router.get("/{player_key}/info", response_model=Player) # Using response_model for Pydantic validation
async def get_player_full_info(player_key: str):
    """
    Retrieves full detailed information for a specific player by their Yahoo Player Key.
    Source: "Player Model" in KB, and yahoofantasy.League.players() method.
    """
    player_data = yahoo_api.get_player_info(player_key)
    if not player_data:
        raise HTTPException(status_code=404, detail=f"Player with key {player_key} not found.")
    return JSONResponse(player_data.to_dict())


@router.get("/{player_key}/stats")
async def get_player_seasonal_stats(player_key: str, season: int = Query(2024)):
    """
    Retrieves player's stats for a given season.
    Source: "test_get_player_stats_for_season" in "Integration Tests for Yahoo Fantasy Sports API Player Data"
    """
    # This would call a method in yahoo_api.py that gets player stats for a season
    # e.g., stats = yahoo_api.get_player_season_stats(player_key, season)
    
    # Placeholder/Mock Response:
    mock_stats = {
        "player_key": player_key,
        "season": season,
        "total_points": 250.5,
        "passing_yards": 4500,
        "passing_touchdowns": 30,
        "receiving_yards": 1200,
        "receiving_touchdowns": 10
    }
    return JSONResponse(mock_stats)

@router.get("/{player_key}/ownership")
async def get_player_ownership_details(player_key: str):
    """
    Retrieves detailed ownership information for a player.
    Source: "Player Model" in KB (ownership, percent_owned)
    """
    # This would call a method like yahoo_api.get_player_ownership(player_key)
    # Mock Response:
    mock_ownership = {
        "player_key": player_key,
        "percent_owned_value": 95.2,
        "owner_team_key": "449.l.12345.t.1" # Example team key
    }
    return JSONResponse(mock_ownership)

