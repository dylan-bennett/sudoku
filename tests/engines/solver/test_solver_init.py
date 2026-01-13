import unittest

from sudoku.board import Board
from sudoku.engines.solver import Solver


class TestSolverInit(unittest.TestCase):
    """Test cases for the Solver class __init__ method."""

    def test_init_with_default_debug(self):
        """Test that Solver initializes with DEBUG=False by default."""
        board = Board()
        solver = Solver(board)
        self.assertEqual(solver.board, board)
        self.assertFalse(solver.DEBUG)

    def test_init_with_debug_false(self):
        """Test that Solver initializes correctly with DEBUG=False explicitly."""
        board = Board()
        solver = Solver(board, DEBUG=False)
        self.assertEqual(solver.board, board)
        self.assertFalse(solver.DEBUG)

    def test_init_with_debug_true(self):
        """Test that Solver initializes correctly with DEBUG=True."""
        board = Board()
        solver = Solver(board, DEBUG=True)
        self.assertEqual(solver.board, board)
        self.assertTrue(solver.DEBUG)

    def test_init_board_reference_stored(self):
        """Test that the board reference is stored correctly."""
        board = Board()
        solver = Solver(board)
        # Verify it's the same object reference
        self.assertIs(solver.board, board)

    def test_init_with_custom_board(self):
        """Test that Solver initializes correctly with a custom board."""
        board = Board(symbols=["1", "2", "3", "4"])
        solver = Solver(board, DEBUG=True)
        self.assertEqual(solver.board, board)
        self.assertEqual(solver.board.size, 4)
        self.assertTrue(solver.DEBUG)

    def test_init_with_board_initial_state(self):
        """Test that Solver initializes correctly with a board with an initial state."""
        board = Board(symbols=["1", "2", "3"], initial_state="123000000")
        solver = Solver(board)
        self.assertEqual(solver.board, board)
        self.assertFalse(solver.DEBUG)
        # Verify the board's initial state is preserved
        self.assertEqual(solver.board.cells[0][0].symbol, "1")
        self.assertEqual(solver.board.cells[0][1].symbol, "2")
        self.assertEqual(solver.board.cells[0][2].symbol, "3")
