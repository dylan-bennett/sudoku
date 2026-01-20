import random

from sudoku.utils import closest_factors


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

        # The symbol filling the cell
        self.symbol = symbol

        # The list of potential candidates. Only really used when actively solving a
        # board. Otherwise it stays empty.
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
    A Sudoku board abstraction supporting arbitrary grids and symbol sets.

    This class organizes a grid of Cell objects and provides access to the
    board by row, column, and box groupings. It supports flexible symbol sets,
    customizable empty cell markers, and arbitrary box shapes (for non-9x9 boards).

    Attributes:
        symbols (list[str]): Sorted list of allowed symbols (as strings) for filled
            cells.
        size (int): Board dimension (number of rows/columns; board is size x size).
        num_bands (int): Number of rows per box (height of a Sudoku subgrid).
        num_stacks (int): Number of columns per box (width of a Sudoku subgrid).
        rows (dict[int, list[Cell]]): Maps row index to list of Cell objects in that
            row.
        cols (dict[int, list[Cell]]): Maps column index to list of Cell objects in that
            column.
        boxes (dict[int, list[Cell]]): Maps box index to list of Cell objects in that
            box.
        cells (list[list[Cell]]): 2D list of Cell objects: cells[row][col].
        empty_symbol (str): String symbol used to designate an empty cell.
    """

    def __init__(self, symbols=None, initial_state=None, empty_symbol="0"):
        """
        Initialize a Sudoku Board instance with a set of possible symbols, an optional
        initial state, and a specified symbol marking empty cells.

        Args:
            symbols (iterable, optional): The collection of symbols to use for the
                board's cells. Can be strings or numbers, and will be converted to
                strings, sorted, and used as the allowed set of board symbols. If not
                provided, defaults to the integers 1 through 9.
            initial_state (list or str, optional): Flat sequence of length (size*size)
                representing initial cell symbols to pre-populate the board. Can include
                the empty_symbol to denote an empty cell. If None, board is initialized
                empty.
            empty_symbol (str, optional): Symbol representing an empty cell
                (default: "0"). Must not appear in the list of valid symbols.

        Behavior:
            - The board is always square (size x size), where size = len(symbols).
            - The symbols are stored as sorted strings in self.symbols.
            - The empty_symbol is checked for conflicts in the allowed symbols.
            - self.size: Number of rows/columns.
            - self.num_bands, self.num_stacks: Chosen via closest_factors to best
                factor board size into box shape.
            - Lookup dictionaries (self.rows, self.cols, self.boxes) allow fast access
                to all cells in a unit.
            - Cells are created "empty" (no symbol) initially.
            - If initial_state is provided, cells are populated accordingly (see
                set_initial_state).
        """
        if symbols is None:
            symbols = range(1, 10)

        # Store the allowed symbols as a sorted list of strings.
        self.symbols = sorted([str(symbol) for symbol in symbols])

        # Raise an error if the empty symbol overlaps with any normal board symbol.
        if empty_symbol in self.symbols:
            raise ValueError(
                f"Invalid configuration: The empty symbol '{empty_symbol}' "
                f"must not appear in the symbols list {self.symbols}."
            )

        # Store the empty cell placeholder used during initialization and validation.
        self.empty_symbol = empty_symbol

        # Determine the board size
        self.size = len(self.symbols)

        # Compute the box (subgrid) structure for this size
        self.num_bands, self.num_stacks = closest_factors(self.size)

        # Lookup dictionaries to group cells by row, column, and box
        self.rows = {}
        self.cols = {}
        self.boxes = {}

        # 2D array to hold board cells
        self.cells = []
        self.initialize_cells()

        # Populate cells using the initial state, if provided
        if initial_state:
            self.set_initial_state(initial_state)

    def initialize_cells(self):
        """
        Initializes the internal grid of Cell objects and populates lookup
        dictionaries for rows, columns, and boxes.

        After execution:
            - self.cells will be a 2D list of size (size x size), where each entry is a
                Cell.
            - self.rows, self.cols, self.boxes will provide direct access to all cells
                in each group.
        """
        for row in range(self.size):
            col_cells = []  # List to hold the Cell objects for this row
            for col in range(self.size):
                # Compute the box index this cell belongs to.
                # Boxes are arranged in a rectangular grid with num_bands rows and
                # num_stacks columns.
                box = (row // self.num_stacks) * self.num_stacks + (
                    col // self.num_bands
                )

                # Instantiate a Cell for this position (initially empty, with no symbol
                # or candidates)
                cell = Cell(row=row, col=col, box=box)
                col_cells.append(cell)

                # Add the cell to the row, column, and box lookup dictionaries.
                # These provide efficient group access for solving/validating.
                self.rows.setdefault(row, []).append(cell)
                self.cols.setdefault(col, []).append(cell)
                self.boxes.setdefault(box, []).append(cell)

            # Append the completed row to the board's cell grid
            self.cells.append(col_cells)

    def copy(self):
        """
        Create a deep copy of the board with all cell symbols duplicated.

        Returns:
            Board: A new Board instance with identical structure and cell symbols.
        """
        # Create a new board with the same configuration
        # (no initial_state to avoid validation)
        new_board = Board(symbols=self.symbols, empty_symbol=self.empty_symbol)

        # Copy all cell symbols directly
        for row_idx, row in enumerate(self.cells):
            for col_idx, cell in enumerate(row):
                new_board.cells[row_idx][col_idx].symbol = cell.symbol

        return new_board

    def set_initial_state(self, initial_state):
        """
        Set the initial state of the board by assigning symbols to cells.

        Args:
            initial_state (list or str): A flat sequence of symbols of length size*size.
                Each symbol must be one of the allowed board symbols, or the empty
                symbol for empty cells.

        Raises:
            ValueError: If the length of initial_state doesn't match the number of
                cells, or if any symbol is not a valid board symbol or the empty symbol.

        The function walks through the cells in row-major order and assigns each cell
        its corresponding symbol from initial_state. Cells corresponding to the empty
        symbol are left unassigned (remain empty).
        """
        # Validate initial_state length for proper board shape
        if len(initial_state) != self.size * self.size:
            raise ValueError(
                f"Initial state must have exactly {self.size * self.size} symbols "
                f"(got {len(initial_state)})."
            )

        # Ensure there are no initial symbols other than our list and the empty symbol
        allowed = set(self.symbols) | {self.empty_symbol}
        for i, sym in enumerate(initial_state):
            if sym not in allowed:
                raise ValueError(
                    f"Invalid symbol '{sym}' at index {i} in initial_state; "
                    f"allowed: {self.symbols} or '{self.empty_symbol}' for empty."
                )

        # Go through each cell and set its symbol to the one in the initial state, or
        # None if it's the empty symbol
        state_index = 0
        for row in self.cells:
            for cell in row:
                cell.symbol = (
                    initial_state[state_index]
                    if initial_state[state_index] != self.empty_symbol
                    else None
                )
                state_index += 1

    def seed_empty_board(self):
        """
        Take an empty board and fill in some seed cells.
        This will make solving the board go much faster.
        """
        # Verify that the board is empty. If it's not, abort
        for row in self.cells:
            for cell in row:
                if cell.symbol is not None:
                    return

        # Choose a random column
        column_index = random.randrange(self.size)

        # Shuffle the symbols
        symbols = [s for s in self.symbols]
        random.shuffle(symbols)

        # Place the symbols into all the cells in that column
        for i, cell in enumerate(self.cols[column_index]):
            cell.symbol = symbols[i]

        # Choose a random cell within that column
        cell = random.choice(self.cols[column_index])

        # Get the other cells within our cell's row and box
        remaining_box_cells = [
            c for c in self.boxes[cell.box] if c.row == cell.row and c.col != cell.col
        ]

        # Keep track of the symbols in this row
        used_symbols = [cell.symbol]

        # For each cell , calculate its candidates and choose a random one
        for remaining_cell in remaining_box_cells:
            candidates = list(self.calculate_cell_candidates(remaining_cell))
            remaining_cell.symbol = random.choice(candidates)
            used_symbols.append(remaining_cell.symbol)

        # Get the remaining symbols allowed in that row and shuffle them
        remaining_symbols = [s for s in self.symbols if s not in used_symbols]
        random.shuffle(remaining_symbols)

        # Go through the rest of the row and seed those cells
        for cell in self.rows[cell.row]:
            if cell.symbol is None:
                cell.symbol = remaining_symbols.pop()

    def calculate_cell_candidates(self, cell):
        """
        Calculate and return the set of all valid candidate symbols for a given cell,
        based on Sudoku rules.

        Args:
            cell (Cell): The cell object for which to compute candidates.

        Returns:
            set: A set of symbols that may be placed in this cell without violating
                Sudoku rules (no duplicates in the same row, column, or box).

        Method:
            - Start with all possible board symbols as initial candidates.
            - Remove any symbols present in the same row, column, or box as the cell.
            - The remaining symbols are the valid candidates for this cell.
        """
        # Start with all symbols as possible candidates
        possible_candidates = set(self.symbols)

        # Remove any symbol already present in the same row
        for row_cell in self.rows[cell.row]:
            possible_candidates.discard(row_cell.symbol)

        # Remove any symbol already present in the same column
        for col_cell in self.cols[cell.col]:
            possible_candidates.discard(col_cell.symbol)

        # Remove any symbol already present in the same box
        for box_cell in self.boxes[cell.box]:
            possible_candidates.discard(box_cell.symbol)

        # Return the final set of candidates
        return possible_candidates

    def calculate_all_empty_cell_candidates(self):
        """
        For every empty cell on the board (i.e., any cell with symbol == None),
        compute and assign its list of possible candidates.

        This method updates each empty cell's .candidates attribute with a list
        of valid symbols -- all values that could legally be placed in that cell
        according to Sudoku rules (no duplicate values in the same row, column,
        or box).
        """
        for row in self.cells:
            for cell in row:
                if cell.symbol is None:
                    # Populate this empty cell's candidates with valid options
                    cell.candidates = list(self.calculate_cell_candidates(cell))

    @property
    def ascii(self):
        """
        Returns:
            str: An ASCII art representation of the Sudoku board, displaying cell values
            within box and grid borders to visually distinguish each box boundary and
            cell.

        The output shows row and column groupings separated by visible lines. Empty
        cells are displayed using their string representation as defined in the Cell
        class.
        """
        lines = []
        for row, row_of_cells in enumerate(self.cells):
            # Build border line
            border_line = []
            for col, cell in enumerate(row_of_cells):
                if row == 0 or self.cells[row - 1][col].box != cell.box:
                    border_line.append(" -")
                else:
                    border_line.append("  ")
            lines.append("".join(border_line) + "\n")

            # Build cell line
            cell_line = []
            for col, cell in enumerate(row_of_cells):
                if col == 0 or self.cells[row][col - 1].box != cell.box:
                    cell_line.append(f"|{cell}")
                else:
                    cell_line.append(f" {cell}")
            lines.append("".join(cell_line) + "|\n")
        lines.append(" -" * self.size)
        return "".join(lines)

    def __repr__(self):
        """
        Returns:
            str: An ASCII art representation of the board layout,
            suitable for debugging and developer inspection.
        """
        return self.ascii

    def __str__(self):
        """
        Returns:
            str: The concatenation of all cell symbols in the board,
            reading left-to-right and top-to-bottom.

        Each empty cell is represented by the class's empty symbol (default '0').
        """
        return "".join(
            "".join(
                f"{cell.symbol if cell.symbol is not None else self.empty_symbol}"
                for cell in row
            )
            for row in self.cells
        )
