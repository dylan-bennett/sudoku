import unittest

from sudoku.board import Board
from sudoku.engines.reducer import Reducer


class TestReducerInit(unittest.TestCase):
    """Test cases for the Reducer class __init__ method."""

    def test_init_with_default_board(self):
        """Test that Reducer initializes correctly with a default board."""
        board = Board()
        reducer = Reducer(board)
        self.assertEqual(reducer.board, board)

    def test_init_board_reference_stored(self):
        """Test that the board reference is stored correctly."""
        board = Board()
        reducer = Reducer(board)
        # Verify it's the same object reference
        self.assertIs(reducer.board, board)

    def test_init_with_custom_board(self):
        """Test that Reducer initializes correctly with a custom board."""
        board = Board(symbols=["1", "2", "3", "4"])
        reducer = Reducer(board)
        self.assertEqual(reducer.board, board)
        self.assertEqual(reducer.board.size, 4)

    def test_init_with_board_initial_state(self):
        """
        Test that Reducer initializes correctly with a board with an initial state.
        """
        board = Board(symbols=["1", "2", "3"], initial_state="123000000")
        reducer = Reducer(board)
        self.assertEqual(reducer.board, board)
        # Verify the board's initial state is preserved
        self.assertEqual(reducer.board.cells[0][0].symbol, "1")
        self.assertEqual(reducer.board.cells[0][1].symbol, "2")
        self.assertEqual(reducer.board.cells[0][2].symbol, "3")

    def test_init_board_modifications_reflected(self):
        """Test that modifications to the board are reflected in the reducer."""
        board = Board()
        reducer = Reducer(board)
        # Modify the board
        board.cells[0][0].symbol = "1"
        # Verify the modification is reflected in the reducer's board reference
        self.assertEqual(reducer.board.cells[0][0].symbol, "1")
