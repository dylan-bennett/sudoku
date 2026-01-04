class Solver:
    def __init__(self, board):
        self.board = board

    def backtrack(self):
        # Get all empty cells and couple them with 0 (for the index of that Cell's candidate that we're trying)
        # [[Cell, 0], [Cell, 0], ...]

        # Shuffle the list

        # Use an index to keep track of which cell we're on

        # Go through the empty cells via the index
            # Get its candidate at the given index
                # Check if we can place the candidate here (i.e., check the row, col, box)

                # If yes, place it and move on to the next cell

                # If no, increase the index by 1 (up to board.size)

            # If no candidate could be placed:
            # - reset this cell's candidate index back to 0
            # - go back to the previous cell
            # - remove the symbol from the cell
            # - try its next candidate

        # If the cell index is 0, then we failed
        # If the cell index is at board.size * board.size, then we succeeded (you can probably just check if it's not 0)