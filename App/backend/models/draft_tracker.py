# backend/models/draft_tracker.py

from typing import List, Dict, Optional
import yaml
import os # Required for os.path.join

from backend.models.data_models import Player, Team, DraftPick

class DraftTracker:
    def __init__(self, config_path: str, teams_data: List[Dict], all_players: List[Player]):
        # Load league settings from YAML (see backend/config/league_settings.yaml)
        # Ensure the config_path is correctly relative to where the app runs, or absolute.
        # os.path.abspath is used for robustness.
        absolute_config_path = os.path.abspath(config_path)
        
        if not os.path.exists(absolute_config_path):
            raise FileNotFoundError(f"League settings file not found: {absolute_config_path}")

        with open(absolute_config_path, 'r') as f:
            config = yaml.safe_load(f)['draft_settings']
        
        self.total_rounds = config['total_rounds']
        self.total_teams = config['total_teams']
        self.draft_order_type = config['draft_order']
        self.roster_structure = config['roster_structure']

        # Initialize Team objects from provided data
        # YFPY's Team.team_id is int, but we use string for flexibility
        self.teams: Dict[str, Team] = {t['team_id']: Team(**t) for t in teams_data}
        
        # Keep track of available players by their ID for quick lookup and removal
        self.available_players: Dict[str, Player] = {p.player_id: p for p in all_players}
        
        self.draft_board: List[DraftPick] = []
        self.current_pick_index: int = 0 # 0-indexed to point to the next pick
        
        self._initialize_draft_board()

    def _initialize_draft_board(self):
        """
        Generates the full draft pick order based on league settings.
        Handles 'snake' draft order (e.g., Round 1: 1-10, Round 2: 10-1).
        """
        team_ids = list(self.teams.keys())
        pick_number = 1
        for round_num in range(1, self.total_rounds + 1):
            # Determine draft order for the current round
            current_round_order = team_ids
            if self.draft_order_type == 'snake' and round_num % 2 == 0:
                current_round_order = list(reversed(team_ids))

            for round_pick, team_id in enumerate(current_round_order, 1):
                self.draft_board.append(
                    DraftPick(
                        pick_number=pick_number,
                        round=round_num,
                        round_pick=round_pick,
                        team_id=team_id
                    )
                )
                pick_number += 1
        print(f"Draft board initialized with {len(self.draft_board)} picks.")

    def add_pick(self, player_id: str) -> Optional[DraftPick]:
        """
        Records a player selection, updates the draft state, and returns the completed pick.
        Removes the player from the available pool and adds them to the team's roster.
        """
        if self.current_pick_index >= len(self.draft_board):
            print("Error: Draft is already complete.")
            return None

        current_pick_obj = self.draft_board[self.current_pick_index]

        if player_id not in self.available_players:
            print(f"Error: Player with ID '{player_id}' is not available or has already been picked.")
            return None
            
        player = self.available_players.pop(player_id) # Remove player from available pool
        
        current_pick_obj.player = player # Assign player to the current pick
        
        team = self.teams[current_pick_obj.team_id]
        team.add_player(player) # Add player to the team's roster
        
        self.current_pick_index += 1 # Advance to the next pick

        print(f"Pick {current_pick_obj.pick_number}: Team {team.team_name} selects {player.player_name} ({player.position})")
        return current_pick_obj

    def get_current_state(self) -> Dict:
        """Returns a serializable dictionary of the entire draft state for the frontend."""
        return {
            "board": [pick.to_dict() for pick in self.draft_board],
            "teams": {team_id: team.to_dict() for team_id, team in self.teams.items()},
            "available_players": [p.to_dict() for p in self.available_players.values()],
            "current_pick_index": self.current_pick_index,
            "total_picks": len(self.draft_board),
            "current_pick_info": self.draft_board[self.current_pick_index].to_dict() if self.current_pick_index < len(self.draft_board) else None
        }

    def get_team_needs(self, team_id: str) -> Dict[str, int]:
        """
        Calculates the remaining positional needs for a given team based on roster structure.
        Considers starting positions and FLEX slots.
        """
        team = self.teams.get(team_id)
        if not team:
            print(f"Warning: Team with ID {team_id} not found.")
            return {}
        
        needs = self.roster_structure.copy()
        
        # Calculate actual needs for defined positions (QB, RB, WR, TE, DST, K)
        for pos, count_needed in needs.items():
            if pos == 'FLEX' or pos == 'BENCH':
                continue # Handle these separately
            
            num_at_pos = len(team.roster.get(pos, []))
            needs[pos] = max(0, count_needed - num_at_pos)

        # Handle FLEX spots: RB/WR/TE can fill FLEX
        # Count all current RB, WR, TE on the roster
        current_flex_candidates = (
            len(team.roster.get('RB', [])) +
            len(team.roster.get('WR', [])) +
            len(team.roster.get('TE', []))
        )
        
        # Calculate how many "starter" spots (non-FLEX RB/WR/TE) are filled
        required_starters = (
            self.roster_structure.get('RB', 0) +
            self.roster_structure.get('WR', 0) +
            self.roster_structure.get('TE', 0)
        )
        
        # Players filling FLEX are those in RB/WR/TE beyond the required starter spots
        flex_spots_filled = max(0, current_flex_candidates - required_starters)
        needs['FLEX'] = max(0, self.roster_structure.get('FLEX', 0) - flex_spots_filled)

        # Bench spots are just a total count
        needs['BENCH'] = max(0, self.roster_structure.get('BENCH', 0) - sum(len(p) for p in team.roster.values()))

        return needs

