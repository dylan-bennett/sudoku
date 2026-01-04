import random


class Solver:
    def __init__(self, board):
        self.board = board

    def is_candidate_valid(self, candidate, cell):
        # Get the board's rows, cols, and boxes that align with our cell
        # See if any of their symbols are the candidate
        pass

    def solve_backtrack(self):
        # Get all empty cells and couple them with 0 (for the index of that Cell's candidate that we're trying)
        # [[Cell, 0], [Cell, 0], ...]
        empty_cells = [
            [cell, 0] for row in self.board.cells for cell in row if cell.symbol is None
        ]

        # Calculate the length of the list
        num_empty_cells = len(empty_cells)

        # If we have no empty cells, then we're solved
        if num_empty_cells == 0:
            return True

        # Shuffle the list
        random.shuffle(empty_cells)

        # Use an index to keep track of which cell we're on
        cell_index = 0

        # Do a depth-first search through the cells in an attempt to fill them
        while True:
            # If we're past the last cell then we've solved the board.
            # If we're below 0 then we cannot solve the board.
            # Either way, we're done.
            if cell_index >= num_empty_cells or cell_index < 0:
                break

            # Grab the current cell
            cell, cand_index = empty_cells[cell_index]

            # Calculate the number of candidates in this cell
            num_candidates = len(cell.candidates)

            # If this cell is filled, then that means we're backtracking.
            # Empty the cell and move its candidate index forward by 1
            if cell.symbol is not None:
                cell.symbol = None
                cand_index += 1

            # Flag for whether the cell's valid candidate was found
            cand_found = False

            # Run through the cell's candidates, potentially jumping into the middle of a candidate list
            while True:
                # If our candidate index is beyond the number of candidates, then no candidate is valid
                if cand_index >= num_candidates:
                    break

                # Get its candidate at the given index
                candidate = cell.candidates[cand_index]

                # Check if we can place the candidate here (i.e., check the row, col, box)
                cand_valid = self.is_candidate_valid(candidate, cell)

                # If yes, place it, mark the index of the current candidate, and move on to the next cell
                if cand_valid:
                    cand_found = True
                    cell.symbol = candidate
                    empty_cells[cell_index][1] = cand_index
                    cell_index += 1
                    break

                # If no, move on to the next candidate
                else:
                    cand_index += 1

            # No candidate could be placed in the current cell, so we're going to backtrack.
            # Reset the current cell's candidate index, and go to the previous cell in the list
            if cand_found is False:
                empty_cells[cell_index][1] = 0
                cell_index -= 1

        # If the last empty cell is filled, then we succeeded
        return empty_cells[-1][0].symbol is not None
