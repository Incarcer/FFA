import nfl_data_py as nfl
import pandas as pd

class NFLDataIntegration:
    """Wrapper for nfl-data-py library to fetch NFL data."""
    def __init__(self):
        pass

    def get_seasonal_player_stats(self, season: int = 2024) -> pd.DataFrame:
        """Fetches seasonal player statistics for a given year."""
        return nfl.import_seasonal_data(years=[season])

