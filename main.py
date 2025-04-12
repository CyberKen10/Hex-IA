import os
from hex_board import HexBoard
from player import IAPlayer
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
def main():
    print("Bienvenido a HEX")
    try:
        size = int(input("Ingrese el tamaño del tablero (por ejemplo, 5): "))
    except ValueError:
        print("Tamaño inválido. Usando tamaño 5 por defecto.")
        size = 5
    board = HexBoard(size)
    mode = input("Seleccione modo de juego (1: Humano vs Humano, 2: Humano vs IA, 3: IA vs IA): ")
    if mode == "2":
        human_player = int(input("Elija su identificador (1 para 🟦, 2 para 🟥): "))
        ai_player = 2 if human_player == 1 else 1
        player_objects = {
            human_player: None,
            ai_player: IAPlayer(ai_player)
        }
    elif mode == "3":
        player_objects = {
            1: IAPlayer(1),
            2: IAPlayer(2)
        }
    else:
        player_objects = {
            1: None,
            2: None
        }
    current_player = 1
    consecutive_invalid_moves = 0
    max_invalid_moves = 3
    while True:
        clear_console()
        board.print_board()
        if board.check_connection(1):
            print("¡El jugador 1 (🟦) ha ganado!")
            break
        if board.check_connection(2):
            print("¡El jugador 2 (🟥) ha ganado!")
            break
        possible_moves = board.get_possible_moves()
        if not possible_moves:
            print("Empate. No hay más movimientos disponibles.")
            break
        print(f"\n \n Turno del jugador {current_player} ({'🟦' if current_player==1 else '🟥'}).")
        if player_objects.get(current_player) is None:
            try:
                move_input = input("Ingrese su movimiento como 'fila columna': ")
                row, col = map(int, move_input.split())
                if (row, col) not in possible_moves:
                    print("Movimiento no válido o casilla ocupada. Inténtelo de nuevo.")
                    continue
                board.place_piece(row, col, current_player)
                consecutive_invalid_moves = 0
            except Exception as e:
                print("Entrada inválida. Inténtelo de nuevo.")
                continue
        else:
            move = player_objects[current_player].play(board)
            if move not in possible_moves:
                consecutive_invalid_moves += 1
                if consecutive_invalid_moves >= max_invalid_moves:
                    print(f"La IA del jugador {current_player} ha realizado demasiados movimientos inválidos. Fin del juego.")
                    break
                continue
            print(f"La IA ({current_player}) juega en la posición: {move}")
            board.place_piece(move[0], move[1], current_player)
            consecutive_invalid_moves = 0
        current_player = 2 if current_player == 1 else 1
if __name__ == "__main__":
    main()
