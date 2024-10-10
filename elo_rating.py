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
    expected_b = 1 - expected_a
    new_rating_a = rating_a + k_factor * (score_a - expected_a)
    new_rating_b = rating_b + k_factor * (score_b - expected_b)
    return new_rating_a, new_rating_b

# Main function to process the Elo ranking
def calculate_elo_ranking(file_path):
    data = pd.read_csv(file_path)
    player_stats = {}

    for _, row in data.iterrows():
        player_1, player_2 = row['player_1'], row['player_2']
        result_1, result_2 = row['player_1_result'], row['player_2_result']

        for player in [player_1, player_2]:
            if player not in player_stats:
                player_stats[player] = {
                    'Rating': INITIAL_RATING,
                    'Games Played': 0,
                    'Wins': 0,
                    'Losses': 0
                }

        k_1 = calculate_k_factor(player_stats[player_1]['Games Played'])
        k_2 = calculate_k_factor(player_stats[player_2]['Games Played'])
        k_combined = (k_1 + k_2) / 2

        new_rating_1, new_rating_2 = update_elo_rating(
            player_stats[player_1]['Rating'],
            player_stats[player_2]['Rating'],
            result_1,
            result_2,
            k_combined
        )

        # Update player ratings and game count
        player_stats[player_1]['Rating'] = new_rating_1
        player_stats[player_2]['Rating'] = new_rating_2
        player_stats[player_1]['Games Played'] += 1
        player_stats[player_2]['Games Played'] += 1

        # Update wins and losses
        if result_1 == 1:
            player_stats[player_1]['Wins'] += 1
            player_stats[player_2]['Losses'] += 1
        else:
            player_stats[player_2]['Wins'] += 1
            player_stats[player_1]['Losses'] += 1

    # Calculate win rate
    for player, stats in player_stats.items():
        total_games = stats['Games Played']
        stats['Win Rate'] = (stats['Wins'] / total_games) * 100 if total_games > 0 else 0

    # Convert the final stats to a DataFrame
    final_stats = pd.DataFrame.from_dict(player_stats, orient='index')
    final_stats = final_stats.sort_values(by='Rating', ascending=False)
    final_stats = final_stats[['Rating', 'Games Played', 'Wins', 'Losses', 'Win Rate']]
    return final_stats

# Example usage
file_path = 'input/ping_pong_matches.csv'  # Replace with the path to your input file
final_rankings = calculate_elo_ranking(file_path)

# Save the final rankings to a CSV file with the index as a "Player" column
final_rankings.reset_index(inplace=True)
final_rankings.rename(columns={'index': 'Player'}, inplace=True)
final_rankings.to_csv('output/ping_pong_ranking.csv', index=False)
