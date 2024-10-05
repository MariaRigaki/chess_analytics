import chess.pgn


def is_middlegame(board):
    """
    Heuristic to detect if the game is in the middlegame phase.

    Criteria:
    - Both sides have moved some of their pieces (more than 10 half-moves).
    - Both sides still have their queens.
    - There are still a significant number of pieces on the board.
    """
    num_moves = board.fullmove_number
    num_pieces = len(board.piece_map())

    # Avoid detecting the middlegame too early (e.g., before move 10)
    if num_moves < 5:
        return False

    queens = board.pieces(chess.QUEEN, chess.WHITE) or board.pieces(
        chess.QUEEN, chess.BLACK
    )

    # Middlegame if queens are still on the board and there are more than 10 pieces
    return queens and num_pieces > 10


def is_endgame(board):
    """
    Heuristic to detect if the game is in the endgame phase.

    Criteria:
    - Queens are off the board or there are fewer than 10 total pieces.
    - Kings become more active and central.
    """
    num_pieces = len(board.piece_map())
    queens = not (
        board.pieces(chess.QUEEN, chess.WHITE) or board.pieces(chess.QUEEN, chess.BLACK)
    )

    # Check if kings are more centralized (e5, d5, e4, d4)
    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)

    white_king_centralized = white_king_square in [
        chess.D4,
        chess.E4,
        chess.D5,
        chess.E5,
    ]
    black_king_centralized = black_king_square in [
        chess.D4,
        chess.E4,
        chess.D5,
        chess.E5,
    ]

    king_activity = white_king_centralized or black_king_centralized

    # Endgame if queens are gone, few pieces remain, or kings are active
    return queens or num_pieces < 10 or king_activity


if __name__ == "__main__":

    # Example usage
    pgn_file = open("games/game_analysis.pgn")
    game = chess.pgn.read_game(pgn_file)
    board = game.board()

    middlegame_detected = False  # To avoid multiple detections
    # Play through the game and check for middlegame or endgame
    for move_number, move in enumerate(game.mainline_moves(), start=1):
        board.push(move)

        if not middlegame_detected and is_middlegame(board):
            print(f"Middlegame detected at move {move_number}")
            middlegame_detected = True  # To stop detecting further

        if is_endgame(board):
            print(f"Endgame detected at move {move_number}")
            break
