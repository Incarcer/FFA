# backend/models/data_models.py

from dataclasses import dataclass, field
from typing import List, Dict, Optional

# This Player dataclass is designed to hold consolidated player data
# from various sources (YFPY, NFL-Data-Py, static files)
# Its attributes are inspired by the "Player Model" in your KB.
@dataclass
class Player:
    player_id: str             # Corresponds to YFPY Player.player_id
    player_name: str           # Corresponds to YFPY Player.name.full
    position: str              # Corresponds to YFPY Player.display_position
    team_abbr: str             # Corresponds to YFPY Player.editorial_team_abbr (NFL team abbreviation)
    projected_points: float    # Could come from YFPY Player.player_points.total or nfl-data-py projections
    adp: int                   # Corresponds to YFPY Player.draft_analysis.average_draft_pick
    bye_week: int              # Corresponds to YFPY Player.bye_weeks.week
    tier: int = 0              # Custom: Player's tier for recommendation purposes
    vorp: float = 0.0          # Custom: Value Over Replacement Player

    def to_dict(self) -> Dict:
        """Converts the dataclass instance to a dictionary for serialization."""
        return self.__dict__

# This Team dataclass represents a fantasy team in your league.
# Its attributes are inspired by the "Team Model" in your KB.
@dataclass
class Team:
    team_id: str               # Corresponds to YFPY Team.team_id (though YFPY is int, our app uses string)
    team_name: str             # Corresponds to YFPY Team.name
    owner_name: str            # Corresponds to YFPY Manager.nickname
    roster: Dict[str, List[Player]] = field(default_factory=dict) # Roster by position, list of Player objects

    def add_player(self, player: Player):
        """Adds a player to the team's roster, organized by position."""
        if player.position not in self.roster:
            self.roster[player.position] = []
        self.roster[player.position].append(player)

    def to_dict(self) -> Dict:
        """Converts the Team instance to a dictionary, including nested Player objects."""
        return {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "owner_name": self.owner_name,
            "roster": {pos: [p.to_dict() for p in players] for pos, players in self.roster.items()}
        }

# This DraftPick dataclass represents a single pick made in the draft.
# Its attributes are inspired by the "DraftResult" model in your KB.
@dataclass
class DraftPick:
    pick_number: int           # Overall pick number (1-indexed)
    round: int                 # Corresponds to YFPY DraftResult.round
    round_pick: int            # Pick number within the current round
    team_id: str               # ID of the team making the pick
    player: Optional[Player] = None # The Player object drafted, if the pick has been made

    def to_dict(self) -> Dict:
        """Converts the DraftPick instance to a dictionary, including the nested Player object."""
        return {
            "pick_number": self.pick_number,
            "round": self.round,
            "round_pick": self.round_pick,
            "team_id": self.team_id,
            "player": self.player.to_dict() if self.player else None,
        }

