import tkinter as tk
from tkinter import messagebox

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.current_player = "white"
        self.selected_piece = None
        self.last_move = None  # For en passant
        self.kings_moved = {"white": False, "black": False}  # For castling
        self.rooks_moved = {
            "white": {"left": False, "right": False},
            "black": {"left": False, "right": False}
        }
        self.create_board()
        self.initialize_pieces()

    def create_board(self):
        self.squares = {}
        self.buttons = {}
        
        for row in range(8):
            for col in range(8):
                color = "#FFFFFF" if (row + col) % 2 == 0 else "#808080"
                frame = tk.Frame(
                    self.root,
                    width=60,
                    height=60,
                    bg=color
                )
                frame.grid(row=row, column=col)
                frame.grid_propagate(False)
                
                button = tk.Button(
                    frame,
                    bg=color,
                    bd=0,
                    relief="flat",
                    command=lambda r=row, c=col: self.square_clicked(r, c)
                )
                button.place(relwidth=1, relheight=1)
                
                self.buttons[(row, col)] = button
                self.squares[(row, col)] = None

    def initialize_pieces(self):
        # Initialize pawns
        for col in range(8):
            self.squares[(1, col)] = ("black", "pawn")
            self.squares[(6, col)] = ("white", "pawn")
        
        # Initialize other pieces
        piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for col in range(8):
            self.squares[(0, col)] = ("black", piece_order[col])
            self.squares[(7, col)] = ("white", piece_order[col])
        
        self.update_display()

    def get_king_position(self, color):
        for pos, piece in self.squares.items():
            if piece and piece[0] == color and piece[1] == "king":
                return pos
        return None

    def is_check(self, color):
        king_pos = self.get_king_position(color)
        opponent = "black" if color == "white" else "white"
        
        for start_pos, piece in self.squares.items():
            if piece and piece[0] == opponent:
                if self.is_valid_move(start_pos, king_pos, check_check=False):
                    return True
        return False

    def is_checkmate(self, color):
        if not self.is_check(color):
            return False
            
        # Try all possible moves for all pieces
        for start_pos, piece in self.squares.items():
            if piece and piece[0] == color:
                for end_pos in self.squares.keys():
                    if self.is_valid_move(start_pos, end_pos, check_check=True):
                        # If any valid move exists, it's not checkmate
                        return False
        return True

    def can_castle(self, color, side):
        if self.kings_moved[color]:
            return False
            
        row = 7 if color == "white" else 0
        if side == "left":
            if self.rooks_moved[color]["left"]:
                return False
            # Check if path is clear for queenside castling
            return (all(self.squares[(row, col)] is None for col in [1, 2, 3]) and
                   not any(self.is_square_under_attack(color, (row, col)) for col in [2, 3, 4]))
        else:  # right side
            if self.rooks_moved[color]["right"]:
                return False
            # Check if path is clear for kingside castling
            return (all(self.squares[(row, col)] is None for col in [5, 6]) and
                   not any(self.is_square_under_attack(color, (row, col)) for col in [4, 5, 6]))

    def is_square_under_attack(self, color, pos):
        opponent = "black" if color == "white" else "white"
        for start_pos, piece in self.squares.items():
            if piece and piece[0] == opponent:
                if self.is_valid_move(start_pos, pos, check_check=False):
                    return True
        return False

    def try_move(self, start, end):
        # Make temporary move
        temp_end = self.squares[end]
        temp_start = self.squares[start]
        self.squares[end] = self.squares[start]
        self.squares[start] = None
        
        # Check if king is in check after move
        in_check = self.is_check(self.current_player)
        
        # Undo move
        self.squares[start] = temp_start
        self.squares[end] = temp_end
        
        return not in_check

    def promote_pawn(self, pos):
        color = self.squares[pos][0]
        
        # Create promotion window
        promotion_window = tk.Toplevel(self.root)
        promotion_window.title("Pawn Promotion")
        
        def choose_piece(piece_type):
            self.squares[pos] = (color, piece_type)
            self.update_display()
            promotion_window.destroy()
        
        pieces = ["queen", "rook", "bishop", "knight"]
        for i, piece in enumerate(pieces):
            tk.Button(promotion_window, 
                     text=piece.capitalize(), 
                     command=lambda p=piece: choose_piece(p)).grid(row=0, column=i)

    def handle_castling(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        # Kingside castling
        if end_col - start_col == 2:
            rook_start = (start_row, 7)
            rook_end = (start_row, 5)
        # Queenside castling
        else:
            rook_start = (start_row, 0)
            rook_end = (start_row, 3)
            
        self.squares[rook_end] = self.squares[rook_start]
        self.squares[rook_start] = None

    def square_clicked(self, row, col):
        if self.selected_piece is None:
            # Select piece
            if self.squares[(row, col)] and self.squares[(row, col)][0] == self.current_player:
                self.selected_piece = (row, col)
                self.buttons[(row, col)].configure(bg="#FFFF00")  # Highlight selected piece
        else:
            old_row, old_col = self.selected_piece
            # Try to move piece
            if self.is_valid_move(self.selected_piece, (row, col)):
                piece_type = self.squares[self.selected_piece][1]
                
                # Handle castling
                if piece_type == "king" and abs(col - old_col) == 2:
                    self.handle_castling(self.selected_piece, (row, col))
                
                # Make the move
                self.squares[(row, col)] = self.squares[self.selected_piece]
                self.squares[self.selected_piece] = None
                
                # Handle pawn promotion
                if piece_type == "pawn" and (row == 0 or row == 7):
                    self.promote_pawn((row, col))
                
                # Update castling rights
                if piece_type == "king":
                    self.kings_moved[self.current_player] = True
                elif piece_type == "rook":
                    if old_col == 0:
                        self.rooks_moved[self.current_player]["left"] = True
                    elif old_col == 7:
                        self.rooks_moved[self.current_player]["right"] = True
                
                # Store last move for en passant
                self.last_move = (self.selected_piece, (row, col), piece_type)
                
                # Switch players
                self.current_player = "black" if self.current_player == "white" else "white"
                
                # Check for checkmate
                if self.is_checkmate(self.current_player):
                    winner = "White" if self.current_player == "black" else "Black"
                    messagebox.showinfo("Game Over", f"{winner} wins by checkmate!")
                elif self.is_check(self.current_player):
                    messagebox.showinfo("Check", f"{self.current_player.capitalize()} is in check!")
                
                # Reset selection
                self.buttons[self.selected_piece].configure(
                    bg="#FFFFFF" if (old_row + old_col) % 2 == 0 else "#808080"
                )
                self.selected_piece = None
                
                self.update_display()
            elif self.squares[(row, col)] and self.squares[(row, col)][0] == self.current_player:
                # Select new piece
                if self.selected_piece:
                    old_row, old_col = self.selected_piece
                    self.buttons[(old_row, old_col)].configure(
                        bg="#FFFFFF" if (old_row + old_col) % 2 == 0 else "#808080"
                    )
                self.selected_piece = (row, col)
                self.buttons[(row, col)].configure(bg="#FFFF00")

    def is_valid_move(self, start, end, check_check=True):
        if start == end:
            return False
            
        start_row, start_col = start
        end_row, end_col = end
        
        if self.squares[end] and self.squares[end][0] == self.current_player:
            return False
            
        piece_color, piece_type = self.squares[start]
        
        # Check if move would put/leave king in check
        if check_check and not self.try_move(start, end):
            return False
        
        # Pawn movement
        if piece_type == "pawn":
            direction = 1 if piece_color == "black" else -1
            
            # Regular move forward
            if end_col == start_col and end_row == start_row + direction:
                return not self.squares[end]
                
            # Initial two-square move
            if ((piece_color == "black" and start_row == 1) or 
                (piece_color == "white" and start_row == 6)):
                if (end_col == start_col and 
                    end_row == start_row + 2 * direction and 
                    not self.squares[end] and 
                    not self.squares[(start_row + direction, start_col)]):
                    return True
                    
            # Regular capture
            if (abs(end_col - start_col) == 1 and 
                end_row == start_row + direction and 
                self.squares[end] and 
                self.squares[end][0] != piece_color):
                return True
                
            # En passant
            if (self.last_move and 
                self.last_move[2] == "pawn" and 
                abs(self.last_move[0][0] - self.last_move[1][0]) == 2 and
                self.last_move[1][1] == end_col and
                self.last_move[1][0] == start_row and
                abs(end_col - start_col) == 1 and
                end_row == start_row + direction):
                # Remove captured pawn
                self.squares[self.last_move[1]] = None
                return True
                
            return False
            
        # Rook movement
        elif piece_type == "rook":
            if not (start_row == end_row or start_col == end_col):
                return False
            return self.is_path_clear(start, end)
            
        # Knight movement
        elif piece_type == "knight":
            row_diff = abs(end_row - start_row)
            col_diff = abs(end_col - start_col)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
            
        # Bishop movement
        elif piece_type == "bishop":
            if abs(end_row - start_row) != abs(end_col - start_col):
                return False
            return self.is_path_clear(start, end)
            
        # Queen movement
        elif piece_type == "queen":
            if not (start_row == end_row or 
                   start_col == end_col or 
                   abs(end_row - start_row) == abs(end_col - start_col)):
                return False
            return self.is_path_clear(start, end)
            
        # King movement
        elif piece_type == "king":
            row_diff = abs(end_row - start_row)
            col_diff = abs(end_col - start_col)
            
            # Normal king move
            if row_diff <= 1 and col_diff <= 1:
                return True
                
            # Castling
            if (row_diff == 0 and col_diff == 2 and 
                not self.kings_moved[piece_color] and
                not self.is_check(piece_color)):
                # Kingside castling
                if end_col > start_col:
                    return self.can_castle(piece_color, "right")
                # Queenside castling
                else:
                    return self.can_castle(piece_color, "left")
                    
            return False
            
        return False

    def is_path_clear(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        row_step = 0 if start_row == end_row else (end_row - start_row) // abs(end_row - start_row)
        col_step = 0 if start_col == end_col else (end_col - start_col) // abs(end_col - start_col)
        
        current_row, current_col = start_row + row_step, start_col + col_step
        while (current_row, current_col) != (end_row, end_col):
            if self.squares[(current_row, current_col)] is not None:
                return False
            current_row += row_step
            current_col += col_step
        return True

    def update_display(self):
        piece_symbols = {
            ("white", "pawn"): "♙",
            ("white", "rook"): "♖",
            ("white", "knight"): "♘",
            ("white", "bishop"): "♗",
            ("white", "queen"): "♕",
            ("white", "king"): "♔",
            ("black", "pawn"): "♟",
            ("black", "rook"): "♜",
            ("black", "knight"): "♞",
            ("black", "bishop"): "♝",
            ("black", "queen"): "♛",
            ("black", "king"): "♚"
        }
        
        for pos, piece in self.squares.items():
            button = self.buttons[pos]
            row, col = pos
            
            # Update piece symbols
            if piece:
                button.config(text=piece_symbols[(piece.color, piece.type)])
            else:
                button.config(text="")
            
            # Set square colors
            if (row + col) % 2 == 0:
                bg_color = "#FFFFFF"  # White squares
            else:
                bg_color = "#A0522D"  # Brown squares
                
            # Highlight selected piece
            if self.selected_piece and pos == self.selected_piece:
                bg_color = "#90EE90"  # Light green for selected
            
            # Highlight last move
            if hasattr(self, 'last_move') and pos in [self.last_move[0], self.last_move[1]]:
                bg_color = "#FFD700"  # Gold for last move
                
            # Highlight check
            if self.king_in_check and piece and piece.type == "king" and piece.color == self.current_turn:
                bg_color = "#FF6B6B"  # Red for check
                
            button.config(bg=bg_color)
            
            # Enable/disable buttons based on turn
            if piece and piece.color == self.current_turn and not self.game_over:
                button.config(state="normal")
            else:
                button.config(state="disabled" if self.game_over else "normal")
        
        # Update game status label if it exists
        if hasattr(self, 'status_label'):
            if self.game_over:
                status = "Game Over! "
                status += "Checkmate!" if self.checkmate else "Stalemate!"
            else:
                status = f"{self.current_turn.capitalize()}'s turn"
                if self.king_in_check:
                    status += " (Check!)"
            self.status_label.config(text=status)