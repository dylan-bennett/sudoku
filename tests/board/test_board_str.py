import unittest

from sudoku.board import Board


class TestBoardStr(unittest.TestCase):
    """Test cases for the Board class __str__ method."""

    def test_str_empty_board_4x4(self):
        """Test that empty board returns string of empty symbols."""
        board = Board(symbols=["1", "2", "3", "4"])
        result = str(board)
        self.assertEqual(result, "0" * 16)  # 4x4 = 16 cells

    def test_str_empty_board_9x9(self):
        """Test that empty 9x9 board returns string of empty symbols."""
        board = Board()  # Default 9x9
        result = str(board)
        self.assertEqual(result, "0" * 81)  # 9x9 = 81 cells

    def test_str_partially_filled_board(self):
        """Test that partially filled board returns correct string."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill only first row
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"
        board.cells[0][2].symbol = "3"
        board.cells[0][3].symbol = "4"
        result = str(board)
        expected = "1234" + "0" * 12  # First row filled, rest empty
        self.assertEqual(result, expected)

    def test_str_order_left_to_right_top_to_bottom(self):
        """Test that string is ordered left-to-right, top-to-bottom."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill cells in a pattern to verify order
        board.cells[0][0].symbol = "A"
        board.cells[0][1].symbol = "B"
        board.cells[1][0].symbol = "C"
        board.cells[1][1].symbol = "D"
        result = str(board)
        # Should be: row 0: A B 0 0, row 1: C D 0 0, row 2: 0 0 0 0, row 3: 0 0 0 0
        expected = "AB00" + "CD00" + "0" * 8
        self.assertEqual(result, expected)

    def test_str_with_custom_empty_symbol(self):
        """Test that custom empty_symbol is used in string representation."""
        board = Board(symbols=["1", "2", "3"], empty_symbol=".")
        result = str(board)
        self.assertEqual(result, "." * 9)  # 3x3 = 9 cells

    def test_str_custom_empty_symbol_with_filled_cells(self):
        """Test custom empty_symbol with some filled cells."""
        board = Board(symbols=["1", "2", "3"], empty_symbol=".")
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"
        result = str(board)
        # First row: "12.", then "." for remaining cells
        expected = "12." + "." * 6
        self.assertEqual(result, expected)

    def test_str_matches_initial_state_format(self):
        """Test that __str__ output matches initial_state format."""
        board = Board(symbols=["1", "2", "3", "4"])
        initial_state = "1234000000000000"
        board.set_initial_state(initial_state)
        result = str(board)
        self.assertEqual(result, initial_state)

    def test_str_all_cells_filled_different_symbols(self):
        """Test __str__ when all cells are filled with different symbols."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill with pattern
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"
        board.cells[0][2].symbol = "3"
        board.cells[0][3].symbol = "4"
        board.cells[1][0].symbol = "4"
        board.cells[1][1].symbol = "3"
        board.cells[1][2].symbol = "2"
        board.cells[1][3].symbol = "1"
        board.cells[2][0].symbol = "2"
        board.cells[2][1].symbol = "1"
        board.cells[2][2].symbol = "4"
        board.cells[2][3].symbol = "3"
        board.cells[3][0].symbol = "3"
        board.cells[3][1].symbol = "4"
        board.cells[3][2].symbol = "1"
        board.cells[3][3].symbol = "2"
        result = str(board)
        expected = "1234" + "4321" + "2143" + "3412"
        self.assertEqual(result, expected)

    def test_str_length_matches_board_size(self):
        """Test that string length equals size * size."""
        board = Board(symbols=["1", "2", "3", "4"])
        result = str(board)
        self.assertEqual(len(result), board.size * board.size)

    def test_str_after_modifying_cells(self):
        """Test that __str__ reflects changes after modifying cells."""
        board = Board(symbols=["1", "2", "3", "4"])
        initial_result = str(board)
        self.assertEqual(initial_result, "0" * 16)

        # Modify a cell
        board.cells[0][0].symbol = "1"
        modified_result = str(board)
        expected = "1" + "0" * 15
        self.assertEqual(modified_result, expected)

        # Modify another cell
        board.cells[2][2].symbol = "2"
        final_result = str(board)
        # Position 2,2 in row-major order: row 0 (4 cells) + row 1 (4 cells) + 2
        expected = "1" + "0" * 9 + "2" + "0" * 5
        self.assertEqual(final_result, expected)

