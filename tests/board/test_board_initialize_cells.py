import unittest

from sudoku.board import Board


class TestBoardInitializeCells(unittest.TestCase):
    """Test cases for the Board class initialize_cells method."""

    def test_cells_grid_structure_9x9(self):
        """Test that cells grid is correctly structured for 9x9 board."""
        board = Board()
        self.assertEqual(len(board.cells), 9)  # 9 rows
        for row in board.cells:
            self.assertEqual(len(row), 9)  # 9 columns per row

    def test_cells_grid_structure_4x4(self):
        """Test that cells grid is correctly structured for 4x4 board."""
        board = Board(symbols=["1", "2", "3", "4"])
        self.assertEqual(len(board.cells), 4)  # 4 rows
        for row in board.cells:
            self.assertEqual(len(row), 4)  # 4 columns per row

    def test_cells_have_correct_row_col_attributes(self):
        """Test that each cell has correct row and col attributes."""
        board = Board(symbols=["1", "2", "3", "4"])
        for row_idx, row in enumerate(board.cells):
            for col_idx, cell in enumerate(row):
                self.assertEqual(cell.row, row_idx)
                self.assertEqual(cell.col, col_idx)

    def test_cells_are_initially_empty(self):
        """Test that all cells are initialized as empty (no symbol or candidates)."""
        board = Board(symbols=["1", "2", "3", "4"])
        for row in board.cells:
            for cell in row:
                self.assertIsNone(cell.symbol)
                self.assertIsNone(cell.candidates)

    def test_rows_dictionary_structure_9x9(self):
        """Test that rows dictionary contains all cells grouped by row."""
        board = Board()
        self.assertEqual(len(board.rows), 9)  # 9 rows

        for row_idx in range(9):
            self.assertIn(row_idx, board.rows)
            self.assertEqual(len(board.rows[row_idx]), 9)  # 9 cells per row

            # Verify all cells in this row have the correct row index
            for cell in board.rows[row_idx]:
                self.assertEqual(cell.row, row_idx)

    def test_cols_dictionary_structure_9x9(self):
        """Test that cols dictionary contains all cells grouped by column."""
        board = Board()
        self.assertEqual(len(board.cols), 9)  # 9 columns

        for col_idx in range(9):
            self.assertIn(col_idx, board.cols)
            self.assertEqual(len(board.cols[col_idx]), 9)  # 9 cells per column

            # Verify all cells in this column have the correct col index
            for cell in board.cols[col_idx]:
                self.assertEqual(cell.col, col_idx)

    def test_boxes_dictionary_structure_9x9(self):
        """Test that boxes dictionary contains all cells grouped by box."""
        board = Board()  # 9x9 with 3x3 boxes = 9 boxes
        self.assertEqual(len(board.boxes), 9)  # 9 boxes

        # Each box should have 9 cells (3x3)
        for box_idx in range(9):
            self.assertIn(box_idx, board.boxes)
            self.assertEqual(len(board.boxes[box_idx]), 9)

            # Verify all cells in this box have the correct box index
            for cell in board.boxes[box_idx]:
                self.assertEqual(cell.box, box_idx)

    def test_box_calculation_9x9(self):
        """Test that box indices are calculated correctly for 9x9 board (3x3 boxes)."""
        board = Board()
        # For 9x9 with num_bands=3, num_stacks=3:
        # Box 0: rows 0-2, cols 0-2
        # Box 1: rows 0-2, cols 3-5
        # Box 2: rows 0-2, cols 6-8
        # Box 3: rows 3-5, cols 0-2
        # Box 4: rows 3-5, cols 3-5
        # Box 5: rows 3-5, cols 6-8
        # Box 6: rows 6-8, cols 0-2
        # Box 7: rows 6-8, cols 3-5
        # Box 8: rows 6-8, cols 6-8

        # Test box 0 (top-left)
        self.assertEqual(board.cells[0][0].box, 0)
        self.assertEqual(board.cells[1][2].box, 0)
        self.assertEqual(board.cells[2][1].box, 0)

        # Test box 1 (top-middle)
        self.assertEqual(board.cells[0][3].box, 1)
        self.assertEqual(board.cells[1][4].box, 1)
        self.assertEqual(board.cells[2][5].box, 1)

        # Test box 2 (top-right)
        self.assertEqual(board.cells[0][8].box, 2)
        self.assertEqual(board.cells[1][7].box, 2)
        self.assertEqual(board.cells[2][6].box, 2)

        # Test box 3 (middle-left)
        self.assertEqual(board.cells[3][0].box, 3)
        self.assertEqual(board.cells[4][2].box, 3)
        self.assertEqual(board.cells[5][1].box, 3)

        # Test box 4 (middle-middle)
        self.assertEqual(board.cells[3][3].box, 4)
        self.assertEqual(board.cells[4][4].box, 4)
        self.assertEqual(board.cells[5][5].box, 4)

        # Test box 5 (middle-right)
        self.assertEqual(board.cells[3][8].box, 5)
        self.assertEqual(board.cells[4][7].box, 5)
        self.assertEqual(board.cells[5][6].box, 5)

        # Test box 6 (bottom-left)
        self.assertEqual(board.cells[6][0].box, 6)
        self.assertEqual(board.cells[7][2].box, 6)
        self.assertEqual(board.cells[8][1].box, 6)

        # Test box 7 (bottom-middle)
        self.assertEqual(board.cells[6][3].box, 7)
        self.assertEqual(board.cells[7][4].box, 7)
        self.assertEqual(board.cells[8][5].box, 7)

        # Test box 8 (bottom-right)
        self.assertEqual(board.cells[6][8].box, 8)
        self.assertEqual(board.cells[7][7].box, 8)
        self.assertEqual(board.cells[8][6].box, 8)

    def test_box_calculation_4x4(self):
        """Test that box indices are calculated correctly for 4x4 board (2x2 boxes)."""
        board = Board(symbols=["1", "2", "3", "4"])
        # For 4x4 with num_bands=2, num_stacks=2:
        # Box 0: rows 0-1, cols 0-1
        # Box 1: rows 0-1, cols 2-3
        # Box 2: rows 2-3, cols 0-1
        # Box 3: rows 2-3, cols 2-3

        # Test box 0 (top-left)
        self.assertEqual(board.cells[0][0].box, 0)
        self.assertEqual(board.cells[0][1].box, 0)
        self.assertEqual(board.cells[1][0].box, 0)
        self.assertEqual(board.cells[1][1].box, 0)

        # Test box 1 (top-right)
        self.assertEqual(board.cells[0][2].box, 1)
        self.assertEqual(board.cells[0][3].box, 1)
        self.assertEqual(board.cells[1][2].box, 1)
        self.assertEqual(board.cells[1][3].box, 1)

        # Test box 2 (bottom-left)
        self.assertEqual(board.cells[2][0].box, 2)
        self.assertEqual(board.cells[2][1].box, 2)
        self.assertEqual(board.cells[3][0].box, 2)
        self.assertEqual(board.cells[3][1].box, 2)

        # Test box 3 (bottom-right)
        self.assertEqual(board.cells[2][2].box, 3)
        self.assertEqual(board.cells[2][3].box, 3)
        self.assertEqual(board.cells[3][2].box, 3)
        self.assertEqual(board.cells[3][3].box, 3)

    def test_box_calculation_6x6(self):
        """Test that box indices are calculated correctly for 6x6 board."""
        board = Board(symbols=["1", "2", "3", "4", "5", "6"])
        # For 6x6 with num_bands=2, num_stacks=3:
        # Box 0: rows 0-2, cols 0-1
        # Box 1: rows 0-2, cols 2-3
        # Box 2: rows 0-2, cols 4-5
        # Box 3: rows 3-5, cols 0-1
        # Box 4: rows 3-5, cols 2-3
        # Box 5: rows 3-5, cols 4-5

        # Test box 0
        self.assertEqual(board.cells[0][0].box, 0)
        self.assertEqual(board.cells[1][1].box, 0)
        self.assertEqual(board.cells[2][1].box, 0)

        # Test box 1
        self.assertEqual(board.cells[0][2].box, 1)
        self.assertEqual(board.cells[1][3].box, 1)
        self.assertEqual(board.cells[2][2].box, 1)

        # Test box 2
        self.assertEqual(board.cells[0][4].box, 2)
        self.assertEqual(board.cells[1][5].box, 2)
        self.assertEqual(board.cells[2][5].box, 2)

        # Test box 3
        self.assertEqual(board.cells[3][0].box, 3)
        self.assertEqual(board.cells[4][1].box, 3)
        self.assertEqual(board.cells[5][0].box, 3)

        # Test box 4
        self.assertEqual(board.cells[3][2].box, 4)
        self.assertEqual(board.cells[4][2].box, 4)
        self.assertEqual(board.cells[5][3].box, 4)

        # Test box 5
        self.assertEqual(board.cells[3][4].box, 5)
        self.assertEqual(board.cells[4][5].box, 5)
        self.assertEqual(board.cells[5][4].box, 5)

    def test_each_cell_appears_in_exactly_one_row(self):
        """Test that each cell appears in exactly one row dictionary entry."""
        board = Board(symbols=["1", "2", "3", "4"])
        all_cells = []
        for row_cells in board.rows.values():
            all_cells.extend(row_cells)

        # Should have exactly size*size cells
        self.assertEqual(len(all_cells), board.size * board.size)

        # Each cell should appear exactly once
        self.assertEqual(len(all_cells), len(set(all_cells)))

    def test_each_cell_appears_in_exactly_one_column(self):
        """Test that each cell appears in exactly one column dictionary entry."""
        board = Board(symbols=["1", "2", "3", "4"])
        all_cells = []
        for col_cells in board.cols.values():
            all_cells.extend(col_cells)

        # Should have exactly size*size cells
        self.assertEqual(len(all_cells), board.size * board.size)

        # Each cell should appear exactly once
        self.assertEqual(len(all_cells), len(set(all_cells)))

    def test_each_cell_appears_in_exactly_one_box(self):
        """Test that each cell appears in exactly one box dictionary entry."""
        board = Board(symbols=["1", "2", "3", "4"])
        all_cells = []
        for box_cells in board.boxes.values():
            all_cells.extend(box_cells)

        # Should have exactly size*size cells
        self.assertEqual(len(all_cells), board.size * board.size)

        # Each cell should appear exactly once
        self.assertEqual(len(all_cells), len(set(all_cells)))

    def test_cells_grid_matches_row_dictionary(self):
        """Test that cells grid and rows dictionary reference the same Cell objects."""
        board = Board(symbols=["1", "2", "3", "4"])
        for row_idx, row in enumerate(board.cells):
            for col_idx, cell in enumerate(row):
                # The cell in the grid should be the same object as in the rows dict
                self.assertIs(cell, board.rows[row_idx][col_idx])

    def test_cells_grid_matches_col_dictionary(self):
        """Test that cells grid and cols dictionary reference the same Cell objects."""
        board = Board(symbols=["1", "2", "3", "4"])
        for row_idx, row in enumerate(board.cells):
            for col_idx, cell in enumerate(row):
                # The cell in the grid should be the same object as in the cols dict
                self.assertIs(cell, board.cols[col_idx][row_idx])
