# backend/yahoo_api/api_wrapper.py
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from yfpy.query import YahooFantasySportsQuery
from yfpy.data import Data # For saving/loading data, as shown in YFPY demo
from fastapi import HTTPException, status


# Import settings from your new config file
from backend.config import Settings, get_settings


# Determine project root for YFPy token management (as in your v16. ... YFPY demo.py)
project_dir = Path(__file__).parent.parent.parent # Adjust based on your actual file structure
                                                   # If api_wrapper.py is in FFA/backend/yahoo_api,
                                                   # this points to FFA/


class YahooFantasyAPI:
    """
    Encapsulates YFPy query operations for Yahoo Fantasy Sports API.
    Initializes with league data from application settings.
    """
    def __init__(self, settings: Settings):
        # The game_id 449 is hardcoded in your v16. ... YFPY demo.py for NFL 2024.
        # This assumes your YAHOO_GAME_CODE 'nfl' from .env is for 2024 season.
        # If you change game_code in .env, you might need a more dynamic way to get game_id.
        self.game_id = 449


        try:
            self.query = YahooFantasySportsQuery(
                league_id=settings.YAHOO_LEAGUE_ID,
                game_code=settings.YAHOO_GAME_CODE,
                game_id=self.game_id,
                yahoo_consumer_key=settings.YAHOO_CONSUMER_KEY,
                yahoo_consumer_secret=settings.YAHOO_CONSUMER_SECRET,
                env_file_location=project_dir,
                save_token_data_to_env_file=True,
            )


            # Ensure access token data is saved/refreshed (as in your demo script)
            self.query.save_access_token_data_to_env_file(project_dir, save_json_to_var_only=True)
            self.query.league_key = f"{self.game_id}.l.{settings.YAHOO_LEAGUE_ID}"


            # Initialize YFPy Data manager (as in your demo script)
            self.data_manager = Data(project_dir / "yfpy_output_data")
            self.data_manager.data_dir.mkdir(parents=True, exist_ok=True)


            print(f"YahooFantasyAPI initialized for League ID: {settings.YAHOO_LEAGUE_ID}, Game Code: {settings.YAHOO_GAME_CODE}")


        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to initialize Yahoo Fantasy API: {e}"
            )


    # Helper to convert YFPy objects to dictionaries for API responses
    def _to_dict(self, obj: Any) -> Any:
        if hasattr(obj, 'to_dict') and callable(obj.to_dict):
            return obj.to_dict()
        elif isinstance(obj, list):
            return [self._to_dict(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            # Fallback for objects without a specific to_dict method
            return {k: self._to_dict(v) for k, v in obj.__dict__.items() if not k.startswith('_')}
        return obj


    # --- YFPy Query Methods (Comprehensive list from v16. ... YFPY demo.py) ---


    async def get_all_yahoo_fantasy_game_keys(self) -> List[Dict]:
        """Returns all available Yahoo fantasy game keys."""
        try:
            return self._to_dict(self.query.get_all_yahoo_fantasy_game_keys())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting game keys: {e}")


    async def get_game_key_by_season(self, season: int) -> Dict:
        """Returns game key for a specific season."""
        try:
            return self._to_dict(self.query.get_game_key_by_season(season))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting game key by season: {e}")


    async def get_current_game_info(self) -> Dict:
        """Returns current game info."""
        try:
            return self._to_dict(self.query.get_current_game_info())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting current game info: {e}")


    async def get_current_game_metadata(self) -> Dict:
        """Returns current game metadata."""
        try:
            return self._to_dict(self.query.get_current_game_metadata())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting current game metadata: {e}")


    async def get_game_info_by_game_id(self, game_id: int) -> Dict:
        """Returns game info for a specific game ID."""
        try:
            return self._to_dict(self.query.get_game_info_by_game_id(game_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting game info by ID: {e}")


    async def get_game_metadata_by_game_id(self, game_id: int) -> Dict:
        """Returns game metadata for a specific game ID."""
        try:
            return self._to_dict(self.query.get_game_metadata_by_game_id(game_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting game metadata by ID: {e}")


    async def get_game_weeks_by_game_id(self, game_id: int) -> List[Dict]:
        """Returns game weeks for a specific game ID."""
        try:
            return self._to_dict(self.query.get_game_weeks_by_game_id(game_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting game weeks by ID: {e}")


    async def get_game_stat_categories_by_game_id(self, game_id: int) -> Dict:
        """Returns game stat categories for a specific game ID."""
        try:
            return self._to_dict(self.query.get_game_stat_categories_by_game_id(game_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting game stat categories by ID: {e}")


    async def get_game_position_types_by_game_id(self, game_id: int) -> Dict:
        """Returns game position types for a specific game ID."""
        try:
            return self._to_dict(self.query.get_game_position_types_by_game_id(game_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting game position types by ID: {e}")


    async def get_game_roster_positions_by_game_id(self, game_id: int) -> Dict:
        """Returns game roster positions for a specific game ID."""
        try:
            return self._to_dict(self.query.get_game_roster_positions_by_game_id(game_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting game roster positions by ID: {e}")


    async def get_league_key(self, season: int) -> str:
        """Returns the league key for the current league and a specific season."""
        try:
            return self.query.get_league_key(season)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league key: {e}")


    async def get_current_user(self) -> Dict:
        """Returns info about the current authenticated user."""
        try:
            return self._to_dict(self.query.get_current_user())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting current user: {e}")


    async def get_user_games(self) -> List[Dict]:
        """Returns all games the user participates in."""
        try:
            return self._to_dict(self.query.get_user_games())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting user games: {e}")


    async def get_user_leagues_by_game_key(self, game_key: str) -> List[Dict]:
        """Returns all leagues for a user in a specific game."""
        try:
            return self._to_dict(self.query.get_user_leagues_by_game_key(game_key))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting user leagues by game key: {e}")


    async def get_user_teams(self) -> List[Dict]:
        """Returns all teams for the current user."""
        try:
            return self._to_dict(self.query.get_user_teams())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting user teams: {e}")


    async def get_league_info(self) -> Dict:
        """Returns general information about the current league."""
        try:
            return self._to_dict(self.query.get_league_info())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league info: {e}")


    async def get_league_metadata(self) -> Dict:
        """Returns metadata for the current league."""
        try:
            return self._to_dict(self.query.get_league_metadata())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league metadata: {e}")


    async def get_league_settings(self) -> Dict:
        """Returns settings for the current league."""
        try:
            return self._to_dict(self.query.get_league_settings())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league settings: {e}")


    async def get_league_standings(self) -> List[Dict]:
        """Returns standings for the current league."""
        try:
            return self._to_dict(self.query.get_league_standings())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league standings: {e}")


    async def get_league_teams(self) -> List[Dict]:
        """Returns all teams in the current league."""
        try:
            return self._to_dict(self.query.get_league_teams())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league teams: {e}")


    async def get_league_players(self, player_count_limit: Optional[int] = None, player_count_start: Optional[int] = None) -> List[Dict]:
        """Returns all players in the current league, with optional pagination."""
        try:
            return self._to_dict(self.query.get_league_players(
                player_count_limit=player_count_limit,
                player_count_start=player_count_start
            ))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league players: {e}")


    async def get_league_draft_results(self) -> List[Dict]:
        """Returns draft results for the current league."""
        try:
            return self._to_dict(self.query.get_league_draft_results())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league draft results: {e}")


    async def get_league_transactions(self) -> List[Dict]:
        """Returns transactions for the current league."""
        try:
            return self._to_dict(self.query.get_league_transactions())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league transactions: {e}")


    async def get_league_scoreboard_by_week(self, week: int) -> Dict:
        """Returns scoreboard data for a specific league week."""
        try:
            return self._to_dict(self.query.get_league_scoreboard_by_week(week))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league scoreboard by week: {e}")


    async def get_league_matchups_by_week(self, week: int) -> List[Dict]:
        """Returns matchups for a specific league week."""
        try:
            return self._to_dict(self.query.get_league_matchups_by_week(week))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting league matchups by week: {e}")


    async def get_team_info(self, team_id: int) -> Dict:
        """Returns general information about a specific team."""
        try:
            return self._to_dict(self.query.get_team_info(team_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team info: {e}")


    async def get_team_metadata(self, team_id: int) -> Dict:
        """Returns metadata for a specific team."""
        try:
            return self._to_dict(self.query.get_team_metadata(team_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team metadata: {e}")


    async def get_team_stats(self, team_id: int) -> Dict:
        """Returns overall stats for a specific team."""
        try:
            return self._to_dict(self.query.get_team_stats(team_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team stats: {e}")


    async def get_team_stats_by_week(self, team_id: int, week: int) -> Dict:
        """Returns stats for a specific team by week."""
        try:
            return self._to_dict(self.query.get_team_stats_by_week(team_id, week))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team stats by week: {e}")


    async def get_team_standings(self, team_id: int) -> Dict:
        """Returns standings for a specific team."""
        try:
            return self._to_dict(self.query.get_team_standings(team_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team standings: {e}")


    async def get_team_roster_by_week(self, team_id: int, week: int) -> Dict:
        """Returns roster for a specific team by week."""
        try:
            return self._to_dict(self.query.get_team_roster_by_week(team_id, week))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team roster by week: {e}")


    async def get_team_roster_player_info_by_week(self, team_id: int, week: int) -> Dict:
        """Returns player info in roster for a specific team by week."""
        try:
            return self._to_dict(self.query.get_team_roster_player_info_by_week(team_id, week))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team roster player info by week: {e}")


    async def get_team_roster_player_info_by_date(self, team_id: int, date: str) -> Dict:
        """Returns player info in roster for a specific team by date (NHL/MLB/NBA)."""
        try:
            return self._to_dict(self.query.get_team_roster_player_info_by_date(team_id, date))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team roster player info by date: {e}")


    async def get_team_roster_player_stats(self, team_id: int) -> Dict:
        """Returns overall player stats in roster for a specific team."""
        try:
            return self._to_dict(self.query.get_team_roster_player_stats(team_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team roster player stats: {e}")


    async def get_team_roster_player_stats_by_week(self, team_id: int, week: int) -> Dict:
        """Returns player stats in roster for a specific team by week."""
        try:
            return self._to_dict(self.query.get_team_roster_player_stats_by_week(team_id, week))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team roster player stats by week: {e}")


    async def get_team_draft_results(self, team_id: int) -> List[Dict]:
        """Returns draft results for a specific team."""
        try:
            return self._to_dict(self.query.get_team_draft_results(team_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team draft results: {e}")


    async def get_team_matchups(self, team_id: int) -> List[Dict]:
        """Returns matchups for a specific team."""
        try:
            return self._to_dict(self.query.get_team_matchups(team_id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting team matchups: {e}")


    # Player queries often use player_key: {game_id}.p.{player_id}
    # We will accept player_id and reconstruct player_key internally
    def _get_player_key(self, player_id: int) -> str:
        return f"{self.game_id}.p.{player_id}"


    async def get_player_stats_for_season(self, player_id: int, limit_to_league_stats: bool = True) -> Dict:
        """Returns season stats for a specific player."""
        player_key = self._get_player_key(player_id)
        try:
            return self._to_dict(self.query.get_player_stats_for_season(
                player_key, limit_to_league_stats=limit_to_league_stats
            ))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting player season stats: {e}")


    async def get_player_stats_by_week(self, player_id: int, week: int, limit_to_league_stats: bool = True) -> Dict:
        """Returns player stats for a specific week."""
        player_key = self._get_player_key(player_id)
        try:
            return self._to_dict(self.query.get_player_stats_by_week(
                player_key, week, limit_to_league_stats=limit_to_league_stats
            ))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting player week stats: {e}")


    async def get_player_stats_by_date(self, player_id: int, date: str, limit_to_league_stats: bool = True) -> Dict:
        """Returns player stats for a specific date (NHL/MLB/NBA)."""
        player_key = self._get_player_key(player_id)
        try:
            return self._to_dict(self.query.get_player_stats_by_date(
                player_key, date, limit_to_league_stats=limit_to_league_stats
            ))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting player date stats: {e}")


    async def get_player_ownership(self, player_id: int) -> Dict:
        """Returns ownership info for a specific player."""
        player_key = self._get_player_key(player_id)
        try:
            return self._to_dict(self.query.get_player_ownership(player_key))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting player ownership: {e}")


    async def get_player_percent_owned_by_week(self, player_id: int, week: int) -> Dict:
        """Returns percent owned info for a specific player by week."""
        player_key = self._get_player_key(player_id)
        try:
            return self._to_dict(self.query.get_player_percent_owned_by_week(player_key, week))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting player percent owned by week: {e}")


    async def get_player_draft_analysis(self, player_id: int) -> Dict:
        """Returns draft analysis for a specific player."""
        player_key = self._get_player_key(player_id)
        try:
            return self._to_dict(self.query.get_player_draft_analysis(player_key))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting player draft analysis: {e}")
