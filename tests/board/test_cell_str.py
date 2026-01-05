import unittest

from sudoku.board import Cell


class TestCellStr(unittest.TestCase):
    def test_str_with_symbol(self):
        """Test that __str__ returns the symbol when cell has a value."""
        cell = Cell(row=1, col=2, box=3, symbol="7")
        self.assertEqual(str(cell), "7")

    def test_str_without_symbol(self):
        """Test that __str__ returns a space when cell is empty."""
        cell = Cell(row=1, col=2, box=3)
        self.assertEqual(str(cell), " ")

    def test_str_with_string_symbol(self):
        """Test that __str__ works with string symbols."""
        cell = Cell(row=0, col=0, box=0, symbol="A")
        self.assertEqual(str(cell), "A")

    def test_str_with_numeric_symbol(self):
        """Test that __str__ converts numeric symbols to strings."""
        # Note: The symbol is stored as-is, so if passed as int, it stays int
        # But __str__ should still work via f-string conversion
        cell = Cell(row=0, col=0, box=0, symbol=5)
        self.assertEqual(str(cell), "5")
