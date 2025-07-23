import random

class SudokuGame:
    def __init__(self, initial, solution):
        # Tablero inicial y solución (listas de listas)
        self.initial = [row[:] for row in initial]
        self.solution = [row[:] for row in solution]
        self.board = [row[:] for row in initial]  # Estado actual del tablero

    def is_valid_move(self, row, col, num):
        # Verifica si se puede poner 'num' en (row, col)
        if self.initial[row][col] != 0:
            return False
        if not (1 <= num <= 9):
            return False
        for i in range(9):
            if self.board[row][i] == num and i != col:
                return False
            if self.board[i][col] == num and i != row:
                return False
        start_row, start_col = 3*(row//3), 3*(col//3)
        for i in range(start_row, start_row+3):
            for j in range(start_col, start_col+3):
                if self.board[i][j] == num and (i, j) != (row, col):
                    return False
        return True

    def is_completed(self):
        # Verifica si el tablero está completo y correcto
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != self.solution[i][j]:
                    return False
        return True

    def get_random_hint(self):
        # Devuelve una celda vacía aleatoria y su valor correcto
        empty = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == 0]
        if not empty:
            return None
        i, j = random.choice(empty)
        return (i, j, self.solution[i][j])

"""
- fila: row
- columna: col / column
- tablero: board
- pista: hint
- solucion: solution
- inicial: initial
- vacía: empty
- numero: number
- completo: completed
"""