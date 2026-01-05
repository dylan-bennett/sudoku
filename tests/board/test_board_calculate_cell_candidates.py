import unittest

from sudoku.board import Board


class TestBoardCalculateCellCandidates(unittest.TestCase):
    """Test cases for the Board class calculate_cell_candidates method."""

    def test_calculate_candidates_empty_board_4x4(self):
        """Test that empty board returns all symbols as candidates."""
        board = Board(symbols=["1", "2", "3", "4"])
        cell = board.cells[0][0]

        candidates = board.calculate_cell_candidates(cell)

        self.assertEqual(candidates, {"1", "2", "3", "4"})

    def test_calculate_candidates_empty_board_9x9(self):
        """Test that empty 9x9 board returns all symbols as candidates."""
        board = Board()  # Default 9x9
        cell = board.cells[4][4]

        candidates = board.calculate_cell_candidates(cell)

        self.assertEqual(candidates, {"1", "2", "3", "4", "5", "6", "7", "8", "9"})

    def test_calculate_candidates_with_row_constraints(self):
        """Test that symbols in the same row are excluded from candidates."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill row 0 with "1" and "2"
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"
        cell = board.cells[0][3]  # Empty cell in same row

        #  - - - -
        # |1 2|  X|
        #
        # |   |   |
        #  - - - -
        # |   |   |
        #
        # |   |   |
        #  - - - -

        candidates = board.calculate_cell_candidates(cell)

        # Should exclude "1" and "2" (in same row), but include "3" and "4"
        self.assertEqual(candidates, {"3", "4"})

    def test_calculate_candidates_with_column_constraints(self):
        """Test that symbols in the same column are excluded from candidates."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill column 0 with "1" and "3"
        board.cells[0][0].symbol = "1"
        board.cells[2][0].symbol = "3"
        cell = board.cells[3][0]  # Empty cell in same column

        #  - - - -
        # |1  |   |
        #
        # |   |   |
        #  - - - -
        # |3  |   |
        #
        # |X  |   |
        #  - - - -

        candidates = board.calculate_cell_candidates(cell)

        # Should exclude "1" and "3" (in same column), but include "2" and "4"
        self.assertEqual(candidates, {"2", "4"})

    def test_calculate_candidates_with_box_constraints(self):
        """Test that symbols in the same box are excluded from candidates."""
        board = Board(symbols=["1", "2", "3", "4"])  # 2x2 boxes
        # Fill box 0 (top-left) with "1" and "2"
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"
        cell = board.cells[1][0]  # Empty cell in same box (bottom-left of box 0)

        #  - - - -
        # |1 2|   |
        #
        # |X  |   |
        #  - - - -
        # |   |   |
        #
        # |   |   |
        #  - - - -

        candidates = board.calculate_cell_candidates(cell)

        # Should exclude "1" and "2" (in same box), but include "3" and "4"
        self.assertEqual(candidates, {"3", "4"})

    def test_calculate_candidates_with_combined_constraints(self):
        """Test that symbols in row, column, and box are all excluded."""
        board = Board(symbols=["1", "2", "3", "4"])

        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"
        board.cells[1][3].symbol = "3"
        board.cells[1][0].symbol = "4"
        cell = board.cells[0][3]

        #  - - - -
        # |1 2|  X|
        #
        # |4  |  3|
        #  - - - -
        # |   |   |
        #
        # |   |   |
        #  - - - -

        # So "1" and "2" are in the same row, "3" is in the same column & box,
        # but "4" is in none of them.
        # That means our only candidate should be "4".
        candidates = board.calculate_cell_candidates(cell)
        self.assertEqual(candidates, {"4"})

    def test_calculate_candidates_all_constraints_exhausted(self):
        """Test that when all symbols are constrained, empty set is returned."""
        board = Board(symbols=["1", "2", "3", "4"])
        board.cells[0][0].symbol = "1"
        board.cells[0][2].symbol = "2"
        board.cells[1][1].symbol = "3"
        board.cells[1][0].symbol = "4"
        cell = board.cells[0][1]

        #  - - - -
        # |1 X|2  |
        #
        # |4 3|   |
        #  - - - -
        # |   |   |
        #
        # |   |   |
        #  - - - -

        # So "1", "3", and "4" are in the same box, and "2" is in the same row.
        # That means we have no candidates.
        candidates = board.calculate_cell_candidates(cell)
        self.assertEqual(candidates, set())

    def test_calculate_candidates_different_cells_same_board(self):
        """Test that different cells can have different candidate sets."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Set up board with different constraints in different areas
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"
        board.cells[2][2].symbol = "3"
        board.cells[3][2].symbol = "4"

        cell1 = board.cells[0][2]  # X
        cell2 = board.cells[1][1]  # Y

        #  - - - -
        # |1 2|X  |
        #
        # |  Y|   |
        #  - - - -
        # |   |3  |
        #
        # |   |4  |
        #  - - - -

        candidates1 = board.calculate_cell_candidates(cell1)
        candidates2 = board.calculate_cell_candidates(cell2)

        self.assertEqual(candidates1, set())
        self.assertEqual(candidates2, {"3", "4"})

    def test_calculate_candidates_returns_set_type(self):
        """Test that calculate_cell_candidates returns a set object."""
        board = Board(symbols=["1", "2", "3", "4"])
        cell = board.cells[0][0]

        candidates = board.calculate_cell_candidates(cell)

        self.assertIsInstance(candidates, set)

    def test_calculate_candidates_handles_none_symbols(self):
        """Test calculate_candidates correctly handles None symbols (empty cells)."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Set up board with some filled and some empty cells
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = None  # Explicitly empty
        board.cells[1][0].symbol = "2"
        cell = board.cells[0][1]

        candidates = board.calculate_cell_candidates(cell)

        # Should exclude "1" and "2", but not None
        # None values are discarded, so candidates should be {"3", "4"}
        self.assertEqual(candidates, {"3", "4"})
