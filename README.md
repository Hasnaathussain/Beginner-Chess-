# Python Chess Game

A fully-functional chess game implementation using Python and Tkinter with complete chess rules and graphical interface.

## Features

- Complete chess rules implementation:
  - Standard piece movements for all pieces
  - Pawn promotion
  - Castling (both kingside and queenside)
  - En passant captures
  - Check detection
  - Checkmate detection

- Graphical user interface using Tkinter:
  - Visual chess board with alternating colors
  - Unicode chess pieces
  - Piece highlighting on selection
  - Move validation
  - Turn indicator
  - Game state notifications

## Requirements

- Python 3.x
- Tkinter (usually comes with Python installation)

## Installation

1. Clone the repository or download the source code:
```bash
git clone https://github.com/hasnaathussain/Beginner-Chess-.git
cd python-chess
```

2. Run the game:
```bash
python Beginner-Chess-.py
```

## How to Play

1. The game starts with White's turn
2. Click on a piece to select it
   - Valid piece selections will be highlighted in yellow
3. Click on a destination square to move the selected piece
   - If the move is invalid, the piece will remain selected
   - Click on a different piece of the same color to change selection
4. Special moves:
   - **Castling**: Move the king two squares towards a rook
   - **Pawn Promotion**: Move a pawn to the opposite end of the board
   - **En Passant**: Capture an opponent's pawn that just moved two squares

## Game Rules

### Piece Movements

- **Pawn**: Moves forward one square at a time, can move two squares on first move
  - Captures diagonally
  - Can perform en passant captures
  - Promotes to any piece (except king) when reaching the opposite end

- **Rook**: Moves any number of squares horizontally or vertically

- **Knight**: Moves in L-shape (two squares in one direction, then one square perpendicular)
  - Can jump over other pieces

- **Bishop**: Moves any number of squares diagonally

- **Queen**: Combines rook and bishop movements

- **King**: Moves one square in any direction
  - Can perform castling under specific conditions

### Special Rules

#### Castling
- King moves two squares towards a rook
- Rook moves to the square the king crossed
- Requirements:
  - Neither king nor rook has moved
  - No pieces between king and rook
  - King is not in check
  - King does not pass through check
  - Final king position is not in check

#### En Passant
- Can capture an opponent's pawn that just moved two squares
- Must be performed immediately after the opponent's pawn move

#### Pawn Promotion
- When a pawn reaches the opposite end of the board
- Can be promoted to any piece except a king
- Selection window appears automatically

## Code Structure

- `ChessGame` class: Main game logic
  - Board creation and initialization
  - Move validation
  - Special moves handling
  - Check/checkmate detection
  - Game state management

## Future Improvements

Potential features to be added:
1. Move history/notation
2. Save/load game functionality
3. Time control
4. AI opponent
5. Network multiplayer
6. Stalemate detection
7. Draw by insufficient material
8. Fifty-move rule
9. Threefold repetition rule

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Chess piece Unicode symbols from the [Unicode Character Database](https://www.unicode.org/charts/)
- Inspired by traditional chess rules and mechanics
