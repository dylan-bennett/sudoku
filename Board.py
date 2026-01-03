from Cell import Cell
from utils import closest_factors


class Board:
    """
    Represents a Sudoku board with a specified set of symbols.

    Attributes:
        symbols (list[str]): Sorted list of string symbols used on the board.
        size (int): Number of symbols/ size of the grid (board is size x size).
        num_bands (int): Number of ros of boxes (height of boxes).
        num_stacks (int): Number of columns of boxes (width of boxes).
        cells (list[list[Cell]]): 2D list of Cell objects representing the
            board grid.
    """

    def __init__(self, symbols):
        """
        Initializes a Board with the given symbols.

        Args:
            symbols (iterable): Symbols used for the board.
                Can be numbers or characters.

        The board will be created as a square grid (size x size).
        The symbols are stringified and sorted. The number of bands (boxes per
        column) and stacks (boxes per row) are chosen to be as close as
        possible in size, using closest_factors. Each cell is initialized with
        all possible candidate symbols.
        """
        # The list of symbols, stringified and sorted
        self.symbols = sorted([str(symbol) for symbol in symbols])

        # The side length of the board
        self.size = len(self.symbols)

        # Determine the box configuration (bands and stacks)
        self.num_bands, self.num_stacks = closest_factors(self.size)

        # Create the 2-dimensional list of Cells
        self.cells = [
            [
                Cell(
                    row=row,
                    col=col,
                    box=self.get_box_index(row, col),
                    symbol=None,
                    candidates=self.symbols,
                )
                for col in range(self.size)
            ]
            for row in range(self.size)
        ]

    def get_box_index(self, row, col):
        """
        Compute the box index for a cell at (row, col).

        The boxes are ordered left-to-right within a band (horizontal group of
        boxes), progressing top-to-bottom by bands.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            int: The box index for the given cell.
        """
        return row // self.num_stacks * self.num_stacks + col // self.num_bands

    def __repr__(self):
        """
        Returns:
            str: An ASCII representation of the Sudoku Board, with box borders.

        The grid is displayed with horizontal lines between bands and
        vertical '|' characters between stacks for easy visual separation of
        boxes. Each cell shows its symbol (or blank if None).
        """
        line = ""
        for row, row_of_cells in enumerate(self.cells):
            # Draw the box border above the row, if appropriate
            for col, cell in enumerate(row_of_cells):
                if row == 0 or self.cells[row - 1][col].box != cell.box:
                    line += " -"
                else:
                    line += "  "
            line += "\n"

            # Draw the row's symbols, with vertical box borders if necessary
            for col, cell in enumerate(row_of_cells):
                if col == 0 or self.cells[row][col - 1].box != cell.box:
                    line += f"|{cell}"
                else:
                    line += f" {cell}"
            line += "|\n"
        line += " -" * self.size

        return line

    def __str__(self):
        """
        Returns:
            str: The concatenation of all cell symbols in the board,
            reading left-to-right and top-to-bottom.

        Each empty cell is represented by '0'.
        """
        return "".join(
            "".join(f"{cell.symbol if cell.symbol is not None else 0}" for cell in row)
            for row in self.cells
        )
