import chess.pgn
import re


# Function to extract time spent per move from PGN
def extract_move_times(game: chess.pgn.Game, increment: int):
    """
    Extracts move times from a PGN game and returns a list of times per move for each player.
    Assumes that the PGN has time stamps in the format [%clk hh:mm:ss]
    """
    move_times = {"white": [], "black": []}  # To store move times for both players
    clock_times = {"white": [], "black": []}

    # Traverse through all moves in the game
    node = game
    white_to_move = False  # Flag to track whose turn it is
    while node.variations:
        next_node = node.variation(0)
        comment = node.comment
        # print(white_to_move, comment)
        # Extract the time from the comments (if present)
        time_match = re.search(r"\[%clk (\d+):(\d+):(\d+)\]", comment)

        if time_match:
            hours, minutes, seconds = map(int, time_match.groups())
            clock_time = (
                hours * 3600 + minutes * 60 + seconds
            )  # Convert time to seconds

            if white_to_move:
                player = "white"
            else:
                player = "black"

            # print(player)
            if len(move_times[player]) > 0:
                time_diff = (
                    clock_times[player][-1] + increment - clock_time
                )  # add the increment
            else:
                time_diff = 0
            move_times[player].append(time_diff)
            clock_times[player].append(clock_time)

        white_to_move = not white_to_move  # Toggle turn
        node = next_node

    return move_times, clock_times


# Function to evaluate time usage
def get_time_stats(
    game: chess.pgn.Game, time_control_seconds: int, increment_seconds: int
) -> dict:
    """
    Evaluates whether a player used their time well:
    1. Checks if the player used at least half of their available time.
    2. Checks if the player ran out of time.
    """
    move_times, clock_times = extract_move_times(game, increment_seconds)
    # print(move_times, clock_times)
    total_time_used_white = sum(move_times["white"])
    total_time_used_black = sum(move_times["black"])

    num_moves_white = len(move_times["white"])
    num_moves_black = len(move_times["black"])

    # Check time usage for White
    white_time_stats = {
        "total_time_minutes": total_time_used_white / 60,
        "used_half_time": total_time_used_white >= time_control_seconds / 2,
        "ran_out_of_time": clock_times["white"][-1] <= increment_seconds,
        "time_per_move": total_time_used_white / num_moves_white,
    }

    # Check time usage for Black
    black_time_stats = {
        "total_time_minutes": total_time_used_black / 60,
        "used_half_time": total_time_used_black >= time_control_seconds / 2,
        "ran_out_of_time": clock_times["black"][-1] <= increment_seconds,
        "time_per_move": total_time_used_black / num_moves_black,
    }

    return {"white": white_time_stats, "black": black_time_stats}


if __name__ == "__main__":
    # pgn_file = open("games/game.pgn")
    pgn_file = open("games/game_analysis.pgn")
    game = chess.pgn.read_game(pgn_file)

    # Assume a time control of 30 + 30
    time_control_seconds = 30 * 60
    increment_seconds = 30

    # Evaluate time management
    time_management_evaluation = get_time_stats(
        game, time_control_seconds, increment_seconds
    )

    # Display the results
    print("White's Time Management:")
    print(
        f'\tUsed {time_management_evaluation["white"]["total_time_minutes"]:.2f} minutes in total'
    )
    print(
        "\tUsed at least half of the time:",
        time_management_evaluation["white"]["used_half_time"],
    )
    print("\tRan out of time:", time_management_evaluation["white"]["ran_out_of_time"])
    print(
        f'\tTime per move: {time_management_evaluation["white"]["time_per_move"]:.2f} seconds'
    )

    print("\nBlack's Time Management:")
    print(
        f'\tUsed {time_management_evaluation["black"]["total_time_minutes"]:.2f} minutes in total'
    )
    print(
        "\tUsed at least half of the time:",
        time_management_evaluation["black"]["used_half_time"],
    )
    print("\tRan out of time:", time_management_evaluation["black"]["ran_out_of_time"])
    print(
        f'\tTime per move: {time_management_evaluation["black"]["time_per_move"]:.2f} seconds'
    )
