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
