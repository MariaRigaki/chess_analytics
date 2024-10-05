import os
import chess.pgn
import pandas as pd
from eval_stats import calculate_mistakes_and_blunders
from time_analysis import get_time_stats


def parse_game_metadata(game):
    """
    Extracts metadata from a chess game in PGN format.

    Parameters:
    - game (chess.pgn.Game): A parsed chess game.

    Returns:
    A dictionary with game metadata like player names, result, time control, etc.
    """
    metadata = {
        "White": game.headers.get("White", "Unknown"),
        "Black": game.headers.get("Black", "Unknown"),
        "Result": game.headers.get("Result", "Unknown"),
        "Date": game.headers.get("Date", "Unknown"),
        "Event": game.headers.get("Event", "Unknown"),
        "Site": game.headers.get("Site", "Unknown"),
        "Round": game.headers.get("Round", "Unknown"),
        "WhiteElo": game.headers.get("WhiteElo", "Unknown"),
        "BlackElo": game.headers.get("BlackElo", "Unknown"),
        "TimeControl": game.headers.get(
            "TimeControl", "Unknown"
        ),  # Format is '600+5' (600 seconds with 5 sec increment)
        "Termination": game.headers.get("Termination", "Unknown"),
    }

    # Parse the time control to split base time and increment if available
    if metadata["TimeControl"] != "Unknown":
        time_parts = metadata["TimeControl"].split("+")
        if len(time_parts) == 2:
            metadata["BaseTime"] = int(time_parts[0])
            metadata["Increment"] = int(time_parts[1])
        else:
            metadata["BaseTime"] = int(time_parts[0])
            metadata["Increment"] = 0
    else:
        metadata["BaseTime"] = metadata["Increment"] = None

    evals = calculate_mistakes_and_blunders(game)
    # Add stats to metadata
    metadata["Blunders (White)"] = evals["blunders"]["white"]
    metadata["Blunders (Black)"] = evals["blunders"]["white"]
    metadata["Mistakes (White)"] = evals["mistakes"]["black"]
    metadata["Mistakes (Black)"] = evals["mistakes"]["black"]

    if metadata["BaseTime"] is not None:
        time_stats = get_time_stats(game, metadata["BaseTime"], metadata["Increment"])
    metadata["Avg Move Time (White)"] = time_stats["white"]["time_per_move"]
    metadata["Avg Move Time (Black)"] = time_stats["black"]["time_per_move"]

    return metadata


def parse_pgn_directory(directory):
    """
    Parses all PGN files in a given directory and extracts game statistics into a pandas DataFrame.

    Parameters:
    - directory (str): Path to the directory containing PGN files.

    Returns:
    A pandas DataFrame with metadata for each game.
    """
    game_data = []

    for filename in os.listdir(directory):
        if filename.endswith(".pgn"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as pgn_file:
                while True:
                    game = chess.pgn.read_game(pgn_file)
                    if game is None:
                        break

                    # Extract metadata and add to the list
                    game_metadata = parse_game_metadata(game)
                    game_data.append(game_metadata)

    # Create a DataFrame from the game data
    df = pd.DataFrame(game_data)
    return df


# Example usage
directory = "games"  # Replace with the path to your directory
df = parse_pgn_directory(directory)

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file for later use
df.to_csv("chess_games_statistics.csv", index=False)
