# backend/models/recommendation_engine.py

from typing import List, Dict
import pandas as pd
from backend.models.draft_tracker import DraftTracker
from backend.models.data_models import Player # Used for type hinting

class RecommendationEngine:
    def __init__(self, all_players_df: pd.DataFrame):
        """
        Initializes the RecommendationEngine with a DataFrame of all known players.
        This DataFrame should contain enriched data (e.g., VORP, ADP, projections).
        """
        if not isinstance(all_players_df, pd.DataFrame):
            raise TypeError("all_players_df must be a pandas DataFrame.")
        if all_players_df.empty:
            print("Warning: Initializing RecommendationEngine with an empty player DataFrame.")
            
        self.all_players_df = all_players_df.set_index('player_id', drop=False) # Index by player_id for quick lookups

    def get_recommendations(
        self,
        draft_tracker: DraftTracker,
        team_id: str,
        num_recommendations: int = 5
    ) -> List[Dict]:
        """
        Generates player recommendations for the specified team based on current draft state.
        This simplified logic prioritizes:
        1. Positional need (from DraftTracker.get_team_needs)
        2. Player value (VORP, projected_points)
        3. Draft value (ADP vs. current pick)

        Source: Combines concepts from "Player Model" (VORP, ADP) and "Team Model" (needs)
        """
        team_needs = draft_tracker.get_team_needs(team_id)
        
        # Filter for players still available in the draft
        available_player_ids = list(draft_tracker.available_players.keys())
        if not available_player_ids:
            return [] # No players left

        available_df = self.all_players_df[self.all_players_df['player_id'].isin(available_player_ids)].copy()

        if available_df.empty:
            return []

        # Calculate a 'need factor' based on team's current roster needs
        def calculate_need_score(position: str) -> float:
            # High priority for empty starting spots
            if team_needs.get(position, 0) > 0 and position not in ['FLEX', 'BENCH']:
                return 2.0 # Higher boost for direct starters
            # Medium priority for FLEX-eligible players if FLEX spot is open
            if team_needs.get('FLEX', 0) > 0 and position in ['RB', 'WR', 'TE']:
                return 1.5
            # Basic value otherwise
            return 1.0

        available_df['need_score'] = available_df['position'].apply(calculate_need_score)

        # Calculate 'ADP value' (how much of a steal a player is)
        current_pick_number = draft_tracker.current_pick_index + 1
        # Players whose ADP is much earlier than current_pick_number are good value.
        # Higher positive value means a bigger "steal".
        available_df['adp_value'] = available_df['adp'] - current_pick_number
        
        # Combine scores into a final recommendation score
        # These weights (0.6, 0.3, 0.1) can be tuned to change recommendation strategy
        available_df['recommendation_score'] = (
            (available_df['vorp'] * 0.6) +                # Prioritize VORP
            (available_df['projected_points'] * 0.3) +    # Add projected points as a factor
            (available_df['adp_value'] * 0.1)             # Reward draft value
        ) * available_df['need_score'] # Apply positional need multiplier

        # Get top recommendations
        top_recs_df = available_df.sort_values('recommendation_score', ascending=False).head(num_recommendations)

        recommendations = []
        for _, row in top_recs_df.iterrows():
            # Retrieve the full Player object from the draft_tracker for detailed info
            player = draft_tracker.available_players.get(row['player_id'])
            if player:
                rec = {
                    "player": player.to_dict(),
                    "score": round(row['recommendation_score'], 2),
                    "reason": f"High VORP ({row['vorp']:.1f}), excellent ADP value ({row['adp_value']}), meets positional need."
                }
                recommendations.append(rec)
            
        return recommendations
