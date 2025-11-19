from typing import Tuple
from .board import (
    Board,
    create_board,
    apply_move,
    print_board,
    get_winner,
    is_terminal,
)
from .config import MAX_PLAYER, MIN_PLAYER
from .agents import Agent, MinimaxAgent, ExpectimaxAgent, RandomAgent


def play_game(agent_max: Agent, agent_min: Agent, verbose: bool = False) -> str:
    """
    Juega una partida completa entre agent_max (MAX_PLAYER) y agent_min (MIN_PLAYER).
    Devuelve "O", "X" o "draw".
    """
    board: Board = create_board()
    current_player = MAX_PLAYER  # Empieza MAX por defecto

    if verbose:
        print("Nueva partida: MAX =", type(agent_max).__name__, "| MIN =", type(agent_min).__name__)
        print_board(board)

    while not is_terminal(board):
        if current_player == MAX_PLAYER:
            move = agent_max.get_move(board)
        else:
            move = agent_min.get_move(board)

        board = apply_move(board, move, current_player)

        if verbose:
            print(f"Jugador {current_player} juega columna {move}")
            print_board(board)

        current_player = MIN_PLAYER if current_player == MAX_PLAYER else MAX_PLAYER

    winner = get_winner(board)
    if winner is None:
        result = "draw"
    elif winner == MAX_PLAYER:
        result = MAX_PLAYER
    else:
        result = MIN_PLAYER

    if verbose:
        print("Resultado final:", result)
    return result


def run_experiments(num_games: int = 20) -> None:
    """
    Ejecuta algunos experimentos básicos:
    - Minimax vs Random
    - Expectimax vs Random
    """
    '''
    print("=== Experimento 1: Minimax (MAX) vs Random (MIN) ===")
    minimax_agent = MinimaxAgent(depth=4)
    random_agent = RandomAgent()

    wins = losses = draws = 0
    for _ in range(num_games):
        result = play_game(minimax_agent, random_agent, verbose=False)
        if result == MAX_PLAYER:
            wins += 1
        elif result == MIN_PLAYER:
            losses += 1
        else:
            draws += 1
    print(f"Minimax vs Random (MAX): {wins} victorias, {losses} derrotas, {draws} empates")

    print("\n=== Experimento 2: Expectimax (MAX) vs Random (MIN) ===")
    expectimax_agent = ExpectimaxAgent(depth=4)

    wins = losses = draws = 0
    for _ in range(num_games):
        result = play_game(expectimax_agent, random_agent, verbose=False)
        if result == MAX_PLAYER:
            wins += 1
        elif result == MIN_PLAYER:
            losses += 1
        else:
            draws += 1
    print(f"Expectimax vs Random (MAX): {wins} victorias, {losses} derrotas, {draws} empates")
    '''
    print("\n=== Experimento 3: Minimax (MAX) vs Expectimax (MIN) ===")
    minimax_agent = MinimaxAgent(depth=4)
    expectimax_agent = ExpectimaxAgent(depth=4)

    wins = losses = draws = 0
    for _ in range(num_games):
        result = play_game(minimax_agent, expectimax_agent, verbose=False)
        if result == MAX_PLAYER:
            wins += 1
        elif result == MIN_PLAYER:
            losses += 1
        else:
            draws += 1

    print(f"Minimax vs Expectimax (MAX vs MIN): {wins} victorias MAX, {losses} victorias MIN, {draws} empates")

    print("\n=== Experimento 4: Expectimax (MAX) vs Minimax (MIN) ===")
    expectimax_agent = ExpectimaxAgent(depth=4)
    minimax_agent = MinimaxAgent(depth=4)

    wins = losses = draws = 0
    for _ in range(num_games):
        result = play_game(expectimax_agent, minimax_agent, verbose=False)
        if result == MAX_PLAYER:
            wins += 1
        elif result == MIN_PLAYER:
            losses += 1
        else:
            draws += 1

    print(f"Expectimax vs Minimax (MAX vs MIN): {wins} victorias MAX, {losses} victorias MIN, {draws} empates")
    

if __name__ == "__main__":
    run_experiments(num_games=10)

