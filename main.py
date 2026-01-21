from sudoku import Sudoku


def main():
    sudoku = Sudoku(symbols="PYTHON", difficulty="expert")
    print(sudoku.ascii)
    print(sudoku)


if __name__ == "__main__":
    main()
