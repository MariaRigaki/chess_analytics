import chess.pgn
import matplotlib.pyplot as plt


def calculate_mistakes_and_blunders(
    game, mistake_threshold=0.75, blunder_threshold=1.8
):
    """
    Parses the PGN data and calculates the number of mistakes and blunders for each player.

    Parameters:
    - pgn_data (str): PGN formatted chess game data.
    - mistake_threshold (float): The evaluation drop threshold to consider a mistake (in pawns).
    - blunder_threshold (float): The evaluation drop threshold to consider a blunder (in pawns).

    Returns:
    A dictionary containing the number of mistakes and blunders for both White and Black players.
    """
    # game = chess.pgn.read_game(pgn_data)

    if game is None:
        raise ValueError("No valid game found in PGN data")

    mistakes = {"white": 0, "black": 0}
    blunders = {"white": 0, "black": 0}

    node = game
    prev_eval = None
    white_to_move = False  # Flag to track whose turn it is

    while node.variations:
        next_node = node.variation(0)
        if white_to_move:
            current_player = "white"
        else:
            current_player = "black"

        # Check if there's an evaluation comment
        if "eval" in node.comment:
            # Extract the engine evaluation from the comment
            eval_start = node.comment.index("[%eval") + 7
            eval_end = node.comment.index("]", eval_start)
            eval_str = node.comment[eval_start:eval_end].strip()

            # This condition indicates an unavoidable checkmate
            # However, it is not always a blunder. It is a blunder only if the eval drop is significant
            if eval_str.startswith("#"):
                if int(eval_str[1:]) > 0:
                    eval_str = "100.0"
                else:
                    eval_str = "-100.0"

            try:
                current_eval = float(eval_str)
            except ValueError:
                # If evaluation parsing fails, skip this move
                node = next_node
                continue

            if prev_eval is not None:
                # Calculate the evaluation drop between moves
                eval_drop = abs(current_eval - prev_eval)

                if eval_drop >= blunder_threshold:
                    blunders[current_player] += 1
                elif eval_drop >= mistake_threshold:
                    mistakes[current_player] += 1

            prev_eval = current_eval

        # Alternate between White and Black players
        white_to_move = not white_to_move  # Toggle turn
        node = next_node

    return {"mistakes": mistakes, "blunders": blunders}


def extract_evaluation(comment):
    """
    Extracts the evaluation from the PGN comment, which may contain multiple fields like eval and clock.

    Parameters:
    - comment (str): The PGN comment containing the evaluation.

    Returns:
    - eval (float or None): The evaluation value in pawns if present, otherwise None.
    """
    if "[%eval" in comment:
        eval_start = comment.index("[%eval") + 7
        eval_end = comment.index("]", eval_start)
        eval_str = comment[eval_start:eval_end].strip()

        if eval_str.startswith("#"):
            # Checkmate in X moves
            if int(eval_str[1:]) > 0:
                return 5
            else:
                return -5

        try:
            return float(eval_str)
        except ValueError:
            pass

    return None


def extract_game_evaluations(game):
    """
    Parses the PGN data and extracts a list of evaluations for each move.

    Parameters:
    - pgn_data (str): PGN formatted chess game data.

    Returns:
    A list of evaluations where positive values indicate White's advantage and negative values indicate Black's advantage.
    """

    if game is None:
        raise ValueError("No valid game found in PGN data")

    evaluations = []
    node = game

    while node.variations:
        next_node = node.variation(0)

        # Extract the engine evaluation from the comment
        current_eval = extract_evaluation(node.comment)

        if current_eval is not None:
            evaluations.append(current_eval)

        node = next_node

    return evaluations


def plot_game_evaluation(evaluations):
    """
    Plots the game evaluation over time and fills the background with color based on which player has the advantage.

    Parameters:
    - evaluations (list of float): List of evaluations for each move where positive values indicate White's advantage and negative values indicate Black's advantage.
    """
    plt.figure(figsize=(10, 6))

    moves = list(range(1, len(evaluations) + 1))

    # Plot the evaluations
    plt.plot(moves, evaluations, color="blue", linewidth=2)

    # Fill the background with color based on who has the advantage
    plt.fill_between(
        moves,
        evaluations,
        0,
        where=[e > 0 for e in evaluations],
        color="gray",
        # alpha=0.3,
        label="White Advantage",
    )
    plt.fill_between(
        moves,
        evaluations,
        0,
        where=[e < 0 for e in evaluations],
        color="black",
        alpha=0.1,
        label="Black Advantage",
    )

    plt.fill_between(
        moves,
        evaluations,
        0,
        where=[True] * len(evaluations),
        color="black",
        alpha=0.1,
        interpolate=True,
    )
    plt.axhline(
        0, color="gray", linestyle="--"
    )  # Draw a horizontal line at 0 (equal position)
    plt.title("Game Evaluation Over Time")
    plt.xlabel("Move Number")
    plt.ylabel("Evaluation (Pawns)")
    plt.legend(loc="upper right")

    plt.show()


if __name__ == "__main__":
    # Example usage
    pgn_file = open("games/game_analysis.pgn")
    game = chess.pgn.read_game(pgn_file)
    stats = calculate_mistakes_and_blunders(game)
    print(stats)

    evaluations = extract_game_evaluations(game)
    plot_game_evaluation(evaluations)
