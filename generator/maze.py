import random

from PIL import Image

from . import genutils


class Maze(object):

    DIRECTIONS = {
        'N': lambda c: (c[0], c[1]-1),
        'E': lambda c: (c[0]+1, c[1]),
        'S': lambda c: (c[0], c[1]+1),
        'W': lambda c: (c[0]-1, c[1]),
    }

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = {
            (x, y): set()
            for y in range(h)
            for x in range(w)
        }
        self.deadends = set()

    def close_deadends(self, randomness=1.0):
        """
        Close dead end cells by joining them back to existing cells
        Args:
            randomness (float): percentage of how often the direction
                                of a corridor changes
        """

        while self.deadends:
            cell = self.deadends.pop()
            done = False
            direction = 'W'

            # done when the deadends joined a corridor
            while not done:
                valid = False
                directions = set(self.DIRECTIONS.keys())

                # valid when we find an unvisited cells that is not a wall
                while not valid and directions:
                    directions.discard(direction)
                    next_cell = self.DIRECTIONS[direction](cell)

                    # not a neighbor already and in the bounds
                    if (next_cell not in self.data[cell] and self.data.get(next_cell) is not None):
                        self.deadends.discard(cell)
                        self.data[cell].add(next_cell)

                        # not a neighbor and is visited, we stop
                        if self.data.get(next_cell):
                            self.data[next_cell].add(cell)
                            self.deadends.discard(next_cell)
                            done = True
                            break

                        # not a neighbor and not visited, we add it
                        else:
                            self.data[next_cell].add(cell)
                            self.deadends.add(next_cell)
                            cell = next_cell
                            valid = True
                            break
                    else:
                        direction = next(iter(directions))

                # take a chance and see if we should change direction
                if genutils.chance(randomness):
                    direction = random.choice(self.DIRECTIONS.keys())

    def make_sparse(self, sparseness_ratio=0.4):
        """
        Remove sparseness_ratio percentage of dead end cells
        Args:
            sparseness_ratio (float): percentage of dead end cell to remove
        """

        sparseness = int(len(self.data) * sparseness_ratio)
        removed = set()
        while len(removed) < sparseness:
            for cell in self.data.keys():
                if len(self.data[cell]) == 1:
                    nb = self.data[cell].pop()
                    # remove the cell from its neighbor's neighbors
                    self.data[nb].discard(cell)
                    # if the neighbor is in turn a deadend, add it to the set
                    if len(self.data[nb]) == 1:
                        self.deadends.add(nb)

                    # disconnect the cell
                    self.data[cell] = set()
                    self.deadends.discard(cell)

                    removed.add(cell)

                if len(removed) >= sparseness:
                    break

    def create(self, randomness=1):
        """
        Create a perfect maze of size self.h*self.w
        Args:
            randomness (float): percentage of how often the direction
                                of a corridor changes
        """

        unvisited_cells = {
            (x, y)
            for y in range(self.h)
            for x in range(self.w)
        }

        cell = random.sample(unvisited_cells, 1)[0]
        unvisited_cells.discard(cell)
        visited_cells = [cell]
        direction = 'W'

        while unvisited_cells:
            valid = False
            directions = set(self.DIRECTIONS.keys())

            # valid when we find an unvisited cells that is not a wall
            while not valid and directions:
                directions.discard(direction)
                next_cell = self.DIRECTIONS[direction](cell)

                # if not a wall and unvisited
                if self.data.get(next_cell) is not None and next_cell in unvisited_cells:
                    valid = True
                    break
                elif directions:
                    direction = next(iter(directions))

            # take a chance and see if we should change direction
            if genutils.chance(randomness):
                direction = random.choice(self.DIRECTIONS.keys())

            if valid:
                # connect the cell with its neighbor
                self.data[cell].add(next_cell)
                self.data[next_cell].add(cell)
                visited_cells.append(next_cell)
                unvisited_cells.discard(next_cell)
                cell = next_cell
            else:
                # try again from an other visited cell
                cell = genutils.random_choice(visited_cells, cell)

    def _ascii(self, size=5):
        """
        // Debug func to have a visual of the tree //

        Create a ASCII representation of the maze tree in a 2D map
        Returns:
            list(list(char))
        """

        def draw_cell(x, y):
            x = x*size
            y = y*size
            for j in range(size):
                for i in range(size):
                    art[y+j][x+i] = ' '

        art = [
            ['#' for _ in range((self.w*2+1)*size)]
            for __ in range((self.h*2+1)*size)
        ]
        for y in range(self.h):
            for x in range(self.w):
                cell = (x, y)
                for neighbor in self.data[cell]:
                    xmin = min(x*2+1, neighbor[0]*2+1)
                    xmax = max(x*2+1, neighbor[0]*2+1)
                    for i in range(xmin, xmax):
                        draw_cell(y=y*2+1, x=i)

                    ymin = min(y*2+1, neighbor[1]*2+1)
                    ymax = max(y*2+1, neighbor[1]*2+1)
                    for j in range(ymin, ymax):
                        draw_cell(y=j, x=x*2+1)

                if self.data[cell]:
                    draw_cell(y=y*2+1, x=x*2+1)

        return art

    def draw(self, size=5, filename=None):
        """
        // Debug func to have a visual of the tree //

        Draw the maze tree in a Pillow image and save it if filename isn't None
        Args:
            size (int): size of each cell in pixels
            filename (str): filename of image to be saved
        """

        img = Image.new('RGB', ((self.w*2+1)*size, (self.h*2+1)*size), "black")
        art = [
            {'#': (0, 0, 0), ' ': (255, 255, 255)}[c]
            for row in self._ascii(size=size)
            for c in row
        ]
        img.putdata(art)

        if filename:
            img.save(filename)
        else:
            img.show()
