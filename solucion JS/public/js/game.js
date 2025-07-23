// Diccionario Español-Inglés:
// fila: row, columna: col, tablero: board, pista: hint, solucion: solution, inicial: initial, vacía: empty, numero: number, completo: completed

class SudokuGame {
  constructor(initial, solution) {
    this.initial = initial.map(row => row.slice());
    this.solution = solution.map(row => row.slice());
    this.board = initial.map(row => row.slice());
  }

  isValidMove(row, col, num) {
    if (this.initial[row][col] !== 0) return false;
    if (!(num >= 1 && num <= 9)) return false;
    for (let i = 0; i < 9; i++) {
      if (this.board[row][i] === num && i !== col) return false;
      if (this.board[i][col] === num && i !== row) return false;
    }
    let startRow = 3 * Math.floor(row / 3), startCol = 3 * Math.floor(col / 3);
    for (let i = startRow; i < startRow + 3; i++)
      for (let j = startCol; j < startCol + 3; j++)
        if (this.board[i][j] === num && (i !== row || j !== col)) return false;
    return true;
  }

  isCompleted() {
    for (let i = 0; i < 9; i++)
      for (let j = 0; j < 9; j++)
        if (this.board[i][j] !== this.solution[i][j]) return false;
    return true;
  }

  getRandomHint() {
    let empty = [];
    for (let i = 0; i < 9; i++)
      for (let j = 0; j < 9; j++)
        if (this.board[i][j] === 0) empty.push([i, j]);
    if (!empty.length) return null;
    let [i, j] = empty[Math.floor(Math.random() * empty.length)];
    return { row: i, col: j, num: this.solution[i][j] };
  }
}