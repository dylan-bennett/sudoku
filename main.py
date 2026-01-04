from Board import Board
from engines.Solver import Solver


def main():
    DEBUG = False

    # Create our empty board
    board = Board(range(1, 7))

    # Solve it in order to fill it out
    solver = Solver(board, DEBUG=DEBUG)
    solved = solver.solve_backtrack()

    # If it was properly solved, then all of the cells are filled so all of their candidate lists can be emptied
    if solved:
        for row in board.cells:
            for cell in row:
                cell.candidates = []

    print(board.ascii)


if __name__ == "__main__":
    main()
