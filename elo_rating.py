import pandas as pd
import math

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
    expected_b = 1 - expected_a  # The expected score for player B
    new_rating_a = rating_a + k_factor * (score_a - expected_a)
    new_rating_b = rating_b + k_factor * (score_b - expected_b)
    return new_rating_a, new_rating_b

# Main function to process the Elo ranking
def calculate_elo_ranking(file_path):
    # Read the input file
    data = pd.read_csv(file_path)

    # Dictionary to keep track of player ratings and number of games played
    player_ratings = {}
    player_games = {}

    # Process each game in the data
    for index, row in data.iterrows():
        player_1 = row['player_1']
        player_2 = row['player_2']
        result_1 = row['player_1_result']
        result_2 = row['player_2_result']

        # Initialize ratings and games if players are new
        if player_1 not in player_ratings:
            player_ratings[player_1] = INITIAL_RATING
            player_games[player_1] = 0
        if player_2 not in player_ratings:
            player_ratings[player_2] = INITIAL_RATING
            player_games[player_2] = 0

        # Calculate the K-factor for each player
        k_1 = calculate_k_factor(player_games[player_1])
        k_2 = calculate_k_factor(player_games[player_2])

        # Use the average K-factor for the game
        k_combined = (k_1 + k_2) / 2

        # Update the Elo ratings
        new_rating_1, new_rating_2 = update_elo_rating(
            player_ratings[player_1],
            player_ratings[player_2],
            result_1,
            result_2,
            k_combined
        )

        # Update player ratings and game count
        player_ratings[player_1] = new_rating_1
        player_ratings[player_2] = new_rating_2
        player_games[player_1] += 1
        player_games[player_2] += 1

    # Output the final Elo ratings for all players
    final_ratings = pd.DataFrame.from_dict(player_ratings, orient='index', columns=['Rating'])
    final_ratings = final_ratings.sort_values(by='Rating', ascending=False)
    return final_ratings

# Example usage
file_path = 'ping_pong_matches.csv'  # Replace with the path to your input file
final_rankings = calculate_elo_ranking(file_path)
print(final_rankings)
