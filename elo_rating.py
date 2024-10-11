import pandas as pd
import math
import gspread

# Configuration
SHEET_NAME = "Klar Table Tennis Ranking"
WORKSHEET_NAME_MATCHES = "Games"
WORKSHEET_NAME_RANKINGS = "Ranking"
GOOGLE_CREDENTIALS_FILE = "google_cred.json"

# Constants for Elo calculation
K_MAX = 40
K_MIN = 20
INITIAL_RATING = 1000


# Function to calculate the dynamic K-factor based on the number of games
def calculate_k_factor(n_games):
    return K_MIN + (K_MAX - K_MIN) * (1 / (math.log(n_games + 1) + 1))


# Function to calculate the expected score
def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


# Function to update Elo ratings
def update_elo_rating(rating_a, rating_b, score_a, score_b, k_factor):
    expected_a = expected_score(rating_a, rating_b)
    expected_b = 1 - expected_a
    new_rating_a = rating_a + k_factor * (score_a - expected_a)
    new_rating_b = rating_b + k_factor * (score_b - expected_b)
    return new_rating_a, new_rating_b


# Get DataFrame from Google Sheets
def get_df_from_gsheet(sheet_name, worksheet_name):
    gc = gspread.service_account(filename=GOOGLE_CREDENTIALS_FILE)
    sh = gc.open(sheet_name)
    worksheet = sh.worksheet(worksheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    return df


# Write DataFrame to Google Sheets
def write_df_to_gsheet(sheet_name, df, worksheet_name):
    gc = gspread.service_account(filename=GOOGLE_CREDENTIALS_FILE)
    sh = gc.open(sheet_name)
    
    # Try to open the specified worksheet, or create it if it doesn't exist
    try:
        worksheet = sh.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=worksheet_name, rows=1, cols=1)

    # Clear the worksheet before updating
    worksheet.clear()

    # Update the worksheet with the DataFrame data
    rows_to_write = [df.columns.values.tolist()] + df.values.tolist()
    
    # Resize the worksheet to fit the DataFrame size
    worksheet.resize(rows=len(rows_to_write), cols=len(rows_to_write[0]))

    # Update the worksheet with the DataFrame data
    worksheet.update(rows_to_write)


# Main function to process the Elo ranking
def calculate_elo_ranking(df_matches):
    data = df_matches
    player_stats = {}

    for _, row in data.iterrows():
        player_1, player_2 = row["player_1"], row["player_2"]
        result_1, result_2 = row["player_1_result"], row["player_2_result"]
        game_date = row["game_date"]

        for player in [player_1, player_2]:
            if player not in player_stats:
                player_stats[player] = {
                    "Rating": INITIAL_RATING,
                    "Games Played": 0,
                    "Wins": 0,
                    "Losses": 0,
                    "Last Played Date": None,
                }

        k_1 = calculate_k_factor(player_stats[player_1]["Games Played"])
        k_2 = calculate_k_factor(player_stats[player_2]["Games Played"])
        k_combined = (k_1 + k_2) / 2

        new_rating_1, new_rating_2 = update_elo_rating(
            player_stats[player_1]["Rating"],
            player_stats[player_2]["Rating"],
            result_1,
            result_2,
            k_combined,
        )

        # Update player ratings and game count
        player_stats[player_1]["Rating"] = new_rating_1
        player_stats[player_2]["Rating"] = new_rating_2
        player_stats[player_1]["Games Played"] += 1
        player_stats[player_2]["Games Played"] += 1

        # Update wins and losses
        if result_1 == 1:
            player_stats[player_1]["Wins"] += 1
            player_stats[player_2]["Losses"] += 1
        else:
            player_stats[player_2]["Wins"] += 1
            player_stats[player_1]["Losses"] += 1

        # Update last played date
        player_stats[player_1]["Last Played Date"] = game_date
        player_stats[player_2]["Last Played Date"] = game_date

    # Calculate win rate
    for player, stats in player_stats.items():
        total_games = stats["Games Played"]
        stats["Win Rate"] = (
            (stats["Wins"] / total_games) * 100 if total_games > 0 else 0
        )

    # Convert the final stats to a DataFrame and round to two decimal places
    final_stats = pd.DataFrame.from_dict(player_stats, orient="index")
    final_stats = final_stats.sort_values(by="Rating", ascending=False)
    final_stats = final_stats[
        ["Rating", "Games Played", "Wins", "Losses", "Win Rate", "Last Played Date"]
    ]
    final_stats["Rating"] = final_stats["Rating"].round(2)
    final_stats["Win Rate"] = final_stats["Win Rate"].round(2)

    return final_stats


# Load the match data from Google Sheets
df_matches = get_df_from_gsheet(SHEET_NAME, WORKSHEET_NAME_MATCHES)

# Calculate the final Elo rankings
final_rankings = calculate_elo_ranking(df_matches)

# Save the final rankings to Google Sheets
final_rankings.reset_index(inplace=True)
final_rankings.rename(columns={"index": "Player"}, inplace=True)
write_df_to_gsheet(SHEET_NAME, final_rankings, WORKSHEET_NAME_RANKINGS)
