from .board import (
    Board,
    create_board,
    print_board,
    apply_move,
    get_winner,
    is_terminal,
    get_valid_moves,
)
from .config import MAX_PLAYER, MIN_PLAYER
from .agents import MinimaxAgent, ExpectimaxAgent


def human_turn(board: Board, human_symbol: str) -> Board:
    valid_moves = get_valid_moves(board)
    if not valid_moves:
        print("No hay movimientos disponibles.")
        return board

    while True:
        try:
            col = int(input(f"Tu turno ({human_symbol}). Elige columna {valid_moves}: "))
            if col in valid_moves:
                return apply_move(board, col, human_symbol)
            else:
                print(f"Columna inválida. Debes elegir entre {valid_moves}")
        except ValueError:
            print("Entrada inválida, por favor introduce un número.")


def choose_ai() -> str:
    print("Elige la IA oponente:")
    print("1) Minimax")
    print("2) Expectimax")
    choice = input("Opción [1/2]: ").strip()
    return choice or "1"


def main():
    ai_choice = choose_ai()
    symbol = input("Elige [O/X]: ").strip().upper()
    
    if symbol == "X":
        human_symbol = MIN_PLAYER
        ai_symbol = MAX_PLAYER
    else:
        human_symbol = MAX_PLAYER
        ai_symbol = MIN_PLAYER
    
    # Crear agente con el símbolo correcto
    if ai_choice == "2":
        ai_agent = ExpectimaxAgent(depth=4, player_symbol=ai_symbol) 
        print("Has elegido jugar contra Expectimax (profundidad 4).")
    else:
        ai_agent = MinimaxAgent(depth=4, player_symbol=ai_symbol) 
        print("Has elegido jugar contra Minimax (profundidad 4).")
    
    board = create_board()
    current_player = MAX_PLAYER

    print_board(board)

    while not is_terminal(board):
        if current_player == human_symbol:
            board = human_turn(board, human_symbol)
        else:
            # Turno de la IA    
            print(f"Turno de la IA ({ai_symbol})...")
            col = ai_agent.get_move(board)
            board = apply_move(board, col, ai_symbol)
            print(f"La IA jugó en la columna {col}.")

        print_board(board)
        current_player = MIN_PLAYER if current_player == MAX_PLAYER else MAX_PLAYER

    winner = get_winner(board)
    if winner is None:
        print("La partida terminó en empate.")
    elif winner == human_symbol:
        print("¡Has ganado!")
    else:
        print("Ha ganado la IA.")


if __name__ == "__main__":
    main()

