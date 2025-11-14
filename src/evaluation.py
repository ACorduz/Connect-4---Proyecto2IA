"""
Funciones de evaluación heurística para Connect-4.

La idea es asignar una puntuación al tablero vista desde la perspectiva
del jugador MAX_PLAYER (IA).
"""

from .config import ROWS, COLS, EMPTY, MAX_PLAYER, MIN_PLAYER
from .board import Board, check_winner, is_full


def score_window(window, player: str) -> int:
    """
    Asigna una puntuación a una "ventana" de 4 celdas.
    Recompensa las formaciones del jugador y penaliza las del oponente.
    """
    opponent = MIN_PLAYER if player == MAX_PLAYER else MAX_PLAYER
    score = 0

    if window.count(player) == 4:
        score += 1000
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 5

    # Penalizar la posibilidad de que el oponente haga 4 en línea
    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 80

    return score


def heuristic_evaluation(board: Board, player: str) -> int:
    """
    Evalúa el tablero de forma heurística desde la perspectiva de 'player'.
    """
    score = 0

    # 1. Recompensar fichas en la columna central
    center_col_index = COLS // 2
    center_col = [board[row][center_col_index] for row in range(ROWS)]
    score += center_col.count(player) * 3

    # 2. Horizontales
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = board[row][col:col + 4]
            score += score_window(window, player)

    # 3. Verticales
    for col in range(COLS):
        col_array = [board[row][col] for row in range(ROWS)]
        for row in range(ROWS - 3):
            window = col_array[row:row + 4]
            score += score_window(window, player)

    # 4. Diagonales \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += score_window(window, player)

    # 5. Diagonales /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += score_window(window, player)

    return score


def evaluate(board: Board) -> float:
    """
    Función de evaluación general:
    - +inf si gana MAX_PLAYER.
    - -inf si gana MIN_PLAYER.
    - heurística si no es estado terminal.
    """
    if check_winner(board, MAX_PLAYER):
        return float("inf")
    if check_winner(board, MIN_PLAYER):
        return -float("inf")
    if is_full(board):
        return 0.0  # Empate
    return float(heuristic_evaluation(board, MAX_PLAYER))

