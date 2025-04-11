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
        alpha = float('-inf')
        beta = float('inf')

        for move in possible_moves:
            new_board = board.clone()
            new_board.place_piece(move[0], move[1], self.player_id)
            score = self._minimax(new_board, self.max_depth - 1, False,alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
        return best_move if best_move else random.choice(possible_moves)
    def _minimax(self, board: HexBoard, depth: int, is_maximizing: bool,alpha: float, beta: float) -> float:
        opponent = 2 if self.player_id == 1 else 1
        if board.check_connection(self.player_id):
            return 1000
        if board.check_connection(opponent):
            return -1000
        if depth == 0 or not board.get_possible_moves():
            return self._evaluate_board(board)
        possible_moves = board.get_possible_moves()
        if is_maximizing:
            max_eval = float('-inf')
            for move in possible_moves:
                new_board = board.clone()
                new_board.place_piece(move[0], move[1], self.player_id)
                eval = self._minimax(new_board, depth-1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                new_board = board.clone()
                new_board.place_piece(move[0], move[1], opponent)
                eval = self._minimax(new_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  
            return min_eval

    def _evaluate_board(self, board: HexBoard) -> float:
        opponent = 2 if self.player_id == 1 else 1
        score = 0
        my_positions = board.player_positions[self.player_id]
        opp_positions = board.player_positions[opponent]
        for pos in my_positions:
            score += 10 - (abs(pos[0] - board.size // 2) + abs(pos[1] - board.size // 2))
        for pos in opp_positions:
            score -= 10 - (abs(pos[0] - board.size // 2) + abs(pos[1] - board.size // 2))
        if self.player_id == 1: 
            for pos in my_positions:
                if pos[1] == 0:
                    score += 15
                if pos[1] == board.size - 1:
                    score += 15
        else: 
            for pos in my_positions:
                if pos[0] == 0:
                    score += 15
                if pos[0] == board.size - 1:
                    score += 15
        return score

    def _sort_moves(self, board: HexBoard, moves: list) -> list:
        move_scores = []
        for move in moves:
            score = 0
            score -= abs(move[0] - board.size//2) + abs(move[1] - board.size//2)
            if self.player_id == 1:
                if move[1] == 0 or move[1] == board.size - 1:
                    score += 5
            else:
                if move[0] == 0 or move[0] == board.size - 1:
                    score += 5
            move_scores.append((move, score))
        return [move for move, _ in sorted(move_scores, key=lambda x: x[1], reverse=True)]