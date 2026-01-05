import unittest

from sudoku.board import Cell


class TestCellInit(unittest.TestCase):
    """Test cases for the Cell class."""

    def test_init_with_all_parameters(self):
        """Test that Cell initializes correctly with all parameters."""
        cell = Cell(row=0, col=1, box=2, symbol="5", candidates=["1", "2", "3"])
        self.assertEqual(cell.row, 0)
        self.assertEqual(cell.col, 1)
        self.assertEqual(cell.box, 2)
        self.assertEqual(cell.symbol, "5")
        self.assertEqual(cell.candidates, ["1", "2", "3"])

    def test_init_with_required_parameters_only(self):
        """Test that Cell initializes correctly with only required parameters."""
        cell = Cell(row=5, col=3, box=1)
        self.assertEqual(cell.row, 5)
        self.assertEqual(cell.col, 3)
        self.assertEqual(cell.box, 1)
        self.assertIsNone(cell.symbol)
        self.assertIsNone(cell.candidates)

    def test_init_with_symbol_only(self):
        """Test that Cell initializes correctly with symbol but no candidates."""
        cell = Cell(row=2, col=4, box=0, symbol="9")
        self.assertEqual(cell.symbol, "9")
        self.assertIsNone(cell.candidates)

    def test_init_with_candidates_only(self):
        """Test that Cell initializes correctly with candidates but no symbol."""
        cell = Cell(row=1, col=1, box=1, candidates=["4", "5", "6"])
        self.assertIsNone(cell.symbol)
        self.assertEqual(cell.candidates, ["4", "5", "6"])
