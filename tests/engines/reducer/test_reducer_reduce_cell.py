import unittest

from sudoku.board import Board
from sudoku.engines.reducer import Reducer


class TestReducerReduceCell(unittest.TestCase):
    """Test cases for the Reducer class reduce_cell method."""

    def test_reduce_cell_can_reduce_cell(self):
        """
        Test that reduce_cell removes a cell when it's redundant
        (no candidate leads to a solvable board).
        """
        # Create a filled, valid board
        # fmt: off
        initial_state = (
            "1234"
            "3412"
            "2143"
            "4321"
        )
        # fmt: on
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        cell = board.cells[0][0]  # Cell with "1"

        # Attempt to reduce the cell
        reducer = Reducer(board)
        result = reducer.reduce_cell(cell)

        # Cell should be successfully reduced
        self.assertIsNone(cell.symbol, "Cell symbol should be set to None when removed")
        self.assertTrue(
            result, "reduce_cell should return True when cell is successfully removed"
        )

    def test_reduce_cell_cannot_reduce_cell(self):
        """
        Test that reduce_cell does not remove a cell when it's essential
        (at least one candidate leads to a solvable board).
        """
        # Create a minimal unique puzzle where removing a cell would create ambiguity
        # fmt: off
        initial_state = (
            "0000"
            "0203"
            "4010"
            "0000"
        )
        # fmt: on
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        cell = board.cells[1][1]  # Cell with "2"
        original_symbol = cell.symbol

        reducer = Reducer(board)
        result = reducer.reduce_cell(cell)

        # The cell should not be reduced
        self.assertIsNotNone(cell.symbol, "Cell was not reduced, so should not be None")
        self.assertEqual(
            cell.symbol,
            original_symbol,
            "Cell symbol should remain unchanged when cell was not reduced",
        )
        self.assertFalse(
            result, "reduce_cell should return False when cell is not reduced"
        )

    def test_reduce_cell_with_empty_cell(self):
        """
        Test that reduce_cell handles an empty cell correctly.
        An empty cell has no symbol to remove, so nothing gets reduced.
        """
        board = Board(symbols=["1", "2", "3", "4"])
        cell = board.cells[0][0]  # Empty cell
        self.assertIsNone(cell.symbol, "Cell should be empty initially")

        reducer = Reducer(board)
        result = reducer.reduce_cell(cell)

        # Empty cell should remain empty, and nothing was reduced
        self.assertIsNone(cell.symbol, "Empty cell should remain empty")
        self.assertFalse(
            result, "reduce_cell should return a False when reducing an empty cell"
        )

    def test_reduce_cell_preserves_board_other_cells(self):
        """
        Test that reduce_cell only modifies the target cell, not other cells.
        """
        # fmt: off
        initial_state = (
            "1234"
            "3412"
            "2143"
            "4321"
        )
        # fmt: on
        board = Board(symbols=["1", "2", "3", "4"], initial_state=initial_state)
        cell = board.cells[0][0]

        # Store original state of all other cells
        other_cells_state = {}
        for row_idx, row in enumerate(board.cells):
            for col_idx, cell_obj in enumerate(row):
                if not (row_idx == cell.row and col_idx == cell.col):
                    other_cells_state[(row_idx, col_idx)] = cell_obj.symbol

        reducer = Reducer(board)
        result = reducer.reduce_cell(cell)

        # Verify that the cell was reduced
        self.assertTrue(result)
        self.assertIsNone(cell.symbol)

        # Verify other cells are unchanged
        for (row_idx, col_idx), original_symbol in other_cells_state.items():
            self.assertEqual(
                board.cells[row_idx][col_idx].symbol,
                original_symbol,
                f"Cell at ({row_idx}, {col_idx}) should not be modified",
            )
