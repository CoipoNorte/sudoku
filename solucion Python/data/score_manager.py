import os
import json

class ScoreManager:
    def __init__(self):
        # Ruta del archivo de puntaje
        self.score_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sudoku_score.json")
        self.scores = {"easy": 0, "medium": 0, "hard": 0}
        self.load_score()

    def save_score(self):
        # Guarda el puntaje en un archivo JSON
        with open(self.score_path, "w") as f:
            json.dump(self.scores, f)

    def load_score(self):
        # Carga el puntaje desde el archivo JSON
        if os.path.exists(self.score_path):
            try:
                with open(self.score_path, "r") as f:
                    self.scores = json.load(f)
            except Exception:
                self.scores = {"easy": 0, "medium": 0, "hard": 0}

"""
- puntaje: score
- guardar: save
- cargar: load
- archivo: file
- ruta: path
"""