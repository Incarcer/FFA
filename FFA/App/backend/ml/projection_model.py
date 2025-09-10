"""
Advanced ML-based player projection model using XGBoost.
Integrates with existing VOR calculation and recommendation engine.
"""
import logging
import os
import pickle
from typing import Dict, Tuple, Optional
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error
from data.ngs_data_loader import load_ngs_data
from data.rankings_updater import update_all_rankings

LOGGER = logging.getLogger(__name__)

# Load config if available, otherwise use defaults
try:
    from config.model_config import HYPERPARAMETERS, DECAY_FACTOR, CONFIDENCE_INTERVAL
except ImportError:
    HYPERPARAMETERS = {
        'n_estimators': 250, 'learning_rate': 0.05, 'max_depth': 5,
        'subsample': 0.8, 'colsample_bytree': 0.8, 'random_state': 42, 'n_jobs': -1
    }
    DECAY_FACTOR = 0.9
    CONFIDENCE_INTERVAL = {'low': 0.10, 'median': 0.50, 'high': 0.90}

class PlayerProjectionModel:
    """ML-based player projection system for fantasy football."""
    
    def __init__(self, league_scoring: Dict[str, float]):
        """Initialize with league-specific scoring rules."""
        self.league_scoring = league_scoring
        self.models = {}  # Store models per position
        self.feature_columns = []
        self.cache_dir = "models/cache"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _calculate_fantasy_points(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert raw stats to fantasy points using league scoring."""
        df = df.copy()
        
        # Initialize fantasy points
        df['fantasy_points'] = 0.0
        
        # Passing (QB specific)
        df['fantasy_points'] += (df['passing_yards'] / 25) * self.league_scoring.get('pass_yards', 0.04)
        df['fantasy_points'] += df['passing_tds'] * self.league_scoring.get('pass_td', 4)
        df['fantasy_points'] += df['interceptions'] * self.league_scoring.get('interception', -2)
        
        # Rushing (all positions)
        df['fantasy_points'] += (df['rushing_yards'] / 10) * self.league_scoring.get('rush_yards', 0.1)
        df['fantasy_points'] += df['rushing_tds'] * self.league_scoring.get('rush_td', 6)
        
        # Receiving (all positions)
        df['fantasy_points'] += df['receptions'] * self.league_scoring.get('reception', 0.5)  # Half PPR
        df['fantasy_points'] += (df['receiving_yards'] / 10) * self.league_scoring.get('rec_yards', 0.1)
        df['fantasy_points'] += df['receiving_tds'] * self.league_scoring.get('rec_td', 6)
        
        # Penalties
        df['fantasy_points'] += df.get('fumbles_lost', 0) * self.league_scoring.get('fumble', -2)
        
        return df
    
    def _engineer_features(self, df: pd.DataFrame, rankings: Dict) -> pd.DataFrame:
        """Create predictive features from raw data."""
        df = df.copy()
        
        # Sort by player and season/week for rolling calculations
        df = df.sort_values(['player_id', 'season', 'week'])
        
        # Rolling averages (last 4 games)
        rolling_cols = ['carries', 'targets', 'rushing_yards', 'receiving_yards', 
                       'receptions', 'passing_yards', 'passing_tds', 'fantasy_points']
        
        for col in rolling_cols:
            if col in df.columns:
                df[f'{col}_rolling_4'] = df.groupby('player_id')[col].rolling(4, min_periods=1).mean().values
        
        # Season-level aggregations with decay
        season_stats = df.groupby(['player_id', 'season']).agg({
            'fantasy_points': 'mean',
            'targets': 'mean',
            'carries': 'mean',
            'receptions': 'sum',
            'receiving_yards': 'sum',
            'rushing_yards': 'sum'
        }).reset_index()
        
        # Apply decay factor to historical seasons
        current_season = df['season'].max()
        for season in season_stats['season'].unique():
            seasons_back = current_season - season
            decay_multiplier = DECAY_FACTOR ** seasons_back
            
            mask = season_stats['season'] == season
            for col in ['fantasy_points', 'targets', 'carries']:
                if f'{col}' in season_stats.columns:
                    season_stats.loc[mask, f'{col}_decayed'] = (
                        season_stats.loc[mask, col] * decay_multiplier
                    )
        
        # Merge seasonal data back
        df = df.merge(
            season_stats[['player_id', 'season', 'fantasy_points_decayed', 'targets_decayed']], 
            on=['player_id', 'season'], 
            how='left'
        )
        
        # Add external rankings
        if 'sos' in rankings and not rankings['sos'].empty:
            sos_map = dict(zip(rankings['sos']['Team'], rankings['sos']['SoS Rank']))
            df['sos_rank'] = df['team'].map(sos_map).fillna(16)  # Average rank if missing
        
        if 'oline' in rankings and not rankings['oline'].empty:
            oline_map = dict(zip(rankings['oline']['Team'], rankings['oline']['Tier']))
            df['oline_tier'] = df['team'].map(oline_map).fillna(3)  # Average tier if missing
        
        # Position-specific features
        if 'QB' in df['position'].values:
            df['qb_rushing_share'] = df['carries'] / (df.groupby(['team', 'season', 'week'])['carries'].transform('sum') + 1e-6)
        
        if any(pos in df['position'].values for pos in ['RB', 'WR', 'TE']):
            df['target_share'] = df['targets'] / (df.groupby(['team', 'season', 'week'])['targets'].transform('sum') + 1e-6)
            df['snap_weighted_usage'] = df.get('snap_pct', 0.5) * df.get('target_share', 0) * 100
        
        # Fill missing values
        df = df.fillna(df.median(numeric_only=True))
        
        return df
    
    def prepare_training_data(self) -> pd.DataFrame:
        """Load and prepare training data with features."""
        LOGGER.info("Loading NGS data for model training...")
        ngs_data = load_ngs_data()
        
        if ngs_data.empty:
            raise ValueError("No NGS data available for training")
        
        # Calculate fantasy points
        ngs_data = self._calculate_fantasy_points(ngs_data)
        
        # Load external rankings
        rankings = update_all_rankings()
        
        # Engineer features
        ngs_data = self._engineer_features(ngs_data, rankings)
        
        # Filter to regular season games (weeks 1-17)
        ngs_data = ngs_data[(ngs_data['week'] >= 1) & (ngs_data['week'] <= 17)]
        
        # Remove players with insufficient data
        player_game_counts = ngs_data.groupby('player_id').size()
        valid_players = player_game_counts[player_game_counts >= 8].index
        ngs_data = ngs_data[ngs_data['player_id'].isin(valid_players)]
        
        LOGGER.info(f"Training data prepared: {len(ngs_data)} player-games")
        return ngs_data
    
    def train_models(self, data: Optional[pd.DataFrame] = None) -> Dict[str, Dict]:
        """Train position-specific XGBoost models."""
        if data is None:
            data = self.prepare_training_data()
        
        results = {}
        
        # Define feature columns (exclude target and metadata)
        exclude_cols = ['player_id', 'player_display_name', 'team', 'season', 'week', 
                       'fantasy_points', 'position']
        self.feature_columns = [col for col in data.columns if col not in exclude_cols and data[col].dtype in [np.float64, np.int64]]
        
        # Train separate model for each position
        for position in ['QB', 'RB', 'WR', 'TE']:
            pos_data = data[data['position'] == position].copy()
            
            if len(pos_data) < 100:  # Minimum data requirement
                LOGGER.warning(f"Insufficient data for {position} model: {len(pos_data)} samples")
                continue
            
            LOGGER.info(f"Training {position} model with {len(pos_data)} samples...")
            
            # Prepare features and target
            X = pos_data[self.feature_columns].fillna(0)
            y = pos_data['fantasy_points']
            
            # Time series split for validation
            tscv = TimeSeriesSplit(n_splits=3)
            fold_scores = []
            
            for train_idx, val_idx in tscv.split(X):
                X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
                y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
                
                # Train model
                model = xgb.XGBRegressor(**HYPERPARAMETERS)
                model.fit(X_train, y_train)
                
                # Validate
                y_pred = model.predict(X_val)
                mae = mean_absolute_error(y_val, y_pred)
                fold_scores.append(mae)
            
            # Train final model on all data
            final_model = xgb.XGBRegressor(**HYPERPARAMETERS)
            final_model.fit(X, y)
            
            # Store model and metrics
            self.models[position] = final_model
            results[position] = {
                'model': final_model,
                'cv_mae': np.mean(fold_scores),
                'cv_std': np.std(fold_scores),
                'feature_importance': dict(zip(self.feature_columns, final_model.feature_importances_))
            }
            
            # Save model
            model_path = os.path.join(self.cache_dir, f'{position}_model.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(final_model, f)
            
            LOGGER.info(f"{position} model trained - CV MAE: {np.mean(fold_scores):.2f} ± {np.std(fold_scores):.2f}")
        
        return results
    
    def load_models(self) -> bool:
        """Load pre-trained models from cache."""
        try:
            for position in ['QB', 'RB', 'WR', 'TE']:
                model_path = os.path.join(self.cache_dir, f'{position}_model.pkl')
                if os.path.exists(model_path):
                    with open(model_path, 'rb') as f:
                        self.models[position] = pickle.load(f)
                    LOGGER.info(f"Loaded {position} model from cache")
                else:
                    return False
            return True
        except Exception as e:
            LOGGER.error(f"Error loading models: {e}")
            return False
    
    def predict_season_points(self, player_data: pd.DataFrame, risk_tolerance: str = 'balanced') -> pd.DataFrame:
        """Generate season point projections for players."""
        if not self.models:
            if not self.load_models():
                LOGGER.info("No cached models found, training new models...")
                self.train_models()
        
        # Prepare current season data
        rankings = update_all_rankings()
        player_data = self._engineer_features(player_data, rankings)
        
        projections = []
        
        for position in player_data['position'].unique():
            if position not in self.models:
                LOGGER.warning(f"No model available for position {position}")
                continue
            
            pos_data = player_data[player_data['position'] == position].copy()
            X = pos_data[self.feature_columns].fillna(0)
            
            # Generate predictions
            model = self.models[position]
            base_predictions = model.predict(X)
            
            # Add uncertainty bounds (simplified approach)
            # In production, use quantile regression for better uncertainty estimates
            prediction_std = np.std(base_predictions) * 0.3  # Approximate uncertainty
            
            if risk_tolerance == 'safe':
                final_predictions = base_predictions - prediction_std
            elif risk_tolerance == 'upside':
                final_predictions = base_predictions + prediction_std
            else:  # balanced
                final_predictions = base_predictions
            
            # Ensure non-negative predictions
            final_predictions = np.maximum(final_predictions, 0)
            
            # Scale to 17-game season (adjust if needed)
            final_predictions = final_predictions * 17
            
            pos_data['proj_points'] = final_predictions
            projections.append(pos_data)
        
        return pd.concat(projections, ignore_index=True) if projections else pd.DataFrame()

def get_league_scoring_config():
    """Extract scoring configuration from league settings."""
    # Based on your league settings provided
    return {
        'pass_yards': 0.04,    # 25 yards per point
        'pass_td': 4,
        'interception': -2,
        'rush_yards': 0.1,     # 10 yards per point
        'rush_td': 6,
        'reception': 0.5,      # Half PPR
        'rec_yards': 0.1,      # 10 yards per point
        'rec_td': 6,
        'fumble': -2
    }

# Integration function for your existing pipeline
def generate_player_projections(risk_tolerance: str = 'balanced') -> pd.DataFrame:
    """Main function to generate projections for integration with existing code."""
    scoring_config = get_league_scoring_config()
    model = PlayerProjectionModel(scoring_config)
    
    # Load current player data (you may need to adapt this)
    current_data = load_ngs_data()
    current_season_data = current_data[current_data['season'] == current_data['season'].max()]
    
    # Generate projections
    projections = model.predict_season_points(current_season_data, risk_tolerance)
    
    # Add required columns for VOR calculation
    required_cols = ['player_id', 'player_display_name', 'position', 'team', 'proj_points']
    for col in required_cols:
        if col not in projections.columns:
            if col == 'bye_week':
                projections[col] = np.random.randint(4, 15, len(projections))  # Random bye weeks for demo
            