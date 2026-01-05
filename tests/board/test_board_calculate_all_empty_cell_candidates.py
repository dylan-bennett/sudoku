import unittest

from sudoku.board import Board


class TestBoardCalculateAllEmptyCellCandidates(unittest.TestCase):
    """Test cases for the Board class calculate_all_empty_cell_candidates method."""

    def test_calculate_all_candidates_empty_board_4x4(self):
        """Test that all empty cells get candidates assigned on empty board."""
        board = Board(symbols=["1", "2", "3", "4"])

        board.calculate_all_empty_cell_candidates()

        # All cells should have candidates assigned
        for row in board.cells:
            for cell in row:
                self.assertEqual(set(cell.candidates), {"1", "2", "3", "4"})

    def test_calculate_all_candidates_empty_board_9x9(self):
        """Test that all empty cells get candidates on empty 9x9 board."""
        board = Board()  # Default 9x9

        board.calculate_all_empty_cell_candidates()

        # All cells should have all 9 symbols as candidates
        expected_candidates = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        for row in board.cells:
            for cell in row:
                self.assertEqual(set(cell.candidates), expected_candidates)

    def test_calculate_all_candidates_skips_filled_cells(self):
        """Test that filled cells do not get candidates assigned."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill some cells
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"
        board.cells[1][0].symbol = "3"

        board.calculate_all_empty_cell_candidates()

        # Filled cells should remain None for candidates
        self.assertIsNone(board.cells[0][0].candidates)
        self.assertIsNone(board.cells[0][1].candidates)
        self.assertIsNone(board.cells[1][0].candidates)

        # Empty cells should have candidates
        self.assertIsNotNone(board.cells[0][2].candidates)
        self.assertIsNotNone(board.cells[0][3].candidates)
        self.assertIsNotNone(board.cells[1][1].candidates)

    def test_calculate_all_candidates_only_empty_cells_updated(self):
        """Test that only empty cells get candidates, filled cells are unchanged."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill some cells and set candidates manually on one
        board.cells[0][0].symbol = "1"
        board.cells[0][0].candidates = ["dummy"]  # Should remain unchanged

        board.calculate_all_empty_cell_candidates()

        # Filled cell's candidates should remain unchanged
        self.assertEqual(board.cells[0][0].candidates, ["dummy"])

    def test_calculate_all_candidates_with_partial_fill_4x4(self):
        """Test candidates calculation with partially filled 4x4 board."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill row 0: "1", "2", empty, empty
        board.cells[0][0].symbol = "1"
        board.cells[0][1].symbol = "2"
        cell_0_2 = board.cells[0][2]  # "X"
        cell_2_0 = board.cells[2][0]  # "Y"

        #  - - - -
        # |1 2|X  |
        #
        # |   |   |
        #  - - - -
        # |Y  |   |
        #
        # |   |   |
        #  - - - -

        board.calculate_all_empty_cell_candidates()

        # Cell at (0,2) should exclude "1" and "2" from row
        candidates_0_2 = set(cell_0_2.candidates)
        self.assertEqual(candidates_0_2, {"3", "4"})

        # Cell at (2,0) should exclude "1" from column
        candidates_2_0 = set(cell_2_0.candidates)
        self.assertEqual(candidates_2_0, {"2", "3", "4"})

    def test_calculate_all_candidates_all_filled_board(self):
        """Test that no candidates are assigned when all cells are filled."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Fill all cells
        initial_state = "1234123412341234"
        board.set_initial_state(initial_state)

        board.calculate_all_empty_cell_candidates()

        # All cells should remain None for candidates
        for row in board.cells:
            for cell in row:
                self.assertIsNone(cell.candidates)

    def test_calculate_all_candidates_replaces_existing_candidates(self):
        """Test that calling the method replaces existing candidate lists."""
        board = Board(symbols=["1", "2", "3", "4"])
        # Manually set some candidates
        board.cells[0][0].candidates = ["old", "candidates"]

        board.calculate_all_empty_cell_candidates()

        # Candidates should be replaced with correct ones
        self.assertEqual(set(board.cells[0][0].candidates), {"1", "2", "3", "4"})
        self.assertNotEqual(board.cells[0][0].candidates, ["old", "candidates"])

    def test_calculate_all_candidates_multiple_calls_idempotent(self):
        """Test that calling the method multiple times produces same results."""
        board = Board(symbols=["1", "2", "3", "4"])
        board.cells[0][2].symbol = "1"
        board.cells[2][3].symbol = "2"
        board.cells[3][1].symbol = "3"
        board.cells[1][0].symbol = "4"

        board.calculate_all_empty_cell_candidates()
        first_call_candidates = {}
        for row_idx, row in enumerate(board.cells):
            for col_idx, cell in enumerate(row):
                if cell.candidates is not None:
                    first_call_candidates[(row_idx, col_idx)] = cell.candidates.copy()

        board.calculate_all_empty_cell_candidates()

        # Compare candidates after second call
        for row_idx, row in enumerate(board.cells):
            for col_idx, cell in enumerate(row):
                if (row_idx, col_idx) in first_call_candidates:
                    self.assertEqual(
                        set(cell.candidates),
                        set(first_call_candidates[(row_idx, col_idx)]),
                    )

    def test_calculate_all_candidates_integration_with_calculate_cell_candidates(self):
        """Test that candidates match what calculate_cell_candidates would return."""
        board = Board(symbols=["1", "2", "3", "4"])
        board.cells[0][3].symbol = "1"
        board.cells[3][1].symbol = "2"
        board.cells[1][2].symbol = "3"
        board.cells[2][0].symbol = "4"

        board.calculate_all_empty_cell_candidates()

        # Verify that candidates match individual calls
        for row in board.cells:
            for cell in row:
                if cell.symbol is None:
                    expected = board.calculate_cell_candidates(cell)
                    self.assertEqual(set(cell.candidates), expected)
