import tkinter as tk
from tkinter import messagebox, ttk
from .board import (
    Board,
    create_board,
    apply_move,
    get_winner,
    is_terminal,
    get_valid_moves,
)
from .config import MAX_PLAYER, MIN_PLAYER, EMPTY, ROWS, COLS
from .agents import MinimaxAgent, ExpectimaxAgent


class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect-4 vs IA")
        self.root.resizable(False, False)
        
        # Colores
        self.COLOR_BOARD = "#0066CC"
        self.COLOR_EMPTY = "#FFFFFF"
        self.COLOR_PLAYER_O = "#FF4444"  # Rojo para O
        self.COLOR_PLAYER_X = "#FFFF44"  # Amarillo para X
        self.COLOR_HIGHLIGHT = "#00FF00"  # Verde para resaltar
        
        self.CELL_SIZE = 80
        self.CIRCLE_RADIUS = 30
        
        # Variables del juego
        self.board = None
        self.current_player = None
        self.human_symbol = None
        self.ai_symbol = None
        self.ai_agent = None
        self.game_over = False
        
        # Crear interfaz
        self.setup_menu()
        
    def setup_menu(self):
        """Pantalla inicial para configurar el juego."""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()
        
        # Título
        tk.Label(frame, text="Connect-4 vs IA", 
                font=("Arial", 24, "bold")).pack(pady=10)
        
        # Selección de IA
        tk.Label(frame, text="Elige el tipo de IA:", 
                font=("Arial", 14)).pack(pady=5)
        
        self.ai_choice = tk.StringVar(value="minimax")
        tk.Radiobutton(frame, text="Minimax (Oponente Perfecto)", 
                      variable=self.ai_choice, value="minimax",
                      font=("Arial", 12)).pack(anchor="w", padx=20)
        tk.Radiobutton(frame, text="Expectimax (Oponente Estocástico)", 
                      variable=self.ai_choice, value="expectimax",
                      font=("Arial", 12)).pack(anchor="w", padx=20)
        
        # Selección de profundidad
        tk.Label(frame, text="Nivel de dificultad:", 
                font=("Arial", 14)).pack(pady=5)
        
        self.depth_var = tk.IntVar(value=4)
        depth_frame = tk.Frame(frame)
        depth_frame.pack(pady=5)
        
        tk.Label(depth_frame, text="Fácil", font=("Arial", 10)).pack(side="left")
        tk.Scale(depth_frame, from_=2, to=6, orient="horizontal",
                variable=self.depth_var, length=200).pack(side="left", padx=10)
        tk.Label(depth_frame, text="Difícil", font=("Arial", 10)).pack(side="left")
        
        # Selección de símbolo
        tk.Label(frame, text="Elige tu símbolo:", 
                font=("Arial", 14)).pack(pady=5)
        
        self.symbol_choice = tk.StringVar(value="O")
        symbol_frame = tk.Frame(frame)
        symbol_frame.pack(pady=5)
        
        tk.Radiobutton(symbol_frame, text="O (Rojo - Empieza primero)", 
                      variable=self.symbol_choice, value="O",
                      font=("Arial", 12)).pack(anchor="w")
        tk.Radiobutton(symbol_frame, text="X (Amarillo - Empieza segundo)", 
                      variable=self.symbol_choice, value="X",
                      font=("Arial", 12)).pack(anchor="w")
        
        # Botón iniciar
        tk.Button(frame, text="Iniciar Juego", command=self.start_game,
                 font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                 padx=20, pady=10).pack(pady=20)
        
    def start_game(self):
        """Inicia una nueva partida con la configuración elegida."""
        # Configurar IA
        depth = self.depth_var.get()
        if self.ai_choice.get() == "expectimax":
            self.ai_agent = ExpectimaxAgent(depth=depth)
            ai_name = "Expectimax"
        else:
            self.ai_agent = MinimaxAgent(depth=depth)
            ai_name = "Minimax"
        
        # Configurar símbolos
        self.human_symbol = self.symbol_choice.get()
        if self.human_symbol == "O":
            self.ai_symbol = "X"
        else:
            self.ai_symbol = "O"
        
        # Inicializar juego
        self.board = create_board()
        self.current_player = MAX_PLAYER  # O siempre empieza
        self.game_over = False
        
        # Crear interfaz de juego
        self.setup_game_board()
        
        # Mostrar info
        info_text = f"Jugando contra {ai_name} (profundidad {depth})\n"
        info_text += f"Tú: {self.human_symbol} | IA: {self.ai_symbol}\n"
        info_text += f"Empieza: {self.current_player}"
        self.info_label.config(text=info_text)
        
        # Si la IA empieza, hacer su movimiento
        if self.current_player == self.ai_symbol:
            self.root.after(500, self.ai_move)
    
    def setup_game_board(self):
        """Crea la interfaz del tablero de juego."""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        # Panel superior con info y botones
        top_frame = tk.Frame(main_frame)
        top_frame.pack(pady=10)
        
        self.info_label = tk.Label(top_frame, text="", font=("Arial", 12))
        self.info_label.pack(side="left", padx=20)
        
        button_frame = tk.Frame(top_frame)
        button_frame.pack(side="right")
        
        tk.Button(button_frame, text="Nuevo Juego", command=self.setup_menu,
                 font=("Arial", 10), bg="#2196F3", fg="white",
                 padx=10, pady=5).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Salir", command=self.root.quit,
                 font=("Arial", 10), bg="#f44336", fg="white",
                 padx=10, pady=5).pack(side="left", padx=5)
        
        # Canvas para el tablero
        canvas_width = COLS * self.CELL_SIZE
        canvas_height = ROWS * self.CELL_SIZE
        
        self.canvas = tk.Canvas(main_frame, width=canvas_width, 
                               height=canvas_height, bg=self.COLOR_BOARD)
        self.canvas.pack()
        
        # Vincular clic del mouse
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        # Label de estado
        self.status_label = tk.Label(main_frame, text="", 
                                     font=("Arial", 14, "bold"))
        self.status_label.pack(pady=10)
        
        # Dibujar tablero inicial
        self.draw_board()
        self.update_status()
    
    def draw_board(self):
        """Dibuja el tablero y las fichas."""
        self.canvas.delete("all")
        
        # Dibujar casillas
        for row in range(ROWS):
            for col in range(COLS):
                x0 = col * self.CELL_SIZE
                y0 = row * self.CELL_SIZE
                x1 = x0 + self.CELL_SIZE
                y1 = y0 + self.CELL_SIZE
                
                # Rectángulo de fondo
                self.canvas.create_rectangle(x0, y0, x1, y1, 
                                            fill=self.COLOR_BOARD, outline="black")
                
                # Círculo para la ficha
                center_x = x0 + self.CELL_SIZE // 2
                center_y = y0 + self.CELL_SIZE // 2
                
                cell_value = self.board[row][col]
                if cell_value == EMPTY:
                    color = self.COLOR_EMPTY
                elif cell_value == "O":
                    color = self.COLOR_PLAYER_O
                else:  # X
                    color = self.COLOR_PLAYER_X
                
                self.canvas.create_oval(
                    center_x - self.CIRCLE_RADIUS,
                    center_y - self.CIRCLE_RADIUS,
                    center_x + self.CIRCLE_RADIUS,
                    center_y + self.CIRCLE_RADIUS,
                    fill=color, outline="black", width=2
                )
    
    def on_mouse_move(self, event):
        """Resalta la columna donde está el mouse."""
        if self.game_over or self.current_player != self.human_symbol:
            return
        
        col = event.x // self.CELL_SIZE
        if col < 0 or col >= COLS:
            return
        
        if col not in get_valid_moves(self.board):
            return
        
        # Resaltar columna válida
        x0 = col * self.CELL_SIZE
        y0 = 0
        x1 = x0 + self.CELL_SIZE
        y1 = ROWS * self.CELL_SIZE
        
        self.canvas.delete("highlight")
        self.canvas.create_rectangle(x0, y0, x1, y1, 
                                    outline=self.COLOR_HIGHLIGHT, 
                                    width=3, tags="highlight")
    
    def on_canvas_click(self, event):
        """Maneja el clic en el tablero."""
        if self.game_over:
            return
        
        if self.current_player != self.human_symbol:
            return
        
        # Determinar columna
        col = event.x // self.CELL_SIZE
        if col < 0 or col >= COLS:
            return
        
        # Verificar si es movimiento válido
        if col not in get_valid_moves(self.board):
            messagebox.showwarning("Movimiento Inválido", 
                                  "Esa columna está llena. Elige otra.")
            return
        
        # Aplicar movimiento
        self.make_move(col)
    
    def make_move(self, col):
        """Aplica un movimiento y actualiza el juego."""
        try:
            self.board = apply_move(self.board, col, self.current_player)
            self.draw_board()
            
            # Verificar si el juego terminó
            if self.check_game_over():
                return
            
            # Cambiar turno
            self.current_player = MIN_PLAYER if self.current_player == MAX_PLAYER else MAX_PLAYER
            self.update_status()
            
            # Si es turno de la IA, esperar un momento y mover
            if self.current_player == self.ai_symbol and not self.game_over:
                self.status_label.config(text="La IA está pensando...")
                self.root.update()
                self.root.after(500, self.ai_move)
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def ai_move(self):
        """La IA hace su movimiento."""
        if self.game_over:
            return
        
        try:
            col = self.ai_agent.get_move(self.board)
            self.make_move(col)
        except Exception as e:
            messagebox.showerror("Error de IA", f"Error en el movimiento de la IA: {e}")
    
    def check_game_over(self):
        """Verifica si el juego terminó y muestra mensaje."""
        if not is_terminal(self.board):
            return False
        
        self.game_over = True
        winner = get_winner(self.board)
        
        if winner is None:
            title = "Empate"
            message = "¡La partida terminó en empate!"
            self.status_label.config(text="EMPATE", fg="orange")
        elif winner == self.human_symbol:
            title = "¡Victoria!"
            message = "¡Felicidades! ¡Has ganado!"
            self.status_label.config(text="¡HAS GANADO!", fg="green")
        else:
            title = "Derrota"
            message = "La IA ha ganado. ¡Inténtalo de nuevo!"
            self.status_label.config(text="HA GANADO LA IA", fg="red")
        
        # Mostrar mensaje después de un breve delay
        self.root.after(500, lambda: messagebox.showinfo(title, message))
        return True
    
    def update_status(self):
        """Actualiza el label de estado."""
        if self.game_over:
            return
        
        if self.current_player == self.human_symbol:
            text = f"Tu turno ({self.human_symbol})"
            color = "blue"
        else:
            text = f"Turno de la IA ({self.ai_symbol})"
            color = "purple"
        
        self.status_label.config(text=text, fg=color)


def main():
    """Función principal para iniciar la GUI."""
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

