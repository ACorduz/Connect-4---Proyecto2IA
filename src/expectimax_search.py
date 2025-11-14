"""
Implementación de Expectimax para Connect-4.

Diferencia conceptual:
- En minimax, el oponente (MIN) elige siempre el peor caso para MAX.
- En expectimax, el oponente se modela como agente estocástico:
  elige sus movimientos posibles de forma aleatoria (distribución uniforme).
"""

from .config import MAX_PLAYER, MIN_PLAYER
from .board import Board, get_valid_moves, apply_move, is_terminal
from .evaluation import evaluate


def expectimax(board: Board, depth: int, maximizing: bool) -> float:
    """
    Expectimax recursivo.
    - Nodos MAX: eligen el máximo de los hijos.
    - Nodos "chance" (oponente): valor esperado (promedio) de los hijos.
    """
    val = evaluate(board)

    if depth == 0 or is_terminal(board):
        return val

    valid_moves = get_valid_moves(board)
    if not valid_moves:
        return val

    if maximizing:
        best_value = -float("inf")
        for col in valid_moves:
            child_board = apply_move(board, col, MAX_PLAYER)
            value = expectimax(child_board, depth - 1, False)
            best_value = max(best_value, value)
        return best_value
    else:
        # Nodo de "chance": oponente estocástico
        total_value = 0.0
        for col in valid_moves:
            child_board = apply_move(board, col, MIN_PLAYER)
            value = expectimax(child_board, depth - 1, True)
            total_value += value
        return total_value / len(valid_moves)


def find_best_move_expectimax(board: Board, depth: int) -> int:
    """
    Elige la mejor columna para MAX_PLAYER usando expectimax.
    """
    best_value = -float("inf")
    best_move = None

    for col in get_valid_moves(board):
        child_board = apply_move(board, col, MAX_PLAYER)
        move_value = expectimax(child_board, depth - 1, False)
        if move_value > best_value or best_move is None:
            best_value = move_value
            best_move = col

    if best_move is None:
        valid_moves = get_valid_moves(board)
        if not valid_moves:
            raise ValueError("No hay movimientos válidos")
        return valid_moves[0]

    return best_move

