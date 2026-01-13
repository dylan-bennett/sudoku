import unittest

from sudoku.board import Board
from sudoku.engines.solver import Solver


class TestSolverSolve(unittest.TestCase):
    """Test cases for the Solver class solve method."""

    def _validate_solved_board(self, board):
        """
        Helper method to validate that a board is correctly solved.

        Checks:
        - All cells are filled
        - No duplicates in rows
        - No duplicates in columns
        - No duplicates in boxes
        - All symbols are from the allowed set
        """
        # Check all cells are filled
        for row in board.cells:
            for cell in row:
                self.assertIsNotNone(
                    cell.symbol, f"Cell at ({cell.row}, {cell.col}) is empty"
                )
                self.assertIn(
                    cell.symbol,
                    board.symbols,
                    (
                        f"Cell at ({cell.row}, {cell.col}) has "
                        f"invalid symbol '{cell.symbol}'"
                    ),
                )

        # Check rows for duplicates
        for row_idx, row_cells in board.rows.items():
            symbols = [cell.symbol for cell in row_cells]
            self.assertEqual(
                len(symbols),
                len(set(symbols)),
                f"Duplicate symbols in row {row_idx}: {symbols}",
            )

        # Check columns for duplicates
        for col_idx, col_cells in board.cols.items():
            symbols = [cell.symbol for cell in col_cells]
            self.assertEqual(
                len(symbols),
                len(set(symbols)),
                f"Duplicate symbols in column {col_idx}: {symbols}",
            )

        # Check boxes for duplicates
        for box_idx, box_cells in board.boxes.items():
            symbols = [cell.symbol for cell in box_cells]
            self.assertEqual(
                len(symbols),
                len(set(symbols)),
                f"Duplicate symbols in box {box_idx}: {symbols}",
            )

    # def test_solve_empty_board_9x9(self):
    # NOTE: CURRENTLY TAKES TOO LONG TO RUN
    #     """Test that solve can solve an empty 9x9 board."""
    #     board = Board()
    #     solver = Solver(board)
    #     result = solver.solve()

    #     self.assertTrue(result, "solve() should return True for a solvable board")
    #     self._validate_solved_board(board)

    def test_solve_already_solved_board(self):
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
        result = solver.solve()

        self.assertTrue(
            result, "solve() should return True for an already solved board"
        )
        self._validate_solved_board(board)

    def test_solve_partial_board_9x9(self):
        """Test that solve can complete a partially filled 9x9 board."""
        # fmt: off
        initial_state = (
            "530070000"
            "600195000"
            "098000060"
            "800060003"
            "400803001"
            "700020006"
            "060000280"
            "000419005"
            "000080079"
        )
        # fmt: on
        board = Board(initial_state=initial_state)
        solver = Solver(board)
        result = solver.solve()

        self.assertTrue(
            result, "solve() should return True for a solvable partial board"
        )
        self._validate_solved_board(board)

    def test_solve_empty_board_4x4(self):
        """Test that solve can solve an empty 4x4 board."""
        board = Board(symbols=["1", "2", "3", "4"])
        solver = Solver(board)
        result = solver.solve()

        self.assertTrue(result, "solve() should return True for a solvable 4x4 board")
        self._validate_solved_board(board)

    def test_solve_partial_board_4x4(self):
        """Test that solve can complete a partially filled 4x4 board."""
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
        result = solver.solve()

        self.assertTrue(
            result, "solve() should return True for a solvable 4x4 partial board"
        )
        self._validate_solved_board(board)

    def test_solve_empty_board_6x6(self):
        """Test that solve can solve an empty 6x6 board."""
        board = Board(symbols=["1", "2", "3", "4", "5", "6"])
        solver = Solver(board)
        result = solver.solve()

        self.assertTrue(result, "solve() should return True for a solvable 6x6 board")
        self._validate_solved_board(board)

    def test_solve_custom_symbols(self):
        """Test that solve works with custom symbols."""
        board = Board(symbols=["A", "B", "C", "D"])
        solver = Solver(board)
        result = solver.solve()

        self.assertTrue(
            result,
            "solve() should return True for a solvable board with custom symbols",
        )
        self._validate_solved_board(board)

    def test_solve_partial_custom_symbols(self):
        """Test that solve can complete a board with custom symbols."""
        # fmt: off
        initial_state = (
            "A000"
            "0000"
            "0000"
            "0000"
        )
        # fmt: on
        board = Board(symbols=["A", "B", "C", "D"], initial_state=initial_state)
        solver = Solver(board)
        result = solver.solve()

        self.assertTrue(
            result,
            "solve() should return True for a solvable board with custom symbols",
        )
        self._validate_solved_board(board)

    def test_solve_modifies_board_in_place(self):
        """Test that solve modifies the board object in place."""
        board = Board(symbols=range(1, 5))
        initial_empty_count = sum(
            1 for row in board.cells for cell in row if cell.symbol is None
        )
        self.assertEqual(
            initial_empty_count, 16, "Board should start with 16 empty cells"
        )

        solver = Solver(board)
        result = solver.solve()

        self.assertTrue(result)
        final_empty_count = sum(
            1 for row in board.cells for cell in row if cell.symbol is None
        )
        self.assertEqual(
            final_empty_count, 0, "Board should have no empty cells after solving"
        )

    # def test_solve_difficult_puzzle(self):
    # NOTE: CURRENTLY TAKES TOO LONG TO RUN
    #     """Test that solve can handle a difficult Sudoku puzzle."""
    #     # fmt: off
    #     initial_state = (
    #         "800000000"
    #         "003600000"
    #         "070090200"
    #         "050007000"
    #         "000045700"
    #         "000100030"
    #         "001000068"
    #         "008500010"
    #         "090000400"
    #     )
    #     # fmt: on
    #     board = Board(initial_state=initial_state)
    #     solver = Solver(board)
    #     result = solver.solve()

    #     self.assertTrue(
    #         result, "solve() should return True for a difficult but solvable puzzle"
    #     )
    #     self._validate_solved_board(board)

    # def test_solve_minimal_clues(self):
    # NOTE: CURRENTLY TAKES TOO LONG TO RUN
    #     """Test that solve can handle a puzzle with minimal clues."""
    #     # fmt: off
    #     initial_state = (
    #         "000000000"
    #         "000003085"
    #         "001020000"
    #         "000507000"
    #         "004000100"
    #         "090000000"
    #         "500000073"
    #         "002010000"
    #         "000040009"
    #     )
    #     # fmt: on
    #     board = Board(initial_state=initial_state)
    #     solver = Solver(board)
    #     result = solver.solve()

    #     self.assertTrue(
    #         result, "solve() should return True for a puzzle with minimal clues"
    #     )
    #     self._validate_solved_board(board)

    def test_solve_invalid_puzzle_fails(self):
        """Test that solve returns False on an invalid (i.e., unsolvable) puzzle"""
        # fmt: off
        initial_state = (
            "1000"
            "0020"
            "0300"
            "3000"
        )
        # fmt: on
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        solver = Solver(board)
        result = solver.solve()

        self.assertFalse(
            result, "solve() should return False for an unsolvable 4x4 partial board"
        )
