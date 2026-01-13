import unittest

from sudoku.board import Board
from sudoku.engines.solver import Solver


class TestSolverIsCandidateValid(unittest.TestCase):
    """Test cases for the Solver class is_candidate_valid method."""

    def test_valid_candidate_empty_board(self):
        """Test that a candidate is valid on an empty board."""
        board = Board()
        solver = Solver(board)
        cell = board.cells[0][0]
        self.assertTrue(solver.is_candidate_valid("1", cell))

    def test_valid_candidate_no_conflicts(self):
        """
        Test that a candidate is valid when it doesn't conflict with row, col, or box.
        """
        # fmt: off
        initial_state = (
            "100000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
        )
        # fmt: on
        board = Board(initial_state=initial_state)
        solver = Solver(board)
        # Cell at (1, 1) - "1" is in row 0, col 0, box 0, so "2" should be valid at (1, 1)
        cell = board.cells[1][1]
        self.assertTrue(solver.is_candidate_valid("2", cell))

    def test_invalid_candidate_same_row(self):
        """Test that a candidate is invalid if it appears in the same row."""
        # fmt: off
        initial_state = (
            "100000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
        )
        # fmt: on
        board = Board(initial_state=initial_state)
        solver = Solver(board)
        # Cell at (0, 7) - "1" is already in row 0 at (0, 0)
        cell = board.cells[0][7]
        self.assertFalse(solver.is_candidate_valid("1", cell))

    def test_invalid_candidate_same_column(self):
        """Test that a candidate is invalid if it appears in the same column."""
        # fmt: off
        initial_state = (
            "100000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
        )
        # fmt: on
        board = Board(initial_state=initial_state)
        solver = Solver(board)
        # Cell at (5, 0) - "1" is already in column 0 at (0, 0)
        cell = board.cells[5][0]
        self.assertFalse(solver.is_candidate_valid("1", cell))

    def test_invalid_candidate_same_box(self):
        """Test that a candidate is invalid if it appears in the same box."""
        # fmt: off
        initial_state = (
            "100000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
        )
        # fmt: on
        board = Board(initial_state=initial_state)
        solver = Solver(board)
        # Cell at (1, 1) - "1" is already in box 0 at (0, 0)
        cell = board.cells[1][1]
        self.assertFalse(solver.is_candidate_valid("1", cell))

    def test_valid_candidate_ignores_current_cell(self):
        """Test that the method ignores the current cell's symbol when checking."""
        # fmt: off
        initial_state = (
            "100000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
        )
        # fmt: on
        board = Board(initial_state=initial_state)
        solver = Solver(board)
        # Cell at (0, 0) already has "1"
        # It should return True because "1" is technically valid
        cell = board.cells[0][0]
        self.assertTrue(solver.is_candidate_valid("1", cell))

    def test_valid_candidate_different_row_col_box(self):
        """Test that a candidate is valid when it's in a different row, column, and box."""
        # fmt: off
        initial_state = (
            "100000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
        )
        # fmt: on
        board = Board(initial_state=initial_state)
        solver = Solver(board)
        # Cell at (5, 8) - "1" is at (0, 0) which is different row, col, and box
        cell = board.cells[5][8]
        self.assertTrue(solver.is_candidate_valid("1", cell))

    def test_valid_candidate_4x4_board(self):
        """Test candidate validation on a 4x4 board."""
        # fmt: off
        initial_state = (
            "1000"
            "0000"
            "0000"
            "0000"
        )
        # fmt: on
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        solver = Solver(board)
        # Cell at (1, 1) - "1" is at (0, 0), so "2" should be valid
        cell = board.cells[1][1]
        self.assertTrue(solver.is_candidate_valid("2", cell))

    def test_invalid_candidate_4x4_board_same_box(self):
        """Test that a candidate is invalid in the same box on a 4x4 board."""
        # fmt: off
        initial_state = (
            "1000"
            "0000"
            "0000"
            "0000"
        )
        # fmt: on
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        solver = Solver(board)
        # Cell at (1, 1) - "1" is at (0, 0) which is in the same 2x2 box
        cell = board.cells[1][1]
        self.assertFalse(solver.is_candidate_valid("1", cell))
