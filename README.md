# Ping Pong Elo Rating System

This project implements an Elo rating system for a ping pong league, where players are ranked based on their performance in individual matches. The system dynamically adjusts rating changes using a \( K \)-factor based on the number of games each player has played. Additionally, it supports reading match data from Google Sheets and writing the final rankings back to a Google Sheet.

## Basic Rules
- Each game is played as a standalone match (first to eleven points).
- Players either win or lose; draws are not considered.
- Ratings are updated after each game, with larger changes for surprising results.

## Key Features
- **Dynamic K-Factor**: Adjusts rating changes based on a player's experience (number of games played).
- **Elo Rating Calculation**: Predicts the expected outcome and updates ratings accordingly.
- **Tracking Metrics**: Calculates player ratings, games played, wins, losses, and win rate.
- **Google Sheets Integration**: Reads match data from a specified Google Sheet and writes the calculated rankings back to another sheet.

## Requirements
- Python 3.x
- `pandas` library
- `gspread` library
- Google Service Account credentials (`google_cred.json` file)

## Setup Instructions
1. **Google Service Account Setup**:
   - Create a Google Service Account and download the credentials JSON file (`google_cred.json`).
   - Share your Google Sheets document with the service account email (found in the credentials file).

2. **Dependencies**:
   - Install the required Python libraries:
     ```bash
     pip install pandas gspread
     ```

3. **Google Sheets Setup**:
   - Create a Google Sheets document with two sheets:
     - One for match data (e.g., "Games").
     - Another for the Elo rankings output (e.g., "Ranking").
   - Share the document with the Google Service Account email.

## Running the Code
1. **Load the Match Data from Google Sheets**:
   - Ensure that the match data sheet (e.g., "Games") has the following columns:
     ```
     game_date,player_1,player_2,player_1_result,player_2_result
     ```
     - `game_date`: Date of the match.
     - `player_1` and `player_2`: Names of the players.
     - `player_1_result` and `player_2_result`: Either 0 or 1, indicating the match outcome for each player.

2. **Run the Script**:
   - Execute the Python script to calculate the Elo ratings and update the Google Sheets document:
     ```bash
     python elo_rating.py
     ```

## Output Metrics
- **Rating**: The player's Elo rating.
- **Games Played**: Total number of games participated in.
- **Wins**: Number of games won.
- **Losses**: Number of games lost.
- **Win Rate**: Percentage of games won.
- **Last Played Date**: Date of the last recorded match for each player.

## More Information
For detailed documentation on the Ping Pong Elo Rating System, please refer to the `Ping Pong Elo Rating System.pdf` file.
