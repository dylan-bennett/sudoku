from utils import closest_factors


class Cell:
    """
    Represents a single cell in a Sudoku grid.

    Attributes:
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        box (int): The box index of the cell.
        symbol (optional): The value assigned to the cell
            (e.g., number or letter).
        candidates (optional): A set or list of candidate symbols that the
            cell can take.
    """

    def __init__(self, row, col, box, symbol=None, candidates=None):
        """
        Initializes a Cell object.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            box (int): The box index of the cell.
            symbol (optional): The value assigned to the cell. Default is None.
            candidates (optional): Candidate symbols for the cell. Default is
                None.
        """
        self.row = row
        self.col = col
        self.box = box
        self.symbol = symbol
        self.candidates = candidates

    def __repr__(self):
        """
        Returns a string representation of the Cell object for debugging.

        Returns:
            str: A string containing cell attributes.
        """
        return f"({self.row},{self.col},{self.box},{self.symbol})"

    def __str__(self):
        """
        Returns a user-friendly string representation of the Cell object.

        Returns:
            str: The symbol in the cell, or a space if the cell is empty.
        """
        return f"{self.symbol if self.symbol is not None else ' '}"


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

    Class Attributes:
        rows (dict[int, list[Cell]]): Cells grouped by row index.
        cols (dict[int, list[Cell]]): Cells grouped by column index.
        boxes (dict[int, list[Cell]]): Cells grouped by box index.
    """

    # Dictionaries that will hold the Cell objects for each
    # row, col, and box index
    rows = {}
    cols = {}
    boxes = {}

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

        # Initialize the 2D list of Cell objects
        # and populate row/col/box lookups
        self.cells = []
        for row in range(self.size):
            col_cells = []
            for col in range(self.size):
                # Calculate the box index
                box = row // self.num_stacks * self.num_stacks + col // self.num_bands

                cell = Cell(
                    row=row,
                    col=col,
                    box=box,
                    symbol=None,
                    candidates=self.symbols,
                )
                col_cells.append(cell)

                # Add this Cell to each of our lookup dictionaries
                for d, val in [(self.rows, row), (self.cols, col), (self.boxes, box)]:
                    if val not in d:
                        d[val] = []
                    d[val].append(cell)

            self.cells.append(col_cells)

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
