"""
Definición de agentes que utilizan diferentes estrategias:
- MinimaxAgent
- ExpectimaxAgent
- RandomAgent
"""

import random
from abc import ABC, abstractmethod
from .board import Board, get_valid_moves
from .minimax_search import find_best_move_minimax
from .expectimax_search import find_best_move_expectimax
from .config import MAX_PLAYER, MIN_PLAYER


class Agent(ABC):
    @abstractmethod
    def get_move(self, board: Board) -> int:
        """Devuelve la columna elegida por el agente."""
        pass


class RandomAgent(Agent):
    def get_move(self, board: Board) -> int:
        moves = get_valid_moves(board)
        if not moves:
            raise ValueError("No hay movimientos válidos")
        return random.choice(moves)


class MinimaxAgent(Agent):
    def __init__(self, depth: int = 4):
        self.depth = depth

    def get_move(self, board: Board) -> int:
        return find_best_move_minimax(board, self.depth)


class ExpectimaxAgent(Agent):
    def __init__(self, depth: int = 4):
        self.depth = depth

    def get_move(self, board: Board) -> int:
        return find_best_move_expectimax(board, self.depth)

