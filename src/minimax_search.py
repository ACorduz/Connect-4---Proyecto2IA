"""
Implementación de Minimax con poda Alfa-Beta para Connect-4.

Asume:
- MAX_PLAYER: la IA (quiere maximizar la evaluación).
- MIN_PLAYER: oponente ideal (quiere minimizar la evaluación).
"""

from .config import MAX_PLAYER, MIN_PLAYER
from .board import Board, get_valid_moves, apply_move, is_terminal
from .evaluation import evaluate


def minimax(board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
    """
    Minimax con poda alfa-beta.
    Devuelve la puntuación estimada del tablero.
    """
    # Evaluación del estado actual
    val = evaluate(board)

    # Criterios de parada
    if depth == 0 or is_terminal(board):
        return val

    valid_moves = get_valid_moves(board)
    if not valid_moves:
        return val

    if maximizing:
        best_value = -float("inf")
        for col in valid_moves:
            child_board = apply_move(board, col, MAX_PLAYER)
            value = minimax(child_board, depth - 1, alpha, beta, False)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break  # poda
        return best_value
    else:
        best_value = float("inf")
        for col in valid_moves:
            child_board = apply_move(board, col, MIN_PLAYER)
            value = minimax(child_board, depth - 1, alpha, beta, True)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if alpha >= beta:
                break  # poda
        return best_value


def find_best_move_minimax(board: Board, depth: int) -> int:
    """
    Elige la mejor columna para MAX_PLAYER usando minimax.
    """
    best_value = -float("inf")
    best_move = None

    for col in get_valid_moves(board):
        child_board = apply_move(board, col, MAX_PLAYER)
        move_value = minimax(child_board, depth - 1, -float("inf"), float("inf"), False)
        if move_value > best_value or best_move is None:
            best_value = move_value
            best_move = col

    # Por seguridad, si todo falla, devolvemos cualquier movimiento válido
    if best_move is None:
        valid_moves = get_valid_moves(board)
        if not valid_moves:
            raise ValueError("No hay movimientos válidos")
        return valid_moves[0]

    return best_move

