# File: FFA/manual_auth.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root
project_dir = Path(__file__).parent
dotenv_path = project_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)

from yfpy.query import YahooFantasySportsQuery

print("Starting Yahoo Fantasy Sports API interactive authentication...")
print("Please ensure YAHOO_CONSUMER_KEY and YAHOO_CONSUMER_SECRET are set in your .env file.")

# These values are needed by the YFPy constructor but don't perform a query
# during the initial authentication phase.
# Using values from the YFPY example for NFL 2024.
test_game_id = 461
test_league_id = "274391"

try:
    query = YahooFantasySportsQuery(
        league_id=test_league_id,
        game_code="nfl",
        game_id=test_game_id,
        yahoo_consumer_key=os.environ.get("YAHOO_CONSUMER_KEY"),
        yahoo_consumer_secret=os.environ.get("YAHOO_CONSUMER_SECRET"),
        env_file_location=project_dir,
        save_token_data_to_env_file=True, # This instructs YFPy to save the token to .env
        browser_callback=True # Explicitly enable interactive browser authentication
    )
    print("\nAuthentication successful!")
    print("Your .env file should now be updated with 'YAHOO_ACCESS_TOKEN_JSON'.")
    print("You can now remove manual_auth.py and run 'docker compose up --build'.")

except Exception as e:
    print(f"\nAuthentication failed: {e}")
    print("Please check your consumer key/secret in .env and try again.")
    print("Ensure you enter the verifier code when prompted in the console after browser authentication.")
