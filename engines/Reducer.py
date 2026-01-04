class Reducer:
    def __init__(self, board):
        self.board = board



    def reduce_cell(self, cell):
        # Get all the candidates for the cell
        possible_candidates = self.calculate_cell_candidates(cell)

        # Go through each possible candidate
        for possible_candidate in possible_candidates:
            # Make a copy of the board, since we're going to try to solve it

            # Replace the cell's symbol with our possible candidate

            # Attempt to solve the board

            # If it can be solved, then that means removing this symbol will lead to a non-unique solution. So, abort.
            pass

        # We went through all possible candidates and all of them lead to unsolvable boards. That means that we can safely remove the symbol from this cell.
