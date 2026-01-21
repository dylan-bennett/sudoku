# Sudoku Generator & Solver

A comprehensive Python implementation of a Sudoku solver and puzzle generator with support for arbitrary grid sizes and symbol sets. This project demonstrates advanced algorithm design, constraint satisfaction problem solving, and clean object-oriented programming principles.

## Features

### Core Capabilities
- **Sudoku Solver**: Implements iterative backtracking algorithm to solve any valid Sudoku puzzle
- **Puzzle Generator**: Creates unique, solvable Sudoku puzzles at multiple difficulty levels
- **Flexible Grid Support**: Works with arbitrary board sizes (not limited to 9×9)
- **Custom Symbol Sets**: Support for any symbol set (numbers, letters, or custom characters)
- **Puzzle Reduction**: Minimizes puzzle clues while preserving unique solution

### Architecture Highlights
- **Modular Design**: Clean separation of concerns with dedicated classes for Board, Solver, and Reducer
- **Efficient Data Structures**: Fast lookup dictionaries for rows, columns, and boxes
- **Constraint Validation**: Real-time candidate calculation ensuring Sudoku rules compliance
- **Visual Output**: ASCII art representation for easy visualization

## Project Structure

```
sudoku/
├── sudoku/
│   ├── board.py          # Board and Cell classes with grid management
│   ├── sudoku.py         # High-level Sudoku puzzle generator
│   ├── utils.py          # Utility functions
│   └── engines/
│       ├── solver.py     # Backtracking solver implementation
│       └── reducer.py    # Puzzle reduction algorithm
├── tests/                # Comprehensive test suite
└── main.py              # Example usage
```

## Installation

```bash
# Clone the repository
git clone https://github.com/dylan-bennett/sudoku.git
cd sudoku

# Install dependencies (if any)
# Python 3.7+ is required
```

## Usage

### Basic Example

```python
from sudoku import Sudoku

# Create a new Sudoku game with solution
sudoku = Sudoku()

# Display the game and solution
print(sudoku.ascii)
print(sudoku)
```

```bash
Game:
 - - - - - - - - -
|  3  |     |9 1  |

|6    |  9 5|3   8|

|    8|  4  |  6  |
 - - - - - - - - -
|     |  6  |     |

|     |    3|7 9  |

|7 1 3|  2 4|8    |
 - - - - - - - - -
|     |     |    4|

|2 8  |     |  3 5|

|     |2    |1 7  |
 - - - - - - - - -
==================
Soln:
 - - - - - - - - -
|5 3 4|6 7 8|9 1 2|

|6 7 2|1 9 5|3 4 8|

|1 9 8|3 4 2|5 6 7|
 - - - - - - - - -
|8 5 9|7 6 1|4 2 3|

|4 2 6|8 5 3|7 9 1|

|7 1 3|9 2 4|8 5 6|
 - - - - - - - - -
|9 6 1|5 3 7|2 8 4|

|2 8 7|4 1 9|6 3 5|

|3 4 5|2 8 6|1 7 9|
 - - - - - - - - -
Game: 030000910600095308008040060000060000000003790713024800000000004280000035000200170
Soln: 534678912672195348198342567859761423426853791713924856961537284287419635345286179
```

### Advanced Example

```python
from sudoku import Sudoku

# Create a new Sudoku game with solution
sudoku = Sudoku(symbols="ABCDEF", difficulty="hard", empty_symbol="x")

# Display the game and solution
print(sudoku.ascii)
print(sudoku)
```

```bash
Game:
 - - - - - -
|   |  A|F  |

|A  |F  |   |

|   |  D|   |
 - - - - - -
|   |   |D  |

|  C|   |A E|

|E  |   |  C|
 - - - - - -
============
Soln:
 - - - - - -
|D E|C A|F B|

|A B|F E|C D|

|C F|B D|E A|
 - - - - - -
|B A|E C|D F|

|F C|D B|A E|

|E D|A F|B C|
 - - - - - -
Game: xxxxxxDxCExxxxxxxExBxxDxEAxFxxFxxxxx
Soln: AEFBCDDFCEABBCADFECBEADFEADFBCFDBCEA
```

## Algorithms

### Backtracking Solver
The solver uses an iterative depth-first search approach:
- Calculates valid candidates for each empty cell based on Sudoku constraints
- Systematically tries candidates and backtracks when no valid solution exists
- Optimized with candidate pre-computation and efficient constraint checking

### Puzzle Generator
Puzzle generation follows a two-phase approach:
1. **Solution Generation**: Creates a complete, valid Sudoku solution
2. **Puzzle Reduction**: Removes cells one-by-one, ensuring the puzzle maintains a unique solution

### Unique Solution Guarantee
The reducer tests each cell removal by attempting to solve the puzzle with alternative candidates. If multiple solutions exist, the cell is kept; otherwise, it's safely removed.

## Technical Details

### Data Structures
- **Cells**: Individual cells track their row, column, box, symbol, and candidates
- **Lookup Dictionaries**: Fast O(1) access to all cells in a row, column, or box
- **Dynamic Box Calculation**: Automatically determines optimal box dimensions based on the number of symbols

### Constraint Validation
Each cell's valid candidates are computed by eliminating symbols already present in:
- The same row
- The same column
- The same box (subgrid)

## Testing

The project includes a comprehensive test suite covering:
- Board initialization and state management
- Cell candidate calculation
- Solver correctness
- Reducer functionality
- Edge cases and validation

Run tests with your preferred test runner (pytest, unittest, etc.).

## Design Principles

- **Extensibility**: Easy to add new solving strategies or puzzle generation algorithms
- **Testability**: Clean interfaces and modular design enable thorough testing
- **Documentation**: Comprehensive docstrings explaining algorithms and implementation details
- **Code Quality**: Follows PEP 8 style guidelines with type hints where appropriate

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## License

See [LICENSE](LICENSE) file for details.

## Acknowledgments

I want to give a huge shout out to [Sudoku Wiki by Andrew Stuart](https://www.sudokuwiki.org/Sudoku.htm). His site conains a wealth of information about Sudoku, and especially about solving algorithms.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
