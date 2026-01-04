from Board import Board
from engines.Solver import Solver


def main():
    DEBUG = False

    # Create our empty board
    board = Board(range(1, 7))

    # Solve it in order to fill it out
    solver = Solver(board, DEBUG=DEBUG)
    solver.solve_backtrack()

    print(board.ascii)


if __name__ == "__main__":
    main()
