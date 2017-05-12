import sys

from generator import Maze

USAGE = """
Usage: python example.py GRID_SIZE CELL_SIZE RANDOMNESS SPARSENESS DEADENDS_TO_REMOVE NB_ROOMS"""

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print USAGE
        sys.exit(0)

    width = int(sys.argv[1])
    height = width
    size = int(sys.argv[2])
    maze = Maze(width, height)
    maze.create(randomness=float(sys.argv[3]))
    maze.draw(filename='assets/1.basic.png', size=size)

    maze.make_sparse(sparseness_ratio=float(sys.argv[4]))
    maze.draw(filename='assets/2.sparse.png', size=size)

    maze.close_deadends(randomness=float(sys.argv[3]),
                        deadends_to_close=float(sys.argv[5]))
    maze.draw(filename='assets/3.closed.png', size=size)

    maze.double()
    maze.draw(filename='assets/4.doubled.png', size=size)

    room_width = (int(width*0.3), int(width*0.7))
    room_height = (int(height*0.3), int(height*0.7))
    maze.add_rooms(int(sys.argv[6]), room_width, room_height)
    maze.draw(filename='assets/5.rooms.png', size=size)
