from sudoku.engines.solver import Solver


class Reducer:
    """
    Reducer class for minimizing (reducing) filled Sudoku puzzles by testing
    removability of filled cells while preserving uniqueness.
    """

    def __init__(self, board):
        """
        Initialize the Reducer.

        Args:
            board (Board): The Sudoku board to reduce.
        """
        self.board = board

    def reduce_cell(self, cell):
        """
        Attempts to remove the symbol from the specified filled cell
        while ensuring that the board retains a unique solution.

        Approach:
            - For each possible candidate value that could be placed in the cell,
              create a new board with that candidate instead of the original symbol.
            - Try solving the modified board. If it is solvable, the cell's removal
              would admit more than one solution, so return False (did not remove).
            - If no candidate leads to a solvable board, it's safe to remove
              the symbol; set cell.symbol to None and return True.

        Args:
            cell (Cell): The cell whose symbol is to be considered for removal.

        Returns:
            bool: True if the symbol was removed, False if not.
        """
        # If the cell is already empty then it cannot be reduced, so return False
        if cell.symbol is None:
            return False

        # Get all the candidates for the cell
        possible_candidates = self.board.calculate_cell_candidates(cell)

        # Go through each possible candidate
        for possible_candidate in possible_candidates:
            # Make a copy of the board, since we're going to try to solve it
            new_board = self.board.copy()

            # Replace the cell's symbol with our possible candidate
            new_board.cells[cell.row][cell.col].symbol = possible_candidate

            # Attempt to solve the board
            new_solver = Solver(new_board)
            solved = new_solver.solve()

            # If it can be solved, then that means removing this symbol will lead to a
            # non-unique solution. So, abort.
            if solved:
                return False

        # We went through all possible candidates and all of them lead to unsolvable
        # boards. That means that we can safely remove the symbol from this cell.
        cell.symbol = None
        return True
