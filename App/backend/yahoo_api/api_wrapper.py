# backend/yahoo_api/api_wrapper.py

from typing import List, Optional
import os
from pathlib import Path

from yfpy.query import YahooFantasySportsQuery
from backend.models.data_models import Player, Team, DraftPick

class YahooApiWrapper:
    def __init__(self):
        # Source: "YFPY - Yahoo Fantasy Sports API Wrapper" and YFPY examples
        secrets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'secrets'))
        env_file_location = Path(secrets_dir)
        self.league_id = os.environ.get("YAHOO_LEAGUE_ID")
        self.game_code = os.environ.get("YAHOO_GAME_CODE", "nfl")
        self.game_id = int(os.environ.get("YAHOO_GAME_ID", "449"))  # Default to 2024 NFL

        if not self.league_id:
            raise ValueError("YAHOO_LEAGUE_ID environment variable is not set.")

        # Construct the query object
        self.query = YahooFantasySportsQuery(
            self.league_id,
            self.game_code,
            game_id=self.game_id,
            yahoo_consumer_key=os.environ.get("YAHOO_CONSUMER_KEY"),
            yahoo_consumer_secret=os.environ.get("YAHOO_CONSUMER_SECRET"),
            env_file_location=env_file_location,
            save_token_data_to_env_file=True,
        )
        # Construct league_key (source: get_game_key and get_league_id in your KB examples)
        self.league_key = f"{self.game_id}.l.{self.league_id}"

    def get_player_info(self, player_id: int) -> Optional[Player]:
        """Retrieve Player info for a given player_id using YFPY (source: get_player_stats_for_season in KB)."""
        player_key = f"{self.game_id}.p.{player_id}"
        # Use YFPY to get player stats
        yfpy_player = self.query.get_player_stats_for_season(player_key)
        if not yfpy_player: return None

        # Map to internal Player dataclass (see "Player Model" mapping)
        return Player(
            player_id=str(yfpy_player.player_id),
            player_name=getattr(yfpy_player, "full_name", yfpy_player.name if hasattr(yfpy_player,'name') else ""),
            position=getattr(yfpy_player, "display_position", ""),
            team_abbr=getattr(yfpy_player, "editorial_team_abbr", ""),
            projected_points=getattr(yfpy_player, "player_points_value", 0.0),
            adp=int(getattr(getattr(yfpy_player, "draft_analysis", None), "average_pick", 999) or 999),
            bye_week=getattr(getattr(yfpy_player, "bye_weeks", None), "week", 0),
            tier=0,
            vorp=getattr(yfpy_player, "player_points_value", 0.0)
        )

    def get_all_league_players(self, limit=100) -> List[Player]:
        """Retrieve all players in league, mapped to internal Player dataclass. Fast: uses paging."""
        yfpy_players = self.query.get_league_players(player_count_limit=limit, player_count_start=0)
        player_list = []
        for yfpy_player in yfpy_players:
            player_list.append(Player(
                player_id=str(getattr(yfpy_player, "player_id", "")),
                player_name=getattr(yfpy_player, "full_name", getattr(yfpy_player, "name", "")),
                position=getattr(yfpy_player, "display_position", ""),
                team_abbr=getattr(yfpy_player, "editorial_team_abbr", ""),
                projected_points=getattr(yfpy_player, "player_points_value", 0.0),
                adp=int(getattr(getattr(yfpy_player, "draft_analysis", None), "average_pick", 999) or 999),
                bye_week=getattr(getattr(yfpy_player, "bye_weeks", None), "week", 0),
                tier=0,
                vorp=getattr(yfpy_player, "player_points_value", 0.0)
            ))
        return player_list

    def get_league_draft_results(self) -> List[DraftPick]:
        """Retrieve all draft picks for the league."""
        results = self.query.get_league_draft_results()
        draft_picks = []
        for idx, pick in enumerate(results, 1):
            # Map to your internal DraftPick
            player_obj = self.get_player_info(getattr(pick, "player_id", 0))
            draft_picks.append(DraftPick(
                pick_number=idx,
                round=getattr(pick, "round", 0),
                round_pick=getattr(pick, "pick", 0),
                team_id=getattr(pick, "team_key", ""),
                player=player_obj
            ))
        return draft_picks

    def get_team_roster(self, team_id: int, week: int = None) -> List[Player]:
        """Retrieve the full roster for a given team and week (source: test_get_team_roster_player_stats_by_week in KB)."""
        # YFPY expects integer team_id for NFL
        yfpy_players = self.query.get_team_roster_player_stats_by_week(team_id, week) if week else self.query.get_team_roster_player_stats(team_id)
        player_list = []
        for yfpy_player in yfpy_players:
            player_list.append(Player(
                player_id=str(getattr(yfpy_player, "player_id", "")),
                player_name=getattr(yfpy_player, "full_name", getattr(yfpy_player, "name", "")),
                position=getattr(yfpy_player, "display_position", ""),
                team_abbr=getattr(yfpy_player, "editorial_team_abbr", ""),
                projected_points=getattr(yfpy_player, "player_points_value", 0.0),
                adp=int(getattr(getattr(yfpy_player, "draft_analysis", None), "average_pick", 999) or 999),
                bye_week=getattr(getattr(yfpy_player, "bye_weeks", None), "week", 0),
                tier=0,
                vorp=getattr(yfpy_player, "player_points_value", 0.0)
            ))
        return player_list
