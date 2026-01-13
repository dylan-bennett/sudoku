from sudoku.board import Board
from sudoku.engines.solver import Solver
from tests.engines.solver import BaseTestSolverSolve


class TestSolverSolveBacktrack(BaseTestSolverSolve):
    """Test cases for the Solver class solve method."""

    def test_solve_backtrack_partial_board_4x4(self):
        """Test that solve can complete a partially filled 4x4 board."""
        # fmt: off
        initial_state = (
            "1000"
            "0200"
            "0030"
            "0004"
        )
        # fmt: on
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        solver = Solver(board)
        result = solver.solve_backtrack()

        self.assertTrue(
            result, "solve() should return True for a solvable partial board"
        )
        self._validate_solved_board(board)

    def test_solve_backtrack_invalid_puzzle_fails_row_conflict(self):
        """
        Test that solve returns False on an invalid (i.e., unsolvable) puzzle
        with a row conflict
        """
        # fmt: off
        initial_state = (
            "1001"
            "0020"
            "0300"
            "0000"
        )
        # fmt: on
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        solver = Solver(board)
        result = solver.solve_backtrack()

        self.assertFalse(
            result, "solve() should return False for an unsolvable 4x4 partial board"
        )

    def test_solve_backtrack_invalid_puzzle_fails_col_conflict(self):
        """
        Test that solve returns False on an invalid (i.e., unsolvable) puzzle
        with a column conflict
        """
        # fmt: off
        initial_state = (
            "1000"
            "0020"
            "0300"
            "1000"
        )
        # fmt: on
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        solver = Solver(board)
        result = solver.solve_backtrack()

        self.assertFalse(
            result, "solve() should return False for an unsolvable 4x4 partial board"
        )

    def test_solve_backtrack_invalid_puzzle_fails_box_conflict(self):
        """
        Test that solve returns False on an invalid (i.e., unsolvable) puzzle
        with a box conflict
        """
        # fmt: off
        initial_state = (
            "1000"
            "0120"
            "0300"
            "0000"
        )
        # fmt: on
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        solver = Solver(board)
        result = solver.solve_backtrack()

        self.assertFalse(
            result, "solve() should return False for an unsolvable 4x4 partial board"
        )

    def test_solve_backtrack_empty_board_4x4(self):
        """Test that solve can solve an empty 4x4 board."""
        board = Board(symbols=["1", "2", "3", "4"])
        solver = Solver(board)
        result = solver.solve_backtrack()

        self.assertTrue(result, "solve() should return True for a solvable 4x4 board")
        self._validate_solved_board(board)

    def test_solve_backtrack_already_solved_board(self):
        """Test that solve returns True for an already solved board."""
        # fmt: off
        initial_state = (
            "123456789"
            "456789123"
            "789123456"
            "234567891"
            "567891234"
            "891234567"
            "345678912"
            "678912345"
            "912345678"
        )
        # fmt: on
        board = Board(initial_state=initial_state)
        solver = Solver(board)
        result = solver.solve_backtrack()

        self.assertTrue(
            result, "solve() should return True for an already solved board"
        )

    def test_solve_backtrack_empty_board_6x6(self):
        """Test that solve can solve an empty 6x6 board."""
        board = Board(symbols=["1", "2", "3", "4", "5", "6"])
        solver = Solver(board)
        result = solver.solve_backtrack()

        self.assertTrue(result, "solve() should return True for a solvable 6x6 board")
        self._validate_solved_board(board)
