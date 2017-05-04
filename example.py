import sys

from generator import Maze

USAGE = """
Usage: python example.py GRID_SIZE CELL_SIZE RANDOMNESS SPARSENESS"""

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print USAGE
        sys.exit(0)

    width = int(sys.argv[1])
    height = width
    size = int(sys.argv[2])
    maze = Maze(width, height)
    maze.create(randomness=float(sys.argv[3]))
    maze.draw(filename='1.basic.png', size=size)

    maze.make_sparse(sparseness_ratio=float(sys.argv[4]))
    maze.draw(filename='2.sparse.png', size=size)

    maze.close_deadends(randomness=float(sys.argv[3]))
    maze.draw(filename='3.closed.png', size=size)

