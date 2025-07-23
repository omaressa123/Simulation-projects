## **CHESS GAME PLAY**
## 1- Required libraries: tkinter for GUI, simpledialog and messagebox for user input and alerts.
## 2- Chessboard is 8x8, alternating black and white squares.
## 3- Each element: King, Queen, Rook, Bishop, Knight, Pawn for both white and black, using Unicode symbols.
## 4- Main rules: Standard chess rules including all legal moves, castling, en passant, pawn promotion, check, checkmate, stalemate, and draw conditions.
## 5- Number of players: 2 (White and Black).
## 6- Time: User chooses time per player (default 10 minutes).
## 7- Goal: Checkmate the opponent's king or win by timeout; game can also end in stalemate or draw.
## 8- Players alternate turns, moving their own pieces according to chess rules.
## 9- Each piece moves according to standard chess rules:
##     - Pawn: Forward 1 (or 2 from start), captures diagonally, en passant, promotes on last rank.
##     - Knight: L-shape (2+1).
##     - Bishop: Diagonal.
##     - Rook: Straight lines.
##     - Queen: Any direction.
##     - King: One square any direction, can castle.
## 10- Illegal moves: Moving into check, moving through pieces (except knight), moving opponent's pieces, illegal castling, etc.
## 11- Time per player is set at game start.
## 12- Player score increases by 1 for each win.
## 13- Player info: name, age, score, games played.
## 14- Number of games played tracked per player.
## Enhanced: Visual shadow for selected piece, move lines for possible moves, and robust checkmate detection.

import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import copy
import threading
import time

BOARD_SIZE = 8  # 8x8 chessboard

SQUARE_COLORS = ('white', 'black')

PIECES = {
    'white': {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙'
    },
    'black': {
        'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟'
    }
}

PIECE_COLORS = {
    'white': '#e0c068',  # light gold
    'black': '#4040a0',  # deep blue
}

NUM_PLAYERS = 2
DEFAULT_TIME_MINUTES = 10

STARTING_POSITION = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
]

class Player:
    def __init__(self, name, age, is_computer=False):
        self.name = name
        self.age = age
        self.score = 0
        self.games_played = 0
        self.is_computer = is_computer

# --- AI Section ---

PIECE_VALUES = {
    'K': 0,  # King value is handled by checkmate
    'Q': 900,
    'R': 500,
    'B': 330,
    'N': 320,
    'P': 100
}

# Piece-square tables for positional evaluation (simplified, for both colors)
PIECE_SQUARE_TABLES = {
    'P': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    'N': [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ],
    'B': [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ],
    'R': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]
    ],
    'Q': [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ],
    'K': [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20]
    ]
}

def evaluate_board(board, color):
    # Material + piece-square tables
    score = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            code = board[r][c]
            if code:
                piece = code[1]
                sign = 1 if code[0] == color else -1
                value = PIECE_VALUES.get(piece, 0)
                pst = PIECE_SQUARE_TABLES.get(piece, [[0]*8]*8)
                # For black, flip the table
                if code[0] == 'w':
                    pst_score = pst[r][c]
                else:
                    pst_score = pst[7 - r][c]
                score += sign * (value + pst_score)
    return score

def all_legal_moves(game, board, color, en_passant_target, castling_rights):
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            code = board[r][c]
            if code and code[0] == color:
                for rr in range(BOARD_SIZE):
                    for cc in range(BOARD_SIZE):
                        if game.is_valid_move_custom(board, en_passant_target, castling_rights, r, c, rr, cc):
                            moves.append((r, c, rr, cc))
    return moves

def is_checkmate_custom(game, board, color, en_passant_target, castling_rights):
    opp_color = 'b' if color == 'w' else 'w'
    king_pos = None
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == color + 'K':
                king_pos = (r, c)
    if not king_pos:
        return True
    if not game.square_attacked_custom(board, king_pos[0], king_pos[1], opp_color):
        return False
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            code = board[r][c]
            if code and code[0] == color:
                for rr in range(BOARD_SIZE):
                    for cc in range(BOARD_SIZE):
                        if game.is_valid_move_custom(board, en_passant_target, castling_rights, r, c, rr, cc):
                            # Try move
                            backup = [row[:] for row in board]
                            move_code = board[r][c]
                            move_target = board[rr][cc]
                            board[rr][cc] = move_code
                            board[r][c] = None
                            king_pos2 = (rr, cc) if move_code[1] == 'K' else king_pos
                            in_check = game.square_attacked_custom(board, king_pos2[0], king_pos2[1], opp_color)
                            board = [row[:] for row in backup]
                            if not in_check:
                                return False
    return True

def minimax(game, board, en_passant_target, castling_rights, depth, alpha, beta, maximizing, color, orig_color):
    # Returns (score, move)
    if depth == 0:
        return evaluate_board(board, orig_color), None
    moves = all_legal_moves(game, board, color, en_passant_target, castling_rights)
    if not moves:
        if is_checkmate_custom(game, board, color, en_passant_target, castling_rights):
            return (-99999 if maximizing else 99999), None
        else:
            return 0, None  # Stalemate
    best_move = None
    if maximizing:
        max_eval = -float('inf')
        for move in moves:
            new_board = [row[:] for row in board]
            new_en_passant = en_passant_target
            new_castling = dict(castling_rights)
            # Simulate move
            r1, c1, r2, c2 = move
            code = new_board[r1][c1]
            kind = code[1]
            # Handle en passant
            if kind == 'P' and abs(r2 - r1) == 2:
                new_en_passant = ((r1 + r2) // 2, c1)
            else:
                new_en_passant = None
            # Handle castling rights
            if code == 'wK':
                new_castling['wK'] = False
                new_castling['wQ'] = False
            if code == 'bK':
                new_castling['bK'] = False
                new_castling['bQ'] = False
            if code == 'wR':
                if r1 == 7 and c1 == 0:
                    new_castling['wQ'] = False
                if r1 == 7 and c1 == 7:
                    new_castling['wK'] = False
            if code == 'bR':
                if r1 == 0 and c1 == 0:
                    new_castling['bQ'] = False
                if r1 == 0 and c1 == 7:
                    new_castling['bK'] = False
            # Castling move
            if kind == 'K' and abs(c2 - c1) == 2:
                row = r1
                if c2 == 6:  # kingside
                    new_board[row][4] = None
                    new_board[row][6] = code
                    new_board[row][7] = None
                    new_board[row][5] = code[0] + 'R'
                else:  # queenside
                    new_board[row][4] = None
                    new_board[row][2] = code
                    new_board[row][0] = None
                    new_board[row][3] = code[0] + 'R'
            else:
                # En passant capture
                if kind == 'P' and (r2, c2) == en_passant_target and not new_board[r2][c2]:
                    if code[0] == 'w':
                        captured_row = r2 + 1
                    else:
                        captured_row = r2 - 1
                    new_board[captured_row][c2] = None
                # Normal move
                new_board[r2][c2] = code
                new_board[r1][c1] = None
                # Pawn promotion
                if kind == 'P' and (r2 == 0 or r2 == 7):
                    new_board[r2][c2] = code[0] + 'Q'
            eval_score, _ = minimax(game, new_board, new_en_passant, new_castling, depth-1, alpha, beta, False, 'b' if color == 'w' else 'w', orig_color)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = [row[:] for row in board]
            new_en_passant = en_passant_target
            new_castling = dict(castling_rights)
            r1, c1, r2, c2 = move
            code = new_board[r1][c1]
            kind = code[1]
            if kind == 'P' and abs(r2 - r1) == 2:
                new_en_passant = ((r1 + r2) // 2, c1)
            else:
                new_en_passant = None
            if code == 'wK':
                new_castling['wK'] = False
                new_castling['wQ'] = False
            if code == 'bK':
                new_castling['bK'] = False
                new_castling['bQ'] = False
            if code == 'wR':
                if r1 == 7 and c1 == 0:
                    new_castling['wQ'] = False
                if r1 == 7 and c1 == 7:
                    new_castling['wK'] = False
            if code == 'bR':
                if r1 == 0 and c1 == 0:
                    new_castling['bQ'] = False
                if r1 == 0 and c1 == 7:
                    new_castling['bK'] = False
            if kind == 'K' and abs(c2 - c1) == 2:
                row = r1
                if c2 == 6:  # kingside
                    new_board[row][4] = None
                    new_board[row][6] = code
                    new_board[row][7] = None
                    new_board[row][5] = code[0] + 'R'
                else:  # queenside
                    new_board[row][4] = None
                    new_board[row][2] = code
                    new_board[row][0] = None
                    new_board[row][3] = code[0] + 'R'
            else:
                if kind == 'P' and (r2, c2) == en_passant_target and not new_board[r2][c2]:
                    if code[0] == 'w':
                        captured_row = r2 + 1
                    else:
                        captured_row = r2 - 1
                    new_board[captured_row][c2] = None
                new_board[r2][c2] = code
                new_board[r1][c1] = None
                if kind == 'P' and (r2 == 0 or r2 == 7):
                    new_board[r2][c2] = code[0] + 'Q'
            eval_score, _ = minimax(game, new_board, new_en_passant, new_castling, depth-1, alpha, beta, True, 'b' if color == 'w' else 'w', orig_color)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

class ChessGame:
    def __init__(self, root, player1, player2, time_minutes=DEFAULT_TIME_MINUTES):
        self.root = root
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.current_player_idx = 0  # 0: white, 1: black
        self.time_minutes = time_minutes
        self.board = [row[:] for row in STARTING_POSITION]
        self.piece_ids = {}
        self.selected = None
        self.square_size = 60
        self.canvas = tk.Canvas(root, width=BOARD_SIZE*self.square_size, height=BOARD_SIZE*self.square_size)
        self.canvas.pack()
        self.create_chessboard()
        self.show_starting_position()
        self.canvas.bind("<Button-1>", self.on_click)
        self.status_label = tk.Label(root, text=self.status_text())
        self.status_label.pack()
        self.timers = [self.time_minutes*60, self.time_minutes*60]
        self.timer_labels = [
            tk.Label(root, text=f"{self.player1.name} Time: {self.format_time(self.timers[0])}"),
            tk.Label(root, text=f"{self.player2.name} Time: {self.format_time(self.timers[1])}")
        ]
        self.timer_labels[0].pack()
        self.timer_labels[1].pack()
        self.game_over = False
        self.castling_rights = {'wK': True, 'wQ': True, 'bK': True, 'bQ': True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.move_history = []
        # For visual feedback
        self.shadow_id = None
        self.move_line_ids = []
        self.update_timer()
        # AI
        self.ai_thinking = False
        self.ai_depth = 3  # Medium-difficult: 3 plies (can increase to 4 for more difficulty)

        # Patch for AI: allow custom move validation for board copies
        self._patch_custom_methods()

        # If computer is white, start AI move
        self.root.after(100, self.check_ai_move)

    def _patch_custom_methods(self):
        # Add custom move validation for board copies (for AI)
        def is_valid_move_custom(board, en_passant_target, castling_rights, from_row, from_col, to_row, to_col):
            code = board[from_row][from_col]
            if not code:
                return False
            if (from_row, from_col) == (to_row, to_col):
                return False
            target = board[to_row][to_col]
            if target and target[0] == code[0]:
                return False
            kind = code[1]
            dr = to_row - from_row
            dc = to_col - from_col
            color = code[0]
            opp_color = 'b' if color == 'w' else 'w'

            # Pawn moves
            if kind == 'P':
                direction = -1 if color == 'w' else 1
                start_row = 6 if color == 'w' else 1
                # Normal move
                if dc == 0 and dr == direction and not target:
                    return True
                # Double move from start
                if dc == 0 and dr == 2*direction and from_row == start_row and not target and not board[from_row+direction][from_col]:
                    return True
                # Capture
                if abs(dc) == 1 and dr == direction and target and target[0] == opp_color:
                    return True
                # En passant
                if abs(dc) == 1 and dr == direction and not target and en_passant_target == (to_row, to_col):
                    return True
                return False
            # Knight moves
            elif kind == 'N':
                if (abs(dr), abs(dc)) in [(2, 1), (1, 2)]:
                    return True
                return False
            # Bishop moves
            elif kind == 'B':
                if abs(dr) == abs(dc) and self.clear_path_custom(board, from_row, from_col, to_row, to_col):
                    return True
                return False
            # Rook moves
            elif kind == 'R':
                if (dr == 0 or dc == 0) and self.clear_path_custom(board, from_row, from_col, to_row, to_col):
                    return True
                return False
            # Queen moves
            elif kind == 'Q':
                if ((dr == 0 or dc == 0) or abs(dr) == abs(dc)) and self.clear_path_custom(board, from_row, from_col, to_row, to_col):
                    return True
                return False
            # King moves
            elif kind == 'K':
                if max(abs(dr), abs(dc)) == 1:
                    # Normal king move
                    if not self.square_attacked_custom(board, to_row, to_col, opp_color):
                        return True
                    return False
                # Castling
                if from_row == to_row and abs(dc) == 2:
                    if self.can_castle_custom(board, castling_rights, color, dc > 0):
                        return True
                return False
            return False

        def clear_path_custom(board, from_row, from_col, to_row, to_col):
            dr = to_row - from_row
            dc = to_col - from_col
            step_r = (dr > 0) - (dr < 0)
            step_c = (dc > 0) - (dc < 0)
            r, c = from_row + step_r, from_col + step_c
            while (r, c) != (to_row, to_col):
                if board[r][c]:
                    return False
                r += step_r
                c += step_c
            return True

        def can_castle_custom(board, castling_rights, color, kingside):
            row = 7 if color == 'w' else 0
            if kingside:
                if not castling_rights[color + 'K']:
                    return False
                if board[row][5] or board[row][6]:
                    return False
                if self.square_attacked_custom(board, row, 4, 'b' if color == 'w' else 'w') or \
                   self.square_attacked_custom(board, row, 5, 'b' if color == 'w' else 'w') or \
                   self.square_attacked_custom(board, row, 6, 'b' if color == 'w' else 'w'):
                    return False
                rook = board[row][7]
                if rook != color + 'R':
                    return False
                return True
            else:
                if not castling_rights[color + 'Q']:
                    return False
                if board[row][1] or board[row][2] or board[row][3]:
                    return False
                if self.square_attacked_custom(board, row, 4, 'b' if color == 'w' else 'w') or \
                   self.square_attacked_custom(board, row, 3, 'b' if color == 'w' else 'w') or \
                   self.square_attacked_custom(board, row, 2, 'b' if color == 'w' else 'w'):
                    return False
                rook = board[row][0]
                if rook != color + 'R':
                    return False
                return True

        def square_attacked_custom(board, row, col, by_color):
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    code = board[r][c]
                    if code and code[0] == by_color:
                        if self._attacks_square_custom(board, r, c, row, col):
                            return True
            return False

        def _attacks_square_custom(board, from_row, from_col, to_row, to_col):
            code = board[from_row][from_col]
            if not code:
                return False
            kind = code[1]
            dr = to_row - from_row
            dc = to_col - from_col
            color = code[0]
            opp_color = 'b' if color == 'w' else 'w'
            if kind == 'P':
                direction = -1 if color == 'w' else 1
                if abs(dc) == 1 and dr == direction:
                    return True
                return False
            elif kind == 'N':
                if (abs(dr), abs(dc)) in [(2, 1), (1, 2)]:
                    return True
                return False
            elif kind == 'B':
                if abs(dr) == abs(dc) and clear_path_custom(board, from_row, from_col, to_row, to_col):
                    return True
                return False
            elif kind == 'R':
                if (dr == 0 or dc == 0) and clear_path_custom(board, from_row, from_col, to_row, to_col):
                    return True
                return False
            elif kind == 'Q':
                if ((dr == 0 or dc == 0) or abs(dr) == abs(dc)) and clear_path_custom(board, from_row, from_col, to_row, to_col):
                    return True
                return False
            elif kind == 'K':
                if max(abs(dr), abs(dc)) == 1:
                    return True
                return False
            return False

        self.is_valid_move_custom = is_valid_move_custom
        self.clear_path_custom = clear_path_custom
        self.can_castle_custom = can_castle_custom
        self.square_attacked_custom = square_attacked_custom
        self._attacks_square_custom = _attacks_square_custom

    def create_chessboard(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = SQUARE_COLORS[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')

    def show_starting_position(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                code = self.board[row][col]
                if code:
                    kind = code[1]
                    color = 'white' if code[0] == 'w' else 'black'
                    piece = PIECES[color][kind]
                    piece_id = self.create_piece(piece, row, col, color)
                    self.piece_ids[(row, col)] = piece_id

    def create_piece(self, piece, row, col, color):
        x = col * self.square_size + self.square_size // 2
        y = row * self.square_size + self.square_size // 2
        return self.canvas.create_text(
            x, y, text=piece, font=('Arial', self.square_size//2), tags="piece", fill=PIECE_COLORS[color]
        )

    def move_piece(self, from_row, from_col, to_row, to_col):
        piece_id = self.piece_ids.pop((from_row, from_col))
        self.piece_ids[(to_row, to_col)] = piece_id
        x = to_col * self.square_size + self.square_size // 2
        y = to_row * self.square_size + self.square_size // 2
        self.canvas.coords(piece_id, x, y)
        # Remove captured piece
        if (to_row, to_col) in self.piece_ids and (from_row, from_col) != (to_row, to_col):
            self.canvas.delete(self.piece_ids[(to_row, to_col)])

    def on_click(self, event):
        if self.game_over:
            return
        # If it's computer's turn, ignore clicks
        if self.players[self.current_player_idx].is_computer:
            return
        col = event.x // self.square_size
        row = event.y // self.square_size
        # Remove previous visual feedback
        self.clear_shadow_and_lines()
        if self.selected:
            from_row, from_col = self.selected
            if (from_row, from_col) == (row, col):
                self.selected = None
                return
            if self.is_valid_move(from_row, from_col, row, col):
                self.make_move(from_row, from_col, row, col)
                self.selected = None
                self.next_turn()
                self.root.after(100, self.check_ai_move)
            else:
                messagebox.showinfo("Invalid Move", "That move is not allowed.")
                self.selected = None
        else:
            code = self.board[row][col]
            if code and ((self.current_player_idx == 0 and code[0] == 'w') or (self.current_player_idx == 1 and code[0] == 'b')):
                self.selected = (row, col)
                # Draw shadow and move lines
                self.draw_shadow(row, col)
                self.draw_move_lines(row, col)

    def draw_shadow(self, row, col):
        # Draw a semi-transparent oval under the selected piece
        x = col * self.square_size + self.square_size // 2
        y = row * self.square_size + self.square_size // 2
        r = self.square_size // 2 - 4
        # Use stipple for shadow effect
        self.shadow_id = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill="#888888", outline="", stipple="gray25", tags="shadow"
        )
        # Raise the piece above the shadow
        if (row, col) in self.piece_ids:
            self.canvas.tag_raise(self.piece_ids[(row, col)])

    def draw_move_lines(self, from_row, from_col):
        # Draw lines from the selected piece to all legal destination squares
        legal_moves = self.get_legal_moves(from_row, from_col)
        x0 = from_col * self.square_size + self.square_size // 2
        y0 = from_row * self.square_size + self.square_size // 2
        for to_row, to_col in legal_moves:
            x1 = to_col * self.square_size + self.square_size // 2
            y1 = to_row * self.square_size + self.square_size // 2
            line_id = self.canvas.create_line(
                x0, y0, x1, y1,
                fill="#00bfff", width=3, arrow=tk.LAST, dash=(4, 2), tags="move_line"
            )
            self.move_line_ids.append(line_id)
            # Optionally, draw a small circle at the destination
            r = 8
            circ_id = self.canvas.create_oval(
                x1 - r, y1 - r, x1 + r, y1 + r,
                outline="#00bfff", width=2, fill="", tags="move_line"
            )
            self.move_line_ids.append(circ_id)

    def clear_shadow_and_lines(self):
        if self.shadow_id:
            self.canvas.delete(self.shadow_id)
            self.shadow_id = None
        for lid in self.move_line_ids:
            self.canvas.delete(lid)
        self.move_line_ids = []

    def get_legal_moves(self, from_row, from_col):
        # Return a list of (to_row, to_col) for all legal moves for the piece at (from_row, from_col)
        code = self.board[from_row][from_col]
        if not code:
            return []
        color = code[0]
        opp_color = 'b' if color == 'w' else 'w'
        moves = []
        for to_row in range(BOARD_SIZE):
            for to_col in range(BOARD_SIZE):
                if self.is_valid_move(from_row, from_col, to_row, to_col):
                    # Simulate move to check for king safety
                    backup = [row[:] for row in self.board]
                    move_code = self.board[from_row][from_col]
                    move_target = self.board[to_row][to_col]
                    self.board[to_row][to_col] = move_code
                    self.board[from_row][from_col] = None
                    king_pos = None
                    for r in range(BOARD_SIZE):
                        for c in range(BOARD_SIZE):
                            if self.board[r][c] == color + 'K':
                                king_pos = (r, c)
                    if move_code[1] == 'K':
                        king_pos = (to_row, to_col)
                    in_check = self.square_attacked(king_pos[0], king_pos[1], opp_color)
                    self.board = [row[:] for row in backup]
                    if not in_check:
                        moves.append((to_row, to_col))
        return moves

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        code = self.board[from_row][from_col]
        if not code:
            return False
        if (from_row, from_col) == (to_row, to_col):
            return False
        target = self.board[to_row][to_col]
        if target and target[0] == code[0]:
            return False
        kind = code[1]
        dr = to_row - from_row
        dc = to_col - from_col
        color = code[0]
        opp_color = 'b' if color == 'w' else 'w'

        # Pawn moves
        if kind == 'P':
            direction = -1 if color == 'w' else 1
            start_row = 6 if color == 'w' else 1
            # Normal move
            if dc == 0 and dr == direction and not target:
                return True
            # Double move from start
            if dc == 0 and dr == 2*direction and from_row == start_row and not target and not self.board[from_row+direction][from_col]:
                return True
            # Capture
            if abs(dc) == 1 and dr == direction and target and target[0] == opp_color:
                return True
            # En passant
            if abs(dc) == 1 and dr == direction and not target and self.en_passant_target == (to_row, to_col):
                return True
            return False
        # Knight moves
        elif kind == 'N':
            if (abs(dr), abs(dc)) in [(2, 1), (1, 2)]:
                return True
            return False
        # Bishop moves
        elif kind == 'B':
            if abs(dr) == abs(dc) and self.clear_path(from_row, from_col, to_row, to_col):
                return True
            return False
        # Rook moves
        elif kind == 'R':
            if (dr == 0 or dc == 0) and self.clear_path(from_row, from_col, to_row, to_col):
                return True
            return False
        # Queen moves
        elif kind == 'Q':
            if ((dr == 0 or dc == 0) or abs(dr) == abs(dc)) and self.clear_path(from_row, from_col, to_row, to_col):
                return True
            return False
        # King moves
        elif kind == 'K':
            if max(abs(dr), abs(dc)) == 1:
                # Normal king move
                if not self.square_attacked(to_row, to_col, opp_color):
                    return True
                return False
            # Castling
            if from_row == to_row and abs(dc) == 2:
                if self.can_castle(color, dc > 0):
                    return True
            return False
        return False

    def clear_path(self, from_row, from_col, to_row, to_col):
        dr = to_row - from_row
        dc = to_col - from_col
        step_r = (dr > 0) - (dr < 0)
        step_c = (dc > 0) - (dc < 0)
        r, c = from_row + step_r, from_col + step_c
        while (r, c) != (to_row, to_col):
            if self.board[r][c]:
                return False
            r += step_r
            c += step_c
        return True

    def can_castle(self, color, kingside):
        row = 7 if color == 'w' else 0
        if kingside:
            if not self.castling_rights[color + 'K']:
                return False
            if self.board[row][5] or self.board[row][6]:
                return False
            if self.square_attacked(row, 4, 'b' if color == 'w' else 'w') or \
               self.square_attacked(row, 5, 'b' if color == 'w' else 'w') or \
               self.square_attacked(row, 6, 'b' if color == 'w' else 'w'):
                return False
            rook = self.board[row][7]
            if rook != color + 'R':
                return False
            return True
        else:
            if not self.castling_rights[color + 'Q']:
                return False
            if self.board[row][1] or self.board[row][2] or self.board[row][3]:
                return False
            if self.square_attacked(row, 4, 'b' if color == 'w' else 'w') or \
               self.square_attacked(row, 3, 'b' if color == 'w' else 'w') or \
               self.square_attacked(row, 2, 'b' if color == 'w' else 'w'):
                return False
            rook = self.board[row][0]
            if rook != color + 'R':
                return False
            return True

    def square_attacked(self, row, col, by_color):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                code = self.board[r][c]
                if code and code[0] == by_color:
                    if self._attacks_square(r, c, row, col):
                        return True
        return False

    def _attacks_square(self, from_row, from_col, to_row, to_col):
        code = self.board[from_row][from_col]
        if not code:
            return False
        kind = code[1]
        dr = to_row - from_row
        dc = to_col - from_col
        color = code[0]
        opp_color = 'b' if color == 'w' else 'w'
        if kind == 'P':
            direction = -1 if color == 'w' else 1
            if abs(dc) == 1 and dr == direction:
                return True
            return False
        elif kind == 'N':
            if (abs(dr), abs(dc)) in [(2, 1), (1, 2)]:
                return True
            return False
        elif kind == 'B':
            if abs(dr) == abs(dc) and self.clear_path(from_row, from_col, to_row, to_col):
                return True
            return False
        elif kind == 'R':
            if (dr == 0 or dc == 0) and self.clear_path(from_row, from_col, to_row, to_col):
                return True
            return False
        elif kind == 'Q':
            if ((dr == 0 or dc == 0) or abs(dr) == abs(dc)) and self.clear_path(from_row, from_col, to_row, to_col):
                return True
            return False
        elif kind == 'K':
            if max(abs(dr), abs(dc)) == 1:
                return True
            return False
        return False

    def make_move(self, from_row, from_col, to_row, to_col):
        code = self.board[from_row][from_col]
        target = self.board[to_row][to_col]
        color = code[0]
        opp_color = 'b' if color == 'w' else 'w'
        kind = code[1]
        move = (from_row, from_col, to_row, to_col, code, target, self.en_passant_target, dict(self.castling_rights), self.halfmove_clock)
        self.move_history.append(move)
        self.halfmove_clock = 0 if (kind == 'P' or target) else self.halfmove_clock + 1

        # Castling
        if kind == 'K' and abs(to_col - from_col) == 2:
            row = from_row
            if to_col == 6:  # kingside
                self.board[row][4] = None
                self.board[row][6] = color + 'K'
                self.board[row][7] = None
                self.board[row][5] = color + 'R'
                king_id = self.piece_ids.pop((row, 4))
                rook_id = self.piece_ids.pop((row, 7))
                self.piece_ids[(row, 6)] = king_id
                self.piece_ids[(row, 5)] = rook_id
                self.canvas.coords(king_id, 6 * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2)
                self.canvas.coords(rook_id, 5 * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2)
            else:  # queenside
                self.board[row][4] = None
                self.board[row][2] = color + 'K'
                self.board[row][0] = None
                self.board[row][3] = color + 'R'
                king_id = self.piece_ids.pop((row, 4))
                rook_id = self.piece_ids.pop((row, 0))
                self.piece_ids[(row, 2)] = king_id
                self.piece_ids[(row, 3)] = rook_id
                self.canvas.coords(king_id, 2 * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2)
                self.canvas.coords(rook_id, 3 * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2)
            self.castling_rights[color + 'K'] = False
            self.castling_rights[color + 'Q'] = False
            self.en_passant_target = None
            self.clear_shadow_and_lines()
            return

        # En passant
        if kind == 'P' and (to_row, to_col) == self.en_passant_target:
            if color == 'w':
                captured_row = to_row + 1
            else:
                captured_row = to_row - 1
            self.board[captured_row][to_col] = None
            if (captured_row, to_col) in self.piece_ids:
                self.canvas.delete(self.piece_ids[(captured_row, to_col)])
                del self.piece_ids[(captured_row, to_col)]

        # Update castling rights
        if code == 'wK':
            self.castling_rights['wK'] = False
            self.castling_rights['wQ'] = False
        if code == 'bK':
            self.castling_rights['bK'] = False
            self.castling_rights['bQ'] = False
        if code == 'wR':
            if from_row == 7 and from_col == 0:
                self.castling_rights['wQ'] = False
            if from_row == 7 and from_col == 7:
                self.castling_rights['wK'] = False
        if code == 'bR':
            if from_row == 0 and from_col == 0:
                self.castling_rights['bQ'] = False
            if from_row == 0 and from_col == 7:
                self.castling_rights['bK'] = False

        # Set en_passant target
        if kind == 'P' and abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, from_col)
        else:
            self.en_passant_target = None

        # Remove captured piece from canvas
        if (to_row, to_col) in self.piece_ids:
            self.canvas.delete(self.piece_ids[(to_row, to_col)])
            del self.piece_ids[(to_row, to_col)]
        # Move piece on canvas
        piece_id = self.piece_ids.pop((from_row, from_col))
        self.piece_ids[(to_row, to_col)] = piece_id
        x = to_col * self.square_size + self.square_size // 2
        y = to_row * self.square_size + self.square_size // 2
        self.canvas.coords(piece_id, x, y)
        # Update board
        self.board[to_row][to_col] = code
        self.board[from_row][from_col] = None

        # Pawn promotion (default: Queen)
        if kind == 'P' and (to_row == 0 or to_row == 7):
            color_name = 'white' if color == 'w' else 'black'
            self.board[to_row][to_col] = color + 'Q'
            self.canvas.itemconfig(piece_id, text=PIECES[color_name]['Q'], fill=PIECE_COLORS[color_name])

        self.clear_shadow_and_lines()

        # Check for endgame
        if self.is_checkmate():
            self.mark_king_in_checkmate()
            self.end_game(f"Checkmate! {self.players[self.current_player_idx].name} wins!")
        elif self.is_stalemate():
            self.end_game("Stalemate! Draw.")
        elif self.is_draw():
            self.end_game("Draw!")

    def mark_king_in_checkmate(self):
        # Draw a red circle around the checkmated king
        color = 'w' if self.current_player_idx == 0 else 'b'
        king_pos = None
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == color + 'K':
                    king_pos = (r, c)
        if king_pos and king_pos in self.piece_ids:
            x = king_pos[1] * self.square_size + self.square_size // 2
            y = king_pos[0] * self.square_size + self.square_size // 2
            radius = self.square_size // 2 - 4
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                outline="red", width=3, tags="checkmate_mark"
            )

    def next_turn(self):
        self.current_player_idx = 1 - self.current_player_idx
        self.status_label.config(text=self.status_text())

    def status_text(self):
        return f"Turn: {self.players[self.current_player_idx].name} ({'White' if self.current_player_idx == 0 else 'Black'})"

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{int(m):02}:{int(s):02}"

    def update_timer(self):
        if self.game_over:
            return
        self.timers[self.current_player_idx] -= 1
        for i, label in enumerate(self.timer_labels):
            label.config(text=f"{self.players[i].name} Time: {self.format_time(self.timers[i])}")
        if self.timers[self.current_player_idx] <= 0:
            self.end_game(f"Time out! {self.players[1 - self.current_player_idx].name} wins!")
            return
        self.root.after(1000, self.update_timer)

    def is_checkmate(self):
        # Check if current player's king is in check and has no legal moves or protection
        color = 'w' if self.current_player_idx == 0 else 'b'
        opp_color = 'b' if color == 'w' else 'w'
        king_pos = None
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == color + 'K':
                    king_pos = (r, c)
        if not king_pos:
            return True  # King is missing (should not happen)
        if not self.square_attacked(king_pos[0], king_pos[1], opp_color):
            return False
        # Check if any legal move exists for king or any piece to protect
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                code = self.board[r][c]
                if code and code[0] == color:
                    for rr in range(BOARD_SIZE):
                        for cc in range(BOARD_SIZE):
                            if self.is_valid_move(r, c, rr, cc):
                                # Try move and see if king is still in check
                                backup = [row[:] for row in self.board]
                                move_code = self.board[r][c]
                                move_target = self.board[rr][cc]
                                self.board[rr][cc] = move_code
                                self.board[r][c] = None
                                king_pos2 = (rr, cc) if move_code[1] == 'K' else king_pos
                                in_check = self.square_attacked(king_pos2[0], king_pos2[1], opp_color)
                                self.board = [row[:] for row in backup]
                                if not in_check:
                                    return False
        return True

    def is_stalemate(self):
        # Stalemate: not in check, but no legal moves
        color = 'w' if self.current_player_idx == 0 else 'b'
        opp_color = 'b' if color == 'w' else 'w'
        king_pos = None
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == color + 'K':
                    king_pos = (r, c)
        if not king_pos:
            return False
        if self.square_attacked(king_pos[0], king_pos[1], opp_color):
            return False
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                code = self.board[r][c]
                if code and code[0] == color:
                    for rr in range(BOARD_SIZE):
                        for cc in range(BOARD_SIZE):
                            if self.is_valid_move(r, c, rr, cc):
                                # Try move and see if king is in check
                                backup = [row[:] for row in self.board]
                                move_code = self.board[r][c]
                                move_target = self.board[rr][cc]
                                self.board[rr][cc] = move_code
                                self.board[r][c] = None
                                king_pos2 = (rr, cc) if move_code[1] == 'K' else king_pos
                                in_check = self.square_attacked(king_pos2[0], king_pos2[1], opp_color)
                                self.board = [row[:] for row in backup]
                                if not in_check:
                                    return False
        return True

    def is_draw(self):
        # 50-move rule
        if self.halfmove_clock >= 100:
            return True
        # Insufficient material
        pieces = []
        for row in self.board:
            for code in row:
                if code:
                    pieces.append(code[1])
        if all(p in ('K', 'N', 'B') for p in pieces):
            if pieces.count('N') <= 2 and pieces.count('B') <= 2:
                return True
        # TODO: Threefold repetition (not implemented)
        return False

    def end_game(self, message):
        self.game_over = True
        messagebox.showinfo("Game Over", message)
        self.players[self.current_player_idx].score += 1
        self.players[0].games_played += 1
        self.players[1].games_played += 1

    def check_ai_move(self):
        if self.game_over:
            return
        if self.players[self.current_player_idx].is_computer:
            self.ai_thinking = True
            self.status_label.config(text=f"{self.players[self.current_player_idx].name} (Computer) is thinking...")
            self.root.after(100, self.do_ai_move)
        else:
            self.ai_thinking = False

    def do_ai_move(self):
        # Run AI in a thread to avoid freezing GUI
        def ai_thread():
            # Use minimax with alpha-beta pruning
            color = 'w' if self.current_player_idx == 0 else 'b'
            # For difficulty, you can increase self.ai_depth
            _, move = minimax(self, [row[:] for row in self.board], self.en_passant_target, dict(self.castling_rights), self.ai_depth, -float('inf'), float('inf'), True, color, color)
            if move is None:
                # No move (should be checkmate or stalemate)
                return
            r1, c1, r2, c2 = move
            # Make move on main thread
            self.root.after(100, lambda: self._do_ai_move_on_main_thread(r1, c1, r2, c2))
        threading.Thread(target=ai_thread, daemon=True).start()

    def _do_ai_move_on_main_thread(self, r1, c1, r2, c2):
        if self.game_over:
            return
        self.make_move(r1, c1, r2, c2)
        self.next_turn()
        self.ai_thinking = False
        self.root.after(100, self.check_ai_move)

def get_player_info(root, player_num):
    if player_num == 2:
        # Ask if player 2 is computer
        is_computer = messagebox.askyesno("Player 2", "Do you want to play against the computer?")
        if is_computer:
            return Player("Computer", 0, is_computer=True)
    name = simpledialog.askstring("Player Info", f"Enter name for Player {player_num}:")
    age = simpledialog.askinteger("Player Info", f"Enter age for Player {player_num}:")
    return Player(name or f"Player{player_num}", age or 0)

def get_time_setting(root):
    time = simpledialog.askinteger("Game Time", "Enter time per player (minutes):", minvalue=1, maxvalue=180)
    return time or DEFAULT_TIME_MINUTES

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess Game")
    player1 = get_player_info(root, 1)
    player2 = get_player_info(root, 2)
    time_minutes = get_time_setting(root)
    game = ChessGame(root, player1, player2, time_minutes)
    root.mainloop()