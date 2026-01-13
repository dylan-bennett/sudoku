from sudoku.board import Board
from sudoku.engines.reducer import Reducer
from sudoku.engines.solver import Solver


class Sudoku:
    def __init__(self, **kwargs):
        # Percentages of filled cells to remain, depending on difficulty level
        self.difficulties_reductions = {
            "easy": 0.37,
            "medium": 0.33,
            "hard": 0.28,
            "expert": 0.25,
        }

        # Attributes of the Sudoku
        self.difficulty = kwargs.get("difficulty", "easy")
        assert self.difficulty in self.difficulties_reductions, (
            "Difficulty must be one of "
            f"{[d for d in self.difficulties_reductions.keys()]}"
        )

        self.symbols = kwargs.get("symbols", range(1, 10))
        self.initial_state = kwargs.get("initial_state", None)
        self.empty_symbol = kwargs.get("empty_symbol", "0")

        # Game and solution boards
        self.solution = None
        self.game = None

        # Create the Sudoku game and solution
        self.create()

    def create(self):
        # Create a new Board and solve it -- that's our solution board
        self.solution = Board(
            symbols=self.symbols,
            initial_state=self.initial_state,
            empty_symbol=self.empty_symbol,
        )
        Solver(self.solution).solve()

        # Make a copy of the solution board, to become our game board
        self.game = self.solution.copy()

        # Calculate the desired number of filled cells to have on the game board
        num_cells_total = self.game.size * self.game.size
        reduction_percentage = self.difficulties_reductions[self.difficulty]
        desired_num_filled_cells = int(reduction_percentage * num_cells_total)

        # Reduce the game board down until we reach the desired number of filled cells
        Reducer(self.game).reduce_n_cells(num_cells_total - desired_num_filled_cells)

    def __repr__(self):
        return (
            f"Game:\n{self.game.ascii}\n"
            f"{'=' * self.game.size * 2}\n"
            f"Soln:\n{self.solution.ascii}"
        )

    def __str__(self):
        return f"Game: {self.game}\nSoln: {self.solution}"
