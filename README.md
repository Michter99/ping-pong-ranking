# Ping Pong Elo Rating System

This project implements an Elo rating system for a ping pong league, where players are ranked based on their performance in individual matches. The system dynamically adjusts rating changes using a \( K \)-factor based on the number of games each player has played.

## Basic Rules
- Each game is played as a standalone match (first to eleven points).
- Players either win or lose; draws are not considered.
- Ratings are updated after each game, with larger changes for surprising results.

## Key Features
- **Dynamic K-Factor**: Adjusts rating changes based on experience.
- **Elo Rating Calculation**: Predicts the expected outcome and updates ratings accordingly.
- **Tracking Metrics**: Calculates player ratings, games played, wins, losses, and win rate.

## Requirements
- Python 3.x
- `pandas` library

## Running the Code
1. Save match data in a CSV file, e.g., `ping_pong_matches.csv`:
    ```
    player_1,player_2,player_1_result,player_2_result
    Alice,Bob,1,0
    Charlie,Alice,0,1
    Bob,Charlie,1,0
    ```
    - Each row represents a game, and the results for `player_1_result` and `player_2_result` must be either 0 or 1, and must be opposite.
2. Run the script:
    ```bash
    python elo_rating.py
    ```

## Output Metrics
- **Rating**: The player's Elo rating.
- **Games Played**: Total number of games participated in.
- **Wins**: Number of games won.
- **Losses**: Number of games lost.
- **Win Rate**: Percentage of games won.

## More Information
For detailed documentation on the Ping Pong Elo Rating System, please refer to the `Ping Pong Elo Rating System.pdf` file.
