from sudoku.board import Board
from sudoku.engines.solver import Solver


def main():
    DEBUG = False

    board = Board()
    board.seed_empty_board()

    solver = Solver(board, DEBUG=DEBUG)
    solver.solve()

    print(board.ascii)


if __name__ == "__main__":
    main()
