import customtkinter as ctk
from logic.game import SudokuGame
from data.score_manager import ScoreManager
from data.puzzles import PUZZLES
# import random

class SudokuApp:
    def __init__(self):
        # Configuración de la ventana principal
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("Sudoku")
        self.root.geometry("700x800")
        self.root.resizable(False, False)

        # Instancia de ScoreManager para manejar el puntaje
        self.score_manager = ScoreManager()
        self.selected_level = "easy"  # Nivel seleccionado por defecto
        self.selected_cell = None     # Celda seleccionada (fila, columna)
        self.sudoku_game = None       # Instancia de SudokuGame

        self.setup_ui()
        self.load_level(self.selected_level)

    def setup_ui(self):
        # Selector de nivel (fácil, medio, difícil)
        self.level_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.level_frame.pack(pady=(20, 10))
        ctk.CTkLabel(self.level_frame, text="Selecciona nivel:", font=("Arial", 16)).pack(side="left", padx=10)
        for level, color in zip(["easy", "medium", "hard"], ["#00ff00", "#FFD700", "#ff0000"]):
            btn = ctk.CTkButton(
                self.level_frame, text=level.capitalize(),
                fg_color=color, width=80,
                command=lambda l=level: self.load_level(l)
            )
            btn.pack(side="left", padx=10)

        # Marcador de puntaje por nivel
        self.score_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.score_frame.pack(pady=(0, 10))
        self.score_labels = {}
        for level, color in zip(["easy", "medium", "hard"], ["#00ff00", "#FFD700", "#ff0000"]):
            frame = ctk.CTkFrame(self.score_frame, width=120, height=60)
            frame.pack(side="left", padx=10)
            ctk.CTkLabel(frame, text=level.capitalize(), text_color=color, font=("Arial", 14)).pack()
            lbl = ctk.CTkLabel(frame, text=str(self.score_manager.scores[level]), font=("Arial", 22, "bold"), text_color=color)
            lbl.pack()
            self.score_labels[level] = lbl

        # Tablero Sudoku (9x9 botones)
        self.board_frame = ctk.CTkFrame(self.root)
        self.board_frame.pack(pady=20)
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                btn = ctk.CTkButton(
                    self.board_frame, text="", width=50, height=50,
                    font=("Arial", 20, "bold"),
                    command=lambda r=i, c=j: self.select_cell(r, c)
                )
                btn.grid(row=i, column=j, padx=(2 if j%3==0 else 0, 2 if j%3==2 else 0), pady=(2 if i%3==0 else 0, 2 if i%3==2 else 0))
                self.cells[i][j] = btn

        # Panel de números (botones 1-9 y borrar)
        self.numpad_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.numpad_frame.pack(pady=10)
        for n in range(1, 10):
            btn = ctk.CTkButton(
                self.numpad_frame, text=str(n), width=50, height=50,
                font=("Arial", 18, "bold"),
                command=lambda num=n: self.insert_number(num)
            )
            btn.pack(side="left", padx=5)
        # Botón borrar
        ctk.CTkButton(
            self.numpad_frame, text="Borrar", width=70, height=50,
            font=("Arial", 16), fg_color="#444",
            command=self.delete_number
        ).pack(side="left", padx=10)

        # Botón de pista
        self.hint_button = ctk.CTkButton(
            self.root, text="Pista", width=120, height=40,
            font=("Arial", 16), fg_color="#1F6AA5",
            command=self.give_hint
        )
        self.hint_button.pack(pady=10)

        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(self.root, text="", font=("Arial", 18))
        self.status_label.pack(pady=10)

        # Vincular teclado
        self.root.bind("<Key>", self.handle_keypress)

    def load_level(self, level):
        # Cargar el tablero y solución del nivel seleccionado
        self.selected_level = level
        puzzle = PUZZLES[level]
        self.sudoku_game = SudokuGame(puzzle["initial"], puzzle["solution"])
        self.selected_cell = None
        self.update_board()
        self.status_label.configure(text=f"Nivel: {level.capitalize()}", text_color="white")

    def update_board(self):
        # Actualiza la visualización del tablero
        sel_row, sel_col = self.selected_cell if self.selected_cell else (None, None)
        for i in range(9):
            for j in range(9):
                val = self.sudoku_game.board[i][j]
                is_initial = self.sudoku_game.initial[i][j] != 0
                btn = self.cells[i][j]
                # Sombreado de fila y columna
                if sel_row is not None and (i == sel_row or j == sel_col):
                    shade = "#2a3b4d"
                else:
                    shade = "#222" if is_initial else "#3B8ED0"
                btn.configure(
                    text=str(val) if val != 0 else "",
                    fg_color=shade,
                    text_color="#FFD700" if is_initial else "white"
                )
                btn.configure(state="disabled" if is_initial else "normal")
                # Resalta celda seleccionada
                if self.selected_cell == (i, j):
                    btn.configure(border_width=3, border_color="#FFD700")
                else:
                    btn.configure(border_width=1, border_color="#222")

    def select_cell(self, row, col):
        # Selecciona una celda si no es inicial
        if self.sudoku_game.initial[row][col] != 0:
            return
        self.selected_cell = (row, col)
        self.update_board()

    def insert_number(self, num):
        # Inserta un número en la celda seleccionada
        if not self.selected_cell:
            return
        row, col = self.selected_cell
        if self.sudoku_game.initial[row][col] != 0:
            return
        if self.sudoku_game.is_valid_move(row, col, num):
            self.sudoku_game.board[row][col] = num
            self.update_board()
            if self.sudoku_game.is_completed():
                self.status_label.configure(text="¡Ganaste ù.ú!", text_color="#00ff00")
                self.score_manager.scores[self.selected_level] += 1
                self.score_manager.save_score()
                self.score_labels[self.selected_level].configure(text=str(self.score_manager.scores[self.selected_level]))
        else:
            # Sombrea la celda en naranja si el número es incorrecto
            btn = self.cells[row][col]
            btn.configure(fg_color="#FFA500")  # Naranja
            self.status_label.configure(text="Movimiento inválido", text_color="#FFA500")
            self.root.after(1000, lambda: self.status_label.configure(text=f"Nivel: {self.selected_level.capitalize()}", text_color="white"))
            self.root.after(1000, self.update_board)
        self.update_board()

    def delete_number(self):
        # Borra el número de la celda seleccionada si no es inicial
        if not self.selected_cell:
            return
        row, col = self.selected_cell
        if self.sudoku_game.initial[row][col] == 0:
            self.sudoku_game.board[row][col] = 0
            self.update_board()

    def give_hint(self):
        # Da una pista aleatoria (rellena una celda vacía)
        hint = self.sudoku_game.get_random_hint()
        if hint:
            row, col, num = hint
            self.selected_cell = (row, col)
            self.sudoku_game.board[row][col] = num
            self.update_board()
            self.status_label.configure(text=f"Pista: ({row+1},{col+1}) = {num}", text_color="#00ff00")
            if self.sudoku_game.is_completed():
                self.status_label.configure(text="¡Ganaste ù.ú!", text_color="#00ff00")
                self.score_manager.scores[self.selected_level] += 1
                self.score_manager.save_score()
                self.score_labels[self.selected_level].configure(text=str(self.score_manager.scores[self.selected_level]))
        else:
            self.status_label.configure(text="No hay celdas vacías para pista", text_color="#FFD700")
        self.root.after(1500, lambda: self.status_label.configure(text=f"Nivel: {self.selected_level.capitalize()}", text_color="white"))

    def handle_keypress(self, event):
        # Permite mover la celda seleccionada con flechas y WASD, y poner números con el teclado
        if not self.selected_cell:
            return
        row, col = self.selected_cell
        if event.char and event.char in "123456789":
            self.insert_number(int(event.char))
        elif event.keysym in ("BackSpace", "Delete"):
            self.delete_number()
        elif event.keysym in ("Left", "a", "A"):
            if col > 0:
                self.selected_cell = (row, col - 1)
                self.update_board()
        elif event.keysym in ("Right", "d", "D"):
            if col < 8:
                self.selected_cell = (row, col + 1)
                self.update_board()
        elif event.keysym in ("Up", "w", "W"):
            if row > 0:
                self.selected_cell = (row - 1, col)
                self.update_board()
        elif event.keysym in ("Down", "s", "S"):
            if row < 8:
                self.selected_cell = (row + 1, col)
                self.update_board()

    def run(self):
        self.root.mainloop()

"""
- nivel: level
- facil: easy
- medio: medium
- dificil: hard
- celda: cell
- fila: row
- columna: col / column
- tablero: board
- pista: hint
- puntaje: score
- marcador: score board
- borrar: delete
- estado: status
- seleccionada: selected
- numero: number
- juego: game
"""