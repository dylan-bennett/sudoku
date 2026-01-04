import os
import random


class Solver:
    """
    Solver class that provides methods to solve Sudoku puzzles using
    backtracking algorithms.

    Attributes:
        board (Board): The Sudoku Board object.
        DEBUG (bool): Enables step-by-step output if True.
    """

    def __init__(self, board, DEBUG=False):
        """
        Initialize the solver instance.

        Args:
            board (Board): The Sudoku board to solve.
            DEBUG (bool): If True, print detailed progress.
        """
        self.board = board
        self.DEBUG = DEBUG

    def is_candidate_valid(self, candidate, cell):
        """
        Checks if the candidate value can be placed at the specified cell
        without violating Sudoku rules.

        Args:
            candidate (str): The symbol to test.
            cell (Cell): The cell in which to test the candidate.

        Returns:
            bool: True if candidate can be placed, False otherwise.
        """
        # Check row (excluding current cell)
        for cell_to_check in self.board.rows[cell.row]:
            if cell_to_check is not cell and cell_to_check.symbol == candidate:
                return False

        # Check column (excluding current cell)
        for cell_to_check in self.board.cols[cell.col]:
            if cell_to_check is not cell and cell_to_check.symbol == candidate:
                return False

        # Check box (excluding current cell)
        for cell_to_check in self.board.boxes[cell.box]:
            if cell_to_check is not cell and cell_to_check.symbol == candidate:
                return False

        return True

    def solve_backtrack(self):
        """
        Solves the provided Sudoku board using iterative depth-first search
        (backtracking).

        Returns:
            bool: True if the board was solved successfully, False otherwise.

        The method searches for a solution by filling empty cells with
        candidates, backtracking whenever a dead end is reached.
        """
        # Generate a list of all empty cells, each with a mutable candidate index.
        # Structure: [[Cell, candidate_index], ...]
        empty_cells = [
            [cell, 0] for row in self.board.cells for cell in row if cell.symbol is None
        ]

        num_empty_cells = len(empty_cells)

        # No empty cells = board is already solved
        if num_empty_cells == 0:
            return True

        # Randomize cell order for variety in solution paths
        random.shuffle(empty_cells)

        # Track current position in the list of empty cells
        cell_index = 0

        # Enter iterative backtracking loop
        while True:
            # Terminate: either solved (past last cell) or no solution (before start)
            if cell_index >= num_empty_cells or cell_index < 0:
                break

            # Unpack the current cell and the candidate index to try next
            cell, candidate_index = empty_cells[cell_index]
            num_candidates = len(cell.candidates)

            # If cell already filled, this is a backtrack step.
            # Clear it, try next candidate
            if cell.symbol is not None:
                cell.symbol = None
                candidate_index += 1  # Next candidate

            # Whether we found a valid value for this cell yet
            valid_candidate_found = False

            # Try all candidates for this cell (possibly resuming from before)
            while True:
                if candidate_index >= num_candidates:
                    # No candidates remain, must backtrack further
                    break

                candidate = cell.candidates[candidate_index]

                # If debugging, show board and state before trying a candidate
                if self.DEBUG:
                    cell.symbol = candidate
                    print(self.board.ascii)
                    print(
                        "".join(
                            str(cell.symbol) if cell.symbol else "0"
                            for cell, _ in empty_cells
                        )
                    )
                    os.system("cls" if os.name == "nt" else "clear")
                    cell.symbol = None

                # Check Sudoku constraints (row/col/box uniqueness)
                if self.is_candidate_valid(candidate, cell):
                    # Place candidate and move to next empty cell
                    valid_candidate_found = True
                    cell.symbol = candidate
                    empty_cells[cell_index][1] = candidate_index  # Record progress
                    cell_index += 1
                    break  # Proceed to next cell

                # Candidate failed; try next
                candidate_index += 1

            # If no valid candidate was found for this cell, reset and back up
            if not valid_candidate_found:
                empty_cells[cell_index][1] = 0  # Reset candidate index
                cell_index -= 1  # Go back to previous cell

        # If the board is solved, the last cell will be filled.
        return empty_cells[-1][0].symbol is not None
