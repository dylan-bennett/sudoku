import unittest

from sudoku.board import Cell


class TestCellRepr(unittest.TestCase):
    def test_repr_with_symbol(self):
        """Test that __repr__ returns correct format when cell has a symbol."""
        cell = Cell(row=3, col=7, box=2, symbol="8")
        self.assertEqual(repr(cell), "(3,7,2,8)")

    def test_repr_without_symbol(self):
        """Test that __repr__ returns correct format when cell is empty."""
        cell = Cell(row=0, col=0, box=0)
        self.assertEqual(repr(cell), "(0,0,0,None)")
