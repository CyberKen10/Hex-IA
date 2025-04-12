from hex_board import HexBoard
import math
from typing import List

# Definición de la clase base Player
# Esta clase representa un jugador en el juego Hex.
class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # 1 (rojo) or 2 (azul)

    def play(self, board: "HexBoard") -> tuple:
        raise NotImplementedError("Implement this method!")
    

class IAPlayer(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)
        self.rounds = 0
        self.max_depth = 4  # Profundidad máxima inicial
        self.directions = [(0, 1), (1, 0), (1, -1), (-1, 0), (-1, 1), (0, -1)]
        self.cache = {}
        self.eval_cache = {}  # Cache para evaluaciones de estado

    def play(self, board: HexBoard) -> tuple:
        self.board_size = board.size
        possible_moves = board.get_possible_moves()
        
        if not possible_moves:
            return (-1, -1)

        # Primer movimiento: jugar cerca del centro
        if self.rounds == 0:
            center = self.board_size // 2
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    pos = (center + dx, center + dy)
                    if pos in possible_moves:
                        self.rounds += 1
                        return pos
            self.rounds += 1
            return possible_moves[0]

        # Verificar movimientos ganadores o bloqueadores
        winner, play_winner = self.one_move_to_win(board, self.player_id)
        if winner != 0 and play_winner in possible_moves:
            self.rounds += 1
            return play_winner

        # Determinar profundidad dinámicamente según celdas vacías
        empty_cells = len(possible_moves)
        if empty_cells > (self.board_size * self.board_size) // 2:
            depth = 2
        elif empty_cells > (self.board_size * self.board_size) // 4:
            depth = 3
        else:
            depth = 4

        # Usar Minimax con la profundidad determinada
        move = self.minimax_alpha_beta(board, depth, -float('inf'), float('inf'), True)[1]
        
        if move not in possible_moves:
            move = possible_moves[0]

        self.rounds += 1
        return move

    def one_move_to_win(self, board: HexBoard, player_id: int) -> tuple[int, tuple[int, int]]:
        possible_moves = board.get_possible_moves()
        opponent = 3 - player_id

        # Verificar si el oponente podría ganar en un solo movimiento
        for i, j in possible_moves:
            temp_board = board.clone()
            temp_board.place_piece(i, j, opponent)
            if temp_board.check_connection(opponent):
                return (-1, (i, j))

        # Verificar si yo puedo ganar en un solo movimiento
        for i, j in possible_moves:
            temp_board = board.clone()
            temp_board.place_piece(i, j, player_id)
            if temp_board.check_connection(player_id):
                return (1, (i, j))

        return (0, (-1, -1))

    def minimax_alpha_beta(self, board: HexBoard, depth: int, alpha: float, beta: float, maximizing_player: bool) -> tuple[float, tuple]:
        opponent = 3 - self.player_id

        if board.check_connection(self.player_id):
            return (float('inf'), (-1, -1))
        if board.check_connection(opponent):
            return (-float('inf'), (-1, -1))
        if depth == 0 or not board.get_possible_moves():
            return (self.evaluate_game_state(board), (-1, -1))

        possible_moves = self._sort_moves(board, board.get_possible_moves())

        if maximizing_player:
            max_eval = -float('inf')
            best_move = (-1, -1)
            for i, j in possible_moves:
                temp_board = board.clone()
                temp_board.place_piece(i, j, self.player_id)
                eval, _ = self.minimax_alpha_beta(temp_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (i, j)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return (max_eval, best_move)
        else:
            min_eval = float('inf')
            best_move = (-1, -1)
            for i, j in possible_moves:
                temp_board = board.clone()
                temp_board.place_piece(i, j, opponent)
                eval, _ = self.minimax_alpha_beta(temp_board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (i, j)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return (min_eval, best_move)

    def evaluate_game_state(self, board: HexBoard) -> float:
        # Usar cache para evitar recalcular
        board_state = tuple(map(tuple, board.board))
        if board_state in self.eval_cache:
            return self.eval_cache[board_state]

        my_cost = self._astar_search(board.board, self.player_id)
        opp_cost = self._astar_search(board.board, 3 - self.player_id)
        
        connection_diff = self.count_connections(board, self.player_id) - self.count_connections(board, 3 - self.player_id)
        
        if my_cost == 0:
            score = float('inf')
        elif opp_cost == 0:
            score = -float('inf')
        else:
            threat_penalty = 0
            if opp_cost <= 1:
                threat_penalty = -100000
            elif opp_cost <= 2:
                threat_penalty = -5000 / (opp_cost + 1)
            score = 1 / (my_cost + 1e-6) + opp_cost + 0.1 * connection_diff + threat_penalty
        
        self.eval_cache[board_state] = score
        return score

    def count_connections(self, board: HexBoard, player: int) -> int:
        count = 0
        visited_pairs = set()
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board.board[i][j] == player:
                    for dx, dy in self.directions:
                        ni, nj = i + dx, j + dy
                        if (0 <= ni < self.board_size and 0 <= nj < self.board_size and 
                            board.board[ni][nj] == player):
                            pair = tuple(sorted([(i, j), (ni, nj)]))
                            if pair not in visited_pairs:
                                visited_pairs.add(pair)
                                count += 1
        return count

    def _sort_moves(self, board: HexBoard, moves: list) -> list:
        center = self.board_size // 2
        move_scores = []
        opponent = 3 - self.player_id

        for move in moves:
            i, j = move
            score = 0

            # Priorizar movimientos cerca de piezas existentes
            num_adj_total = sum(1 for dx, dy in self.directions 
                                if 0 <= i + dx < self.board_size and 0 <= j + dy < self.board_size 
                                and board.board[i + dx][j + dy] != 0)
            score += num_adj_total * 3

            # Cercanía al centro
            score -= abs(i - center) + abs(j - center)

            # Conexiones con mis piezas
            num_adj_my = sum(1 for dx, dy in self.directions 
                            if 0 <= i + dx < self.board_size and 0 <= j + dy < self.board_size 
                            and board.board[i + dx][j + dy] == self.player_id)
            score += num_adj_my * 2

            # Bloqueo al oponente
            num_adj_opp = sum(1 for dx, dy in self.directions 
                             if 0 <= i + dx < self.board_size and 0 <= j + dy < self.board_size 
                             and board.board[i + dx][j + dy] == opponent)
            score += num_adj_opp * 1

            # Bonus por bordes relevantes:
            # Para jugador 1 (horizontal) se premia si está en la primera o última columna.
            # Para jugador 2 (vertical) se premia si está en la primera o última fila.
            if self.player_id == 1:
                if j == 0 or j == self.board_size - 1:
                    score += 5
            else:
                if i == 0 or i == self.board_size - 1:
                    score += 5

            move_scores.append((move, score))

        return [move for move, _ in sorted(move_scores, key=lambda x: x[1], reverse=True)]

    def _heuristic(self, x: int, y: int, player: int) -> float:
        # Para jugador 1: distancia horizontal (columna) al borde derecho.
        # Para jugador 2: distancia vertical (fila) al borde inferior.
        if player == 1:
            return abs(self.board_size - 1 - y)
        return abs(self.board_size - 1 - x)

    def _astar_search(self, board: List[List[int]], player: int) -> float:
        n = self.board_size
        distances = [[math.inf] * n for _ in range(n)]
        heap = []

        if player == 1:  # Jugador 1: horizontal (izquierda-derecha)
            for i in range(n):
                if board[i][0] == player:
                    cost = 0
                elif board[i][0] == 0:
                    cost = 1
                else:
                    continue
                distances[i][0] = cost
                h = self._heuristic(i, 0, player)
                heap.append((cost + h, cost, i, 0))

            best = math.inf
            target_col = n - 1
            while heap:
                priority, cost, x, y = heap.pop(0)
                if y == target_col:
                    best = min(best, cost)
                    if best == 0:
                        return best
                if cost > distances[x][y]:
                    continue
                for dx, dy in self.directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n:
                        new_cost = cost + (0 if board[nx][ny] == player else 1 if board[nx][ny] == 0 else math.inf)
                        if new_cost < distances[nx][ny]:
                            distances[nx][ny] = new_cost
                            h = self._heuristic(nx, ny, player)
                            heap.append((new_cost + h, new_cost, nx, ny))
            return best
        else:  # Jugador 2: vertical (arriba-abajo)
            for j in range(n):
                if board[0][j] == player:
                    cost = 0
                elif board[0][j] == 0:
                    cost = 1
                else:
                    continue
                distances[0][j] = cost
                h = self._heuristic(0, j, player)
                heap.append((cost + h, cost, 0, j))

            best = math.inf
            target_row = n - 1
            while heap:
                priority, cost, x, y = heap.pop(0)
                if x == target_row:
                    best = min(best, cost)
                    if best == 0:
                        return best
                if cost > distances[x][y]:
                    continue
                for dx, dy in self.directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n:
                        new_cost = cost + (0 if board[nx][ny] == player else 1 if board[nx][ny] == 0 else math.inf)
                        if new_cost < distances[nx][ny]:
                            distances[nx][ny] = new_cost
                            h = self._heuristic(nx, ny, player)
                            heap.append((new_cost + h, new_cost, nx, ny))
            return best