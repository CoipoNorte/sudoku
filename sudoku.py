import random

# forzar los colores ANSI en Windows importanto colorama señores
from colorama import init
init(autoreset=True)

# ANSI escape codes para colores
class Color:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    GRAY = "\033[90m"

# Crea un tablero vacio
def crear_tablero():
    return [[0 for _ in range(9)] for _ in range(9)]

# Verifica si es valido colocar num en (fila, col)
def es_valido(tablero, fila, col, num):
    for i in range(9):
        if tablero[fila][i] == num or tablero[i][col] == num:
            return False
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (col // 3)
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_col, inicio_col + 3):
            if tablero[i][j] == num:
                return False
    return True

# Genera solucion completa de Sudoku con backtracking
def generar_solucion(tablero):
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num
                        if generar_solucion(tablero):
                            return True
                        tablero[fila][col] = 0
                return False
    return True

# Genera Sudoku resoluble ocultando algunos números
def generar_juego(tablero, cantidad_vacia=40):
    juego = [fila[:] for fila in tablero]
    vacias = 0
    while vacias < cantidad_vacia:
        fila, col = random.randint(0, 8), random.randint(0, 8)
        if juego[fila][col] != 0:
            juego[fila][col] = 0
            vacias += 1
    return juego

# Tablero con colores
def imprimir_tablero(tablero, originales):
    print("\n  ", " ".join(str(i+1) for i in range(9)))
    for i, fila in enumerate(tablero):
        print(i+1, end=" ")
        for j, val in enumerate(fila):
            if val == 0:
                print(f"{Color.GRAY}·{Color.RESET}", end=" ")
            elif originales[i][j] != 0:
                print(f"{Color.GREEN}{val}{Color.RESET}", end=" ")
            else:
                print(f"{Color.BLUE}{val}{Color.RESET}", end=" ")
        print()

# Pista aleatoria
def dar_pista(tablero, solucion, originales):
    opciones = [(i, j) for i in range(9) for j in range(9) if tablero[i][j] == 0]
    if opciones:
        i, j = random.choice(opciones)
        tablero[i][j] = solucion[i][j]
        originales[i][j] = -1  # Marca como pista
        print(f"{Color.YELLOW}Pista colocada en fila {i+1}, columna {j+1}.{Color.RESET}")
    else:
        print(f"{Color.YELLOW}No hay más casillas vacías.{Color.RESET}")

# Juego principal
def jugar():
    solucion = crear_tablero()
    generar_solucion(solucion)
    juego = generar_juego(solucion)
    originales = [fila[:] for fila in juego]

    while True:
        imprimir_tablero(juego, originales)
        accion = input("¿Qué deseas hacer? (insertar [fila col valor], pista, salir): ").strip().lower()
        if accion == "salir":
            print("Gracias por jugar.")
            break
        elif accion == "pista":
            dar_pista(juego, solucion, originales)
        elif accion.startswith("insertar"):
            partes = accion.split()
            if len(partes) == 4:
                try:
                    fila, col, valor = int(partes[1])-1, int(partes[2])-1, int(partes[3])
                    if originales[fila][col] == 0 and es_valido(juego, fila, col, valor):
                        juego[fila][col] = valor
                    else:
                        print(f"{Color.YELLOW}Movimiento inválido o celda bloqueada.{Color.RESET}")
                except:
                    print("Entrada no válida.")
            else:
                print("Formato: insertar fila col valor")
        else:
            print("Comando no reconocido.")

if __name__ == "__main__":
    jugar()
