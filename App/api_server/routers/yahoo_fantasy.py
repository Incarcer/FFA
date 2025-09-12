# api_server/routers/yahoo_fantasy.py
from fastapi import APIRouter, Depends, Query, Path as FastAPIPath
from typing import List, Dict, Any, Optional


# Import the API manager and settings
from backend.yahoo_api.api_wrapper import YahooFantasyAPI
from backend.config import get_settings, Settings


# Create a FastAPI APIRouter
# Source: APIRouter Class - FastAPI, 'Basic Usage Example'
router = APIRouter(
    prefix="/yahoo",
    tags=["Yahoo Fantasy Sports API"],
)


# Dependency to get an initialized YahooFantasyAPI instance
# Source: FastAPI Settings and Environment Variables, 'Using Settings as a Dependency'
async def get_yahoo_api_manager(settings: Settings = Depends(get_settings)) -> YahooFantasyAPI:
    return YahooFantasyAPI(settings)


# --- Game Related Endpoints ---


@router.get("/games/all", summary="Get all available Yahoo fantasy game keys")
async def get_all_game_keys(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> List[Dict]:
    """
    Retrieves a list of all available Yahoo fantasy game keys (sports and years).
    """
    return await api.get_all_yahoo_fantasy_game_keys()


@router.get("/games/key-by-season/{season}", summary="Get game key by season")
async def get_game_key_for_season(
    season: int = FastAPIPath(..., description="The fantasy season year (e.g., 2024)"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves the game key for a specific fantasy season.
    """
    return await api.get_game_key_by_season(season)


@router.get("/games/current-info", summary="Get current game info")
async def get_current_game_information(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> Dict:
    """
    Retrieves information about the current fantasy game based on the configured game ID.
    """
    return await api.get_current_game_info()


@router.get("/games/current-metadata", summary="Get current game metadata")
async def get_current_game_metadata_info(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> Dict:
    """
    Retrieves metadata about the current fantasy game based on the configured game ID.
    """
    return await api.get_current_game_metadata()


@router.get("/games/{game_id}/info", summary="Get game info by ID")
async def get_game_info_by_id(
    game_id: int = FastAPIPath(..., description="The Yahoo Game ID (e.g., 449 for NFL 2024)"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves detailed information for a specific Yahoo Game ID.
    """
    return await api.get_game_info_by_game_id(game_id)


@router.get("/games/{game_id}/metadata", summary="Get game metadata by ID")
async def get_game_metadata_by_id(
    game_id: int = FastAPIPath(..., description="The Yahoo Game ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves metadata for a specific Yahoo Game ID.
    """
    return await api.get_game_metadata_by_game_id(game_id)


@router.get("/games/{game_id}/weeks", summary="Get game weeks by ID")
async def get_game_weeks_by_id(
    game_id: int = FastAPIPath(..., description="The Yahoo Game ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> List[Dict]:
    """
    Retrieves all weeks defined for a specific Yahoo Game ID.
    """
    return await api.get_game_weeks_by_game_id(game_id)


@router.get("/games/{game_id}/stat-categories", summary="Get game stat categories by ID")
async def get_game_stat_categories_by_id(
    game_id: int = FastAPIPath(..., description="The Yahoo Game ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves statistical categories for a specific Yahoo Game ID.
    """
    return await api.get_game_stat_categories_by_game_id(game_id)


@router.get("/games/{game_id}/position-types", summary="Get game position types by ID")
async def get_game_position_types_by_id(
    game_id: int = FastAPIPath(..., description="The Yahoo Game ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves position types for a specific Yahoo Game ID.
    """
    return await api.get_game_position_types_by_game_id(game_id)


@router.get("/games/{game_id}/roster-positions", summary="Get game roster positions by ID")
async def get_game_roster_positions_by_id(
    game_id: int = FastAPIPath(..., description="The Yahoo Game ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves roster positions for a specific Yahoo Game ID.
    """
    return await api.get_game_roster_positions_by_game_id(game_id)


# --- User Related Endpoints ---


@router.get("/user/current", summary="Get current authenticated user info")
async def get_current_user_info(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> Dict:
    """
    Retrieves information about the currently authenticated Yahoo user.
    """
    return await api.get_current_user()


@router.get("/user/games", summary="Get user's games")
async def get_user_fantasy_games(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> List[Dict]:
    """
    Retrieves a list of all fantasy games the authenticated user participates in.
    """
    return await api.get_user_games()


@router.get("/user/leagues-by-game-key/{game_key}", summary="Get user's leagues by game key")
async def get_user_leagues_for_game_key(
    game_key: str = FastAPIPath(..., description="The game key (e.g., '449' for NFL 2024)"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> List[Dict]:
    """
    Retrieves a list of all leagues the authenticated user participates in for a specific game key.
    """
    return await api.get_user_leagues_by_game_key(game_key)


@router.get("/user/teams", summary="Get user's teams")
async def get_user_teams_info(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> List[Dict]:
    """
    Retrieves a list of all teams owned by the authenticated user across their leagues.
    """
    return await api.get_user_teams()


# --- League Related Endpoints ---


@router.get("/league/info", summary="Get current league info")
async def get_league_information(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> Dict:
    """
    Retrieves general information about the configured Yahoo Fantasy League.
    """
    return await api.get_league_info()


@router.get("/league/metadata", summary="Get current league metadata")
async def get_league_metadata_info(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> Dict:
    """
    Retrieves metadata about the configured Yahoo Fantasy League.
    """
    return await api.get_league_metadata()


@router.get("/league/settings", summary="Get current league settings")
async def get_league_settings_info(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> Dict:
    """
    Retrieves the settings for the configured Yahoo Fantasy League.
    """
    return await api.get_league_settings()


@router.get("/league/standings", summary="Get current league standings")
async def get_league_standings_info(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> List[Dict]:
    """
    Retrieves the current standings for all teams in the configured Yahoo Fantasy League.
    """
    return await api.get_league_standings()


@router.get("/league/teams", summary="Get all teams in current league")
async def get_league_teams_info(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> List[Dict]:
    """
    Retrieves a list of all teams participating in the configured Yahoo Fantasy League.
    """
    return await api.get_league_teams()


@router.get("/league/players", summary="Get all players in current league")
async def get_league_players_info(
    player_count_limit: Optional[int] = Query(None, description="Limit the number of players returned."),
    player_count_start: Optional[int] = Query(None, description="Start index for players (for pagination)."),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> List[Dict]:
    """
    Retrieves a list of all players in the configured Yahoo Fantasy League.
    Supports pagination via `player_count_limit` and `player_count_start`.
    """
    return await api.get_league_players(player_count_limit, player_count_start)


@router.get("/league/draft-results", summary="Get current league draft results")
async def get_league_draft_results_info(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> List[Dict]:
    """
    Retrieves the draft results for the configured Yahoo Fantasy League.
    """
    return await api.get_league_draft_results()


@router.get("/league/transactions", summary="Get current league transactions")
async def get_league_transactions_info(api: YahooFantasyAPI = Depends(get_yahoo_api_manager)) -> List[Dict]:
    """
    Retrieves a list of all transactions (adds, drops, trades) in the configured Yahoo Fantasy League.
    """
    return await api.get_league_transactions()


@router.get("/league/scoreboard/{week}", summary="Get league scoreboard by week")
async def get_league_scoreboard_by_week_data(
    week: int = FastAPIPath(..., description="The week number for the scoreboard (e.g., 1)"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves the scoreboard for a specific week in the configured Yahoo Fantasy League.
    """
    return await api.get_league_scoreboard_by_week(week)


@router.get("/league/matchups/{week}", summary="Get league matchups by week")
async def get_league_matchups_by_week_data(
    week: int = FastAPIPath(..., description="The week number for the matchups (e.g., 1)"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> List[Dict]:
    """
    Retrieves the matchups for a specific week in the configured Yahoo Fantasy League.
    """
    return await api.get_league_matchups_by_week(week)


# --- Team Related Endpoints ---


@router.get("/team/{team_id}/info", summary="Get team info by ID")
async def get_team_information(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves general information for a specific team in the configured league.
    """
    return await api.get_team_info(team_id)


@router.get("/team/{team_id}/metadata", summary="Get team metadata by ID")
async def get_team_metadata_info(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves metadata for a specific team in the configured league.
    """
    return await api.get_team_metadata(team_id)


@router.get("/team/{team_id}/stats", summary="Get team stats by ID")
async def get_team_statistics(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves overall statistics for a specific team in the configured league.
    """
    return await api.get_team_stats(team_id)


@router.get("/team/{team_id}/stats/week/{week}", summary="Get team stats by ID and week")
async def get_team_statistics_by_week(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    week: int = FastAPIPath(..., description="The week number"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves statistics for a specific team in the configured league for a given week.
    """
    return await api.get_team_stats_by_week(team_id, week)


@router.get("/team/{team_id}/standings", summary="Get team standings by ID")
async def get_team_standings_info(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves the standings information for a specific team in the configured league.
    """
    return await api.get_team_standings(team_id)


@router.get("/team/{team_id}/roster/week/{week}", summary="Get team roster by ID and week")
async def get_team_roster_by_week_data(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    week: int = FastAPIPath(..., description="The week number"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves the roster for a specific team in the configured league for a given week.
    """
    return await api.get_team_roster_by_week(team_id, week)


@router.get("/team/{team_id}/roster/player-info/week/{week}", summary="Get team roster player info by ID and week")
async def get_team_roster_player_info_by_week_data(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    week: int = FastAPIPath(..., description="The week number"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves detailed player information for the roster of a specific team and week.
    """
    return await api.get_team_roster_player_info_by_week(team_id, week)


@router.get("/team/{team_id}/roster/player-info/date/{date}", summary="Get team roster player info by ID and date (NHL/MLB/NBA)")
async def get_team_roster_player_info_by_date_data(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    date: str = FastAPIPath(..., description="The date in YYYY-MM-DD format (e.g., '2023-11-26')"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves detailed player information for the roster of a specific team and date.
    Primarily useful for daily fantasy sports like NHL, MLB, NBA.
    """
    return await api.get_team_roster_player_info_by_date(team_id, date)


@router.get("/team/{team_id}/roster/player-stats", summary="Get team roster player stats by ID")
async def get_team_roster_player_stats_data(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves overall player statistics for the roster of a specific team.
    """
    return await api.get_team_roster_player_stats(team_id)


@router.get("/team/{team_id}/roster/player-stats/week/{week}", summary="Get team roster player stats by ID and week")
async def get_team_roster_player_stats_by_week_data(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    week: int = FastAPIPath(..., description="The week number"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves player statistics for the roster of a specific team for a given week.
    """
    return await api.get_team_roster_player_stats_by_week(team_id, week)


@router.get("/team/{team_id}/draft-results", summary="Get team draft results by ID")
async def get_team_draft_results_data(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> List[Dict]:
    """
    Retrieves the draft results for a specific team in the configured league.
    """
    return await api.get_team_draft_results(team_id)


@router.get("/team/{team_id}/matchups", summary="Get team matchups by ID")
async def get_team_matchups_data(
    team_id: int = FastAPIPath(..., description="The Yahoo Fantasy Team ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> List[Dict]:
    """
    Retrieves the matchups for a specific team in the configured league.
    """
    return await api.get_team_matchups(team_id)


# --- Player Related Endpoints ---


@router.get("/player/{player_id}/stats/season", summary="Get player season stats by ID")
async def get_player_stats_for_season_data(
    player_id: int = FastAPIPath(..., description="The Yahoo Fantasy Player ID"),
    limit_to_league_stats: bool = Query(True, description="Limit stats to league context"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves season statistics for a specific player.
    """
    return await api.get_player_stats_for_season(player_id, limit_to_league_stats)


@router.get("/player/{player_id}/stats/week/{week}", summary="Get player week stats by ID and week")
async def get_player_stats_by_week_data(
    player_id: int = FastAPIPath(..., description="The Yahoo Fantasy Player ID"),
    week: int = FastAPIPath(..., description="The week number"),
    limit_to_league_stats: bool = Query(True, description="Limit stats to league context"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves player statistics for a specific week.
    """
    return await api.get_player_stats_by_week(player_id, week, limit_to_league_stats)


@router.get("/player/{player_id}/stats/date/{date}", summary="Get player date stats by ID and date (NHL/MLB/NBA)")
async def get_player_stats_by_date_data(
    player_id: int = FastAPIPath(..., description="The Yahoo Fantasy Player ID"),
    date: str = FastAPIPath(..., description="The date in YYYY-MM-DD format (e.g., '2023-11-26')"),
    limit_to_league_stats: bool = Query(True, description="Limit stats to league context"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves player statistics for a specific date.
    Primarily useful for daily fantasy sports like NHL, MLB, NBA.
    """
    return await api.get_player_stats_by_date(player_id, date, limit_to_league_stats)


@router.get("/player/{player_id}/ownership", summary="Get player ownership by ID")
async def get_player_ownership_data(
    player_id: int = FastAPIPath(..., description="The Yahoo Fantasy Player ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves ownership information for a specific player.
    """
    return await api.get_player_ownership(player_id)


@router.get("/player/{player_id}/percent-owned/week/{week}", summary="Get player percent owned by ID and week")
async def get_player_percent_owned_by_week_data(
    player_id: int = FastAPIPath(..., description="The Yahoo Fantasy Player ID"),
    week: int = FastAPIPath(..., description="The week number"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves the percentage of leagues a specific player is owned in for a given week.
    """
    return await api.get_player_percent_owned_by_week(player_id, week)


@router.get("/player/{player_id}/draft-analysis", summary="Get player draft analysis by ID")
async def get_player_draft_analysis_data(
    player_id: int = FastAPIPath(..., description="The Yahoo Fantasy Player ID"),
    api: YahooFantasyAPI = Depends(get_yahoo_api_manager)
) -> Dict:
    """
    Retrieves draft analysis for a specific player.
    """
    return await api.get_player_draft_analysis(player_id)


