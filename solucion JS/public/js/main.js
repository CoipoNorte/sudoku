// Diccionario Español-Inglés:
// nivel: level, celda: cell, fila: row, columna: col, tablero: board, pista: hint, puntaje: score, borrar: delete, estado: status, seleccionada: selected, numero: number, juego: game

let game, currentLevel = 'easy', selectedCell = null, score = { easy: 0, medium: 0, hard: 0 };

function buildBoard() {
  const boardDiv = document.getElementById('board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < 9; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'd-flex';
    for (let j = 0; j < 9; j++) {
      const cell = document.createElement('input');
      cell.type = 'text';
      cell.maxLength = 1;
      cell.className = 'sudoku-cell';
      cell.id = `cell-${i}-${j}`;
      if (game.initial[i][j] !== 0) {
        cell.value = game.initial[i][j];
        cell.disabled = true;
        cell.classList.add('initial');
      } else {
        cell.value = game.board[i][j] !== 0 ? game.board[i][j] : '';
        cell.disabled = false;
        cell.onclick = () => selectCell(i, j);
        cell.onfocus = () => selectCell(i, j);
        cell.oninput = (e) => {
          let val = parseInt(e.target.value);
          if (isNaN(val) || val < 1 || val > 9) {
            e.target.value = '';
            return;
          }
          insertNumber(val);
        };
      }
      rowDiv.appendChild(cell);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function updateBoard() {
  for (let i = 0; i < 9; i++)
    for (let j = 0; j < 9; j++) {
      const cell = document.getElementById(`cell-${i}-${j}`);
      cell.classList.remove('selected', 'highlight', 'error');
      if (selectedCell && (i === selectedCell[0] || j === selectedCell[1]))
        cell.classList.add('highlight');
      if (selectedCell && i === selectedCell[0] && j === selectedCell[1])
        cell.classList.add('selected');
      if (game.initial[i][j] !== 0) {
        cell.classList.add('initial');
      } else {
        cell.classList.remove('initial');
        cell.value = game.board[i][j] !== 0 ? game.board[i][j] : '';
      }
    }
}

function selectCell(row, col) {
  if (game.initial[row][col] !== 0) return;
  selectedCell = [row, col];
  updateBoard();
}

function insertNumber(num) {
  if (!selectedCell) return;
  const [row, col] = selectedCell;
  if (game.initial[row][col] !== 0) return;
  if (game.isValidMove(row, col, num)) {
    game.board[row][col] = num;
    updateBoard();
    setStatus('');
    if (game.isCompleted()) {
      setStatus('¡Ganaste ù.ú!', 'success');
      score[currentLevel]++;
      saveScore();
      updateScoreboard();
    }
  } else {
    const cell = document.getElementById(`cell-${row}-${col}`);
    cell.classList.add('error');
    setStatus('Movimiento inválido', 'warning');
    setTimeout(() => {
      cell.classList.remove('error');
      setStatus('');
    }, 1000);
  }
}

function deleteNumber() {
  if (!selectedCell) return;
  const [row, col] = selectedCell;
  if (game.initial[row][col] === 0) {
    game.board[row][col] = 0;
    updateBoard();
  }
}

function giveHint() {
  const hint = game.getRandomHint();
  if (hint) {
    selectedCell = [hint.row, hint.col];
    game.board[hint.row][hint.col] = hint.num;
    updateBoard();
    setStatus(`Pista: (${hint.row + 1},${hint.col + 1}) = ${hint.num}`, 'info');
    if (game.isCompleted()) {
      setStatus('¡Ganaste ù.ú!', 'success');
      score[currentLevel]++;
      saveScore();
      updateScoreboard();
    }
  } else {
    setStatus('No hay celdas vacías para pista', 'info');
  }
}

function setStatus(msg, type) {
  const status = document.getElementById('status');
  status.textContent = msg;
  status.className = 'fs-5';
  if (type === 'success') status.classList.add('text-success');
  else if (type === 'warning') status.classList.add('text-warning');
  else if (type === 'info') status.classList.add('text-info');
}

function updateScoreboard() {
  document.getElementById('score-easy').textContent = score.easy;
  document.getElementById('score-medium').textContent = score.medium;
  document.getElementById('score-hard').textContent = score.hard;
}

function saveScore() {
  fetch('/api/score', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(score)
  });
}

function loadScore() {
  fetch('/api/score')
    .then(res => res.json())
    .then(data => {
      score = data;
      updateScoreboard();
    });
}

function buildNumpad() {
  const numpad = document.getElementById('numpad');
  numpad.innerHTML = '';
  for (let n = 1; n <= 9; n++) {
    const btn = document.createElement('button');
    btn.className = 'btn btn-outline-light';
    btn.textContent = n;
    btn.style.width = '50px';
    btn.style.height = '50px';
    btn.onclick = () => insertNumber(n);
    numpad.appendChild(btn);
  }
  const delBtn = document.createElement('button');
  delBtn.className = 'btn btn-outline-secondary';
  delBtn.textContent = 'Borrar';
  delBtn.style.width = '90px';
  delBtn.style.height = '50px';
  delBtn.style.marginLeft = '8px';
  delBtn.onclick = deleteNumber;
  numpad.appendChild(delBtn);
}

function startGame(level) {
  currentLevel = level;
  const puzzle = PUZZLES[level];
  game = new SudokuGame(puzzle.initial, puzzle.solution);
  selectedCell = null;
  buildBoard();
  updateBoard();
  setStatus('');
}

document.getElementById('btn-easy').onclick = () => startGame('easy');
document.getElementById('btn-medium').onclick = () => startGame('medium');
document.getElementById('btn-hard').onclick = () => startGame('hard');
document.getElementById('btn-new').onclick = () => startGame(currentLevel);
document.getElementById('btn-reset-score').onclick = () => {
  score = { easy: 0, medium: 0, hard: 0 };
  saveScore();
  updateScoreboard();
};
document.getElementById('btn-hint').onclick = giveHint;

window.onload = () => {
  buildNumpad();
  startGame('easy');
  loadScore();
  // Teclado: números, borrar, flechas, WASD
  document.addEventListener('keydown', (e) => {
    if (!selectedCell) return;
    if (e.key >= '1' && e.key <= '9') insertNumber(parseInt(e.key));
    else if (e.key === 'Backspace' || e.key === 'Delete') deleteNumber();
    else if (['ArrowLeft', 'a', 'A'].includes(e.key)) {
      let [row, col] = selectedCell;
      if (col > 0) selectCell(row, col - 1);
    } else if (['ArrowRight', 'd', 'D'].includes(e.key)) {
      let [row, col] = selectedCell;
      if (col < 8) selectCell(row, col + 1);
    } else if (['ArrowUp', 'w', 'W'].includes(e.key)) {
      let [row, col] = selectedCell;
      if (row > 0) selectCell(row - 1, col);
    } else if (['ArrowDown', 's', 'S'].includes(e.key)) {
      let [row, col] = selectedCell;
      if (row < 8) selectCell(row + 1, col);
    }
  });
};