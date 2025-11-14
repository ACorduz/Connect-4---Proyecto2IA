"""
Lógica del juego Connect-4: representación del tablero, movimientos,
detección de ganador y estado terminal.
"""

from typing import List, Optional
from .config import ROWS, COLS, EMPTY, MAX_PLAYER, MIN_PLAYER

Board = List[List[str]]


def create_board() -> Board:
    """Crea un tablero vacío de ROWS x COLS."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def copy_board(board: Board) -> Board:
    """Devuelve una copia profunda del tablero."""
    return [row[:] for row in board]


def print_board(board: Board) -> None:
    """Imprime el tablero en consola (fila superior primero)."""
    print("\nTablero:")
    for row in board:
        print(" ".join(row))
    print(" ".join(map(str, range(COLS))))
    print()


def get_valid_moves(board: Board) -> List[int]:
    """Devuelve la lista de columnas en las que aún se puede jugar."""
    return [c for c in range(COLS) if board[0][c] == EMPTY]


def apply_move(board: Board, col: int, player: str) -> Board:
    """
    Devuelve un nuevo tablero tras dejar caer una ficha de 'player' en la columna 'col'.
    Lanza ValueError si la columna está llena.
    """
    new_board = copy_board(board)
    for row in range(ROWS - 1, -1, -1):
        if new_board[row][col] == EMPTY:
            new_board[row][col] = player
            return new_board
    raise ValueError(f"La columna {col} está llena")


def is_full(board: Board) -> bool:
    """Devuelve True si el tablero está lleno (no hay movimientos posibles)."""
    return all(board[0][c] != EMPTY for c in range(COLS))


def check_winner(board: Board, player: str) -> bool:
    """Comprueba si 'player' tiene 4 en línea (horizontal, vertical o diagonal)."""

    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False


def get_winner(board: Board) -> Optional[str]:
    """
    Devuelve MAX_PLAYER, MIN_PLAYER si alguno ganó,
    o None si no hay ganador.
    """
    if check_winner(board, MAX_PLAYER):
        return MAX_PLAYER
    if check_winner(board, MIN_PLAYER):
        return MIN_PLAYER
    return None


def is_terminal(board: Board) -> bool:
    """Devuelve True si la partida terminó (alguien ganó o tablero lleno)."""
    if get_winner(board) is not None:
        return True
    if is_full(board):
        return True
    return False

