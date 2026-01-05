import unittest

from sudoku.board import Board


class TestBoardSetInitialState(unittest.TestCase):
    """Test cases for the Board class set_initial_state method."""

    def test_set_initial_state_with_string_4x4(self):
        """Test that set_initial_state works with a string input for 4x4 board."""
        board = Board(symbols=["1", "2", "3", "4"])
        initial_state = "1234000000000000"
        board.set_initial_state(initial_state)

        # First row should be filled
        self.assertEqual(board.cells[0][0].symbol, "1")
        self.assertEqual(board.cells[0][1].symbol, "2")
        self.assertEqual(board.cells[0][2].symbol, "3")
        self.assertEqual(board.cells[0][3].symbol, "4")

        # Rest should be empty
        for row in range(1, 4):
            for col in range(4):
                self.assertIsNone(board.cells[row][col].symbol)

    def test_set_initial_state_with_list_4x4(self):
        """Test that set_initial_state works with a list input for 4x4 board."""
        board = Board(symbols=["1", "2", "3", "4"])
        initial_state = [
            "1",
            "2",
            "3",
            "4",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
        ]
        board.set_initial_state(initial_state)

        # First row should be filled
        self.assertEqual(board.cells[0][0].symbol, "1")
        self.assertEqual(board.cells[0][1].symbol, "2")
        self.assertEqual(board.cells[0][2].symbol, "3")
        self.assertEqual(board.cells[0][3].symbol, "4")

        # Rest should be empty
        for row in range(1, 4):
            for col in range(4):
                self.assertIsNone(board.cells[row][col].symbol)

    def test_set_initial_state_with_empty_symbols(self):
        """Test that set_initial_state correctly handles empty symbols."""
        board = Board(symbols=["1", "2", "3", "4"])
        initial_state = "0000000000000000"
        board.set_initial_state(initial_state)

        # All cells should be empty
        for row in board.cells:
            for cell in row:
                self.assertIsNone(cell.symbol)

    def test_set_initial_state_with_custom_empty_symbol(self):
        """Test that set_initial_state works with custom empty_symbol."""
        board = Board(symbols=["1", "2", "3", "4"], empty_symbol=".")
        initial_state = "1234............"
        board.set_initial_state(initial_state)

        # First row should be filled
        self.assertEqual(board.cells[0][0].symbol, "1")
        self.assertEqual(board.cells[0][1].symbol, "2")
        self.assertEqual(board.cells[0][2].symbol, "3")
        self.assertEqual(board.cells[0][3].symbol, "4")

        # Rest should be empty (represented by "." in initial_state)
        for row in range(1, 4):
            for col in range(4):
                self.assertIsNone(board.cells[row][col].symbol)

    def test_set_initial_state_replaces_previous_state(self):
        """Test calling set_initial_state multiple times replaces previous state."""
        board = Board(symbols=["1", "2", "3", "4"])

        # Set initial state
        board.set_initial_state("1234000000000000")
        # First row should be filled
        self.assertEqual(board.cells[0][0].symbol, "1")
        self.assertEqual(board.cells[0][1].symbol, "2")
        self.assertEqual(board.cells[0][2].symbol, "3")
        self.assertEqual(board.cells[0][3].symbol, "4")
        # Last row should be empty
        self.assertIsNone(board.cells[3][0].symbol)
        self.assertIsNone(board.cells[3][1].symbol)
        self.assertIsNone(board.cells[3][2].symbol)
        self.assertIsNone(board.cells[3][3].symbol)

        # Replace with new state
        board.set_initial_state("0000000000004321")
        # First row should now be empty
        self.assertIsNone(board.cells[0][0].symbol)
        self.assertIsNone(board.cells[0][1].symbol)
        # Last row should now be filled
        self.assertEqual(board.cells[3][0].symbol, "4")
        self.assertEqual(board.cells[3][1].symbol, "3")
        self.assertEqual(board.cells[3][2].symbol, "2")
        self.assertEqual(board.cells[3][3].symbol, "1")

    def test_set_initial_state_raises_error_wrong_length_too_short(self):
        """Test that ValueError is raised when initial_state is too short."""
        board = Board(symbols=["1", "2", "3", "4"])

        with self.assertRaises(ValueError) as context:
            board.set_initial_state("123")

        self.assertIn("must have exactly", str(context.exception).lower())
        self.assertIn("16", str(context.exception))  # 4*4 = 16

    def test_set_initial_state_raises_error_wrong_length_too_long(self):
        """Test that ValueError is raised when initial_state is too long."""
        board = Board(symbols=["1", "2", "3", "4"])

        with self.assertRaises(ValueError) as context:
            board.set_initial_state("0" * 20)  # 20 > 16

        self.assertIn("must have exactly", str(context.exception).lower())
        self.assertIn("16", str(context.exception))

    def test_set_initial_state_raises_error_invalid_symbol(self):
        """Test that ValueError is raised when initial_state contains invalid symbol."""
        board = Board(symbols=["1", "2", "3", "4"])

        with self.assertRaises(ValueError) as context:
            board.set_initial_state("1235000000000000")  # "5" is not a valid symbol

        self.assertIn("invalid symbol", str(context.exception).lower())
        self.assertIn("'5'", str(context.exception))
        self.assertIn("index", str(context.exception).lower())

    def test_set_initial_state_raises_error_invalid_symbol_custom_empty(self):
        """Test ValueError is raised for invalid symbol with custom empty_symbol."""
        board = Board(symbols=["1", "2", "3", "4"], empty_symbol=".")

        with self.assertRaises(ValueError) as context:
            # "0" is not valid (empty_symbol is ".")
            board.set_initial_state("1234.00000000000")

        self.assertIn("invalid symbol", str(context.exception).lower())
        self.assertIn("'0'", str(context.exception))

    def test_set_initial_state_with_all_symbols_filled(self):
        """Test that set_initial_state works when all cells are filled."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill all cells with a pattern
        initial_state = "1234123412341234"
        board.set_initial_state(initial_state)

        # Verify all cells are filled
        for row in range(4):
            for col in range(4):
                self.assertIsNotNone(board.cells[row][col].symbol)
