import unittest


class BaseTestSolverSolve(unittest.TestCase):
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
