"""
Implementación de Minimax con poda Alfa-Beta para Connect-4.
"""

from .config import MAX_PLAYER, MIN_PLAYER
from .board import Board, get_valid_moves, apply_move, is_terminal
from .evaluation import evaluate


def minimax(board: Board, depth: int, alpha: float, beta: float, maximizing: bool, player: str) -> float:
    """
    Minimax con poda alfa-beta.
    Devuelve la puntuación estimada del tablero desde la perspectiva de 'player'.
    
    """
    # Evaluación del estado actual (desde perspectiva del jugador)
    val = evaluate(board)
    if player == MIN_PLAYER:  
        val = -val
    
    # Criterios de parada
    if depth == 0 or is_terminal(board):
        return val

    valid_moves = get_valid_moves(board)
    if not valid_moves:
        return val
    
    # Determinar quién es el oponente
    opponent = MIN_PLAYER if player == MAX_PLAYER else MAX_PLAYER  

    if maximizing:
        best_value = -float("inf")
        for col in valid_moves:
            child_board = apply_move(board, col, player)  #  Usar 'player' no MAX_PLAYER
            value = minimax(child_board, depth - 1, alpha, beta, False, player)  
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break  # poda
        return best_value
    else:
        best_value = float("inf")
        for col in valid_moves:
            child_board = apply_move(board, col, opponent)  # Usar 'opponent' no MIN_PLAYER
            value = minimax(child_board, depth - 1, alpha, beta, True, player)  
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if alpha >= beta:
                break  # poda
        return best_value


def find_best_move_minimax(board: Board, depth: int, player: str = MAX_PLAYER) -> int:
    """
    Elige la mejor columna para 'player' usando minimax.
    
    """
    best_value = -float("inf")
    best_move = None

    for col in get_valid_moves(board):
        child_board = apply_move(board, col, player)  # Usar 'player' no MAX_PLAYER
        move_value = minimax(child_board, depth - 1, -float("inf"), float("inf"), False, player) 
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