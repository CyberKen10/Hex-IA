from hex_board import HexBoard
import math
import random

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
        self.max_depth =2
    def play(self, board: HexBoard) -> tuple:
        possible_moves = board.get_possible_moves()
        possible_moves = self._sort_moves(board, possible_moves)
        best_score = float('-inf')
        best_move = None

        for move in possible_moves:
            new_board = board.clone()
            new_board.place_piece(move[0], move[1], self.player_id)
            score = self._minimax(new_board, self.max_depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move if best_move else random.choice(possible_moves)
    def _minimax(self, board: HexBoard, depth: int, is_maximizing: bool) -> float:
        opponent = 2 if self.player_id == 1 else 1

        # Terminal conditions
        if board.check_connection(self.player_id):
            return 1000
        if board.check_connection(opponent):
            return -1000
        if depth == 0 or not board.get_possible_moves():
            # Basic evaluation: returns 0 (to be improved later)
            return 0

        possible_moves = board.get_possible_moves()

        if is_maximizing:
            best_eval = float('-inf')
            for move in possible_moves:
                new_board = board.clone()
                new_board.place_piece(move[0], move[1], self.player_id)
                eval = self._minimax(new_board, depth - 1, False)
                best_eval = max(best_eval, eval)
            return best_eval
        else:
            best_eval = float('inf')
            for move in possible_moves:
                new_board = board.clone()
                new_board.place_piece(move[0], move[1], opponent)
                eval = self._minimax(new_board, depth - 1, True)
                best_eval = min(best_eval, eval)
            return best_eval

    def _sort_moves(self, board: HexBoard, moves: list) -> list:
        move_scores = []
        for move in moves:
            score = - (abs(move[0] - board.size // 2) + abs(move[1] - board.size // 2))
            # Prioritize strategic border moves based on the player
            if self.player_id == 1:
                if move[1] == 0 or move[1] == board.size - 1:
                    score += 5
            else:
                if move[0] == 0 or move[0] == board.size - 1:
                    score += 5
            move_scores.append((move, score))
        return [move for move, _ in sorted(move_scores, key=lambda x: x[1], reverse=True)]