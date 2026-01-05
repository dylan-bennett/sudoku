import unittest

from sudoku.board import Board


class TestBoardInit(unittest.TestCase):
    """Test cases for the Board class __init__ method."""

    def test_init_with_default_symbols(self):
        """Test that Board initializes with default symbols (1-9) when symbols=None."""
        board = Board()
        self.assertEqual(board.symbols, ["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        self.assertEqual(board.size, 9)
        self.assertEqual(board.empty_symbol, "0")

    def test_init_with_custom_symbols_list(self):
        """Test that Board initializes with custom list of symbols."""
        board = Board(symbols=["A", "B", "C", "D"])
        self.assertEqual(board.symbols, ["A", "B", "C", "D"])
        self.assertEqual(board.size, 4)

    def test_init_with_numeric_symbols(self):
        """Test that numeric symbols are converted to strings."""
        board = Board(symbols=[1, 2, 3, 4, 5])
        self.assertEqual(board.symbols, ["1", "2", "3", "4", "5"])
        self.assertEqual(board.size, 5)

    def test_init_with_mixed_symbol_types(self):
        """Test that mixed symbol types are converted to strings and sorted."""
        board = Board(symbols=[10, "A", 5, "B"])
        self.assertEqual(board.symbols, ["10", "5", "A", "B"])
        self.assertEqual(board.size, 4)

    def test_init_symbols_are_sorted(self):
        """Test that symbols are always stored in sorted order."""
        board = Board(symbols=["Z", "A", "M", "B"])
        self.assertEqual(board.symbols, ["A", "B", "M", "Z"])

    def test_init_with_custom_empty_symbol(self):
        """Test that Board accepts a custom empty_symbol."""
        board = Board(symbols=["1", "2", "3"], empty_symbol=".")
        self.assertEqual(board.empty_symbol, ".")
        self.assertEqual(board.symbols, ["1", "2", "3"])

    def test_init_empty_symbol_conflict_raises_error(self):
        """Test that ValueError is raised when empty_symbol conflicts with symbols."""
        with self.assertRaises(ValueError) as context:
            Board(symbols=["1", "2", "3"], empty_symbol="2")

        self.assertIn("empty symbol '2'", str(context.exception).lower())
        self.assertIn("must not appear", str(context.exception).lower())

    def test_init_size_calculation(self):
        """Test that board size equals the number of symbols."""
        board = Board(symbols=["A", "B", "C"])
        self.assertEqual(board.size, 3)

        board2 = Board(symbols=range(1, 17))  # 16 symbols
        self.assertEqual(board2.size, 16)

    def test_init_box_structure_9x9(self):
        """Test that 9x9 board has correct box structure (3x3 boxes)."""
        board = Board()  # Default 9x9
        # For 9, closest_factors should return (3, 3)
        self.assertEqual(board.num_bands, 3)
        self.assertEqual(board.num_stacks, 3)
        self.assertEqual(board.num_bands * board.num_stacks, board.size)

    def test_init_box_structure_4x4(self):
        """Test that 4x4 board has correct box structure (2x2 boxes)."""
        board = Board(symbols=["1", "2", "3", "4"])
        # For 4, closest_factors should return (2, 2)
        self.assertEqual(board.num_bands, 2)
        self.assertEqual(board.num_stacks, 2)

    def test_init_box_structure_6x6(self):
        """Test that 6x6 board has correct box structure."""
        board = Board(symbols=["1", "2", "3", "4", "5", "6"])
        # For 6, closest_factors should return (2, 3)
        self.assertEqual(board.num_bands, 2)
        self.assertEqual(board.num_stacks, 3)
        self.assertEqual(board.num_bands * board.num_stacks, board.size)

    def test_init_cells_initialized(self):
        """Test that cells are initialized as empty."""
        board = Board(symbols=["1", "2", "3", "4"])
        self.assertEqual(len(board.cells), 4)  # 4 rows
        self.assertEqual(len(board.cells[0]), 4)  # 4 columns

        # All cells should be empty initially
        for row in board.cells:
            for cell in row:
                self.assertIsNone(cell.symbol)

    def test_init_lookup_dictionaries_initialized(self):
        """Test that rows, cols, and boxes dictionaries are initialized."""
        board = Board(symbols=["1", "2", "3", "4"])
        self.assertIsInstance(board.rows, dict)
        self.assertIsInstance(board.cols, dict)
        self.assertIsInstance(board.boxes, dict)

        # Should have correct number of entries
        self.assertEqual(len(board.rows), 4)
        self.assertEqual(len(board.cols), 4)
        # Number of boxes depends on box structure

    def test_init_with_empty_initial_state(self):
        """Test that Board initializes correctly with empty initial_state."""
        board = Board(symbols=["1", "2", "3"], initial_state="000000000")
        # All cells should be empty
        for row in board.cells:
            for cell in row:
                self.assertIsNone(cell.symbol)

    def test_init_with_initial_state(self):
        """Test that Board initializes correctly with an initial state."""
        board = Board(symbols=range(1, 4), initial_state="321300123")
        self.assertEqual(board.cells[0][0].symbol, "3")
        self.assertEqual(board.cells[0][1].symbol, "2")
        self.assertEqual(board.cells[0][2].symbol, "1")
        self.assertEqual(board.cells[1][0].symbol, "3")
        self.assertIsNone(board.cells[1][1].symbol)
        self.assertIsNone(board.cells[1][2].symbol)
        self.assertEqual(board.cells[2][0].symbol, "1")
        self.assertEqual(board.cells[2][1].symbol, "2")
        self.assertEqual(board.cells[2][2].symbol, "3")

    def test_init_without_initial_state(self):
        """Test that Board initializes correctly without initial_state."""
        board = Board(symbols=["1", "2", "3"])
        # All cells should be empty
        for row in board.cells:
            for cell in row:
                self.assertIsNone(cell.symbol)
