from Board import Board
from engines.Solver import Solver


def main():
    DEBUG = False
    board = Board(range(1, 7))
    solver = Solver(board, DEBUG=DEBUG)
    solver.solve_backtrack()
    print(board.ascii)


if __name__ == "__main__":
    main()
