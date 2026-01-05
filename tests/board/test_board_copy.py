import unittest

from sudoku.board import Board


class TestBoardCopy(unittest.TestCase):
    """Test cases for the Board class copy method."""

    def test_copy_returns_new_board_instance(self):
        """Test that copy returns a new Board instance, not the same object."""
        board = Board(symbols=["1", "2", "3", "4"])
        copied_board = board.copy()

        self.assertIsNot(board, copied_board)
        self.assertIsInstance(copied_board, Board)

    def test_copy_has_same_configuration(self):
        """Test that copied board has the same symbols and empty_symbol."""
        board = Board(symbols=["A", "B", "C"], empty_symbol=".")
        copied_board = board.copy()

        self.assertEqual(copied_board.symbols, board.symbols)
        self.assertEqual(copied_board.empty_symbol, board.empty_symbol)
        self.assertEqual(copied_board.size, board.size)

    def test_copy_has_same_box_structure(self):
        """Test that copied board has the same box structure."""
        board = Board(symbols=range(1, 7))
        copied_board = board.copy()

        self.assertEqual(copied_board.num_bands, board.num_bands)
        self.assertEqual(copied_board.num_stacks, board.num_stacks)

    def test_copy_copies_empty_board(self):
        """Test that copying an empty board results in an empty board."""
        board = Board(symbols=["1", "2", "3", "4"])
        copied_board = board.copy()

        # All cells should be empty in both boards
        for row in copied_board.cells:
            for cell in row:
                self.assertIsNone(cell.symbol)

    def test_copy_copies_filled_cells(self):
        """Test that copying a board with filled cells copies all symbols."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill some cells
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"
        board.cells[1][0].symbol = None
        board.cells[3][3].symbol = "4"

        copied_board = board.copy()

        # Verify symbols are copied
        self.assertEqual(copied_board.cells[0][0].symbol, "1")
        self.assertEqual(copied_board.cells[0][1].symbol, "2")
        self.assertIsNone(copied_board.cells[1][0].symbol)
        self.assertEqual(copied_board.cells[3][3].symbol, "4")

    def test_copy_with_initial_state(self):
        """Test that copying a board created with initial_state works correctly."""
        initial_state = "1234000000000000"  # 4x4 board with first row filled
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        copied_board = board.copy()

        # Verify the initialized symbols match
        self.assertEqual(copied_board.cells[0][0].symbol, "1")
        self.assertEqual(copied_board.cells[0][1].symbol, "2")
        self.assertEqual(copied_board.cells[0][2].symbol, "3")
        self.assertEqual(copied_board.cells[0][3].symbol, "4")
        self.assertIsNone(copied_board.cells[1][0].symbol)

    def test_copy_creates_new_cell_objects(self):
        """Test that copied board has new Cell objects, not references to originals."""
        board = Board(symbols=["1", "2", "3", "4"])
        copied_board = board.copy()

        # Cell objects should be different instances
        self.assertIsNot(copied_board.cells[0][0], board.cells[0][0])
        self.assertIsNot(copied_board.cells[1][1], board.cells[1][1])

    def test_modifying_copy_does_not_affect_original(self):
        """Test that modifying the copied board does not affect the original."""
        board = Board(symbols=["1", "2", "3", "4"])
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"

        copied_board = board.copy()

        # Modify the copy
        copied_board.cells[0][0].symbol = "3"
        copied_board.cells[0][1].symbol = None

        # Original should be unchanged
        self.assertEqual(board.cells[0][0].symbol, "1")
        self.assertEqual(board.cells[0][1].symbol, "2")

    def test_modifying_original_does_not_affect_copy(self):
        """Test that modifying the original board does not affect the copy."""
        board = Board(symbols=["1", "2", "3", "4"])
        board.cells[0][0].symbol = "1"

        copied_board = board.copy()

        # Modify the original
        board.cells[0][0].symbol = "4"
        board.cells[1][1].symbol = "2"

        # Copy should be unchanged
        self.assertEqual(copied_board.cells[0][0].symbol, "1")
        self.assertIsNone(copied_board.cells[1][1].symbol)

    def test_copy_lookup_dictionaries_are_separate(self):
        """Test that copied board has separate lookup dictionaries."""
        board = Board(symbols=["1", "2", "3", "4"])
        board.cells[0][0].symbol = "1"

        copied_board = board.copy()

        # Modify a cell through the copy's rows dictionary
        copied_board.rows[0][0].symbol = "2"

        # Original should be unchanged
        self.assertEqual(board.rows[0][0].symbol, "1")
        self.assertEqual(copied_board.rows[0][0].symbol, "2")
