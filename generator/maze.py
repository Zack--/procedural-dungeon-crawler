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
            (x, y): {'neighbors': set(), 'type': 'void'}
            for y in range(h)
            for x in range(w)
        }
        self.deadends = set()
        self.rooms = {}

    def place_room(self, corner, width, height):
        (x, y) = corner

        self.rooms[corner] = {'width': width, 'height': height, 'doors': set()}

        cells = []

        for j in range(height):
            for i in range(width):
                cell = (x+i, y+j)
                cells.append(cell)
                for (xd, yd) in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                    nb = (cell[0]+xd, cell[1]+yd)
                    if self.data.get(nb) is not None:
                        if x <= nb[0] < x+width and y <= nb[1] < y+height:
                            self.data[cell]['type'] = 'room'
                            self.data[nb]['neighbors'].add(cell)
                            self.data[cell]['neighbors'].add(nb)

                        # add door to every connected corridor
                        elif self.data[nb]['neighbors']:
                            self.data[nb]['neighbors'].add(cell)
                            self.data[cell]['neighbors'].add(nb)
                            self.rooms[corner]['doors'].add((nb, cell))

    def add_rooms(self, n_rooms, room_width, room_height, ratio=None):
        while n_rooms:
            n_rooms -= 1
            width = genutils.randint(*room_width)
            height = genutils.randint(*room_height)
            best_pos = None
            for y in range(self.h - height):
                for x in range(self.w - width):
                    c = (x, y)
                    score = 0
                    for j in range(height):
                        for i in range(width):
                            cell = (x+i, y+j)

                            if self.data[cell]['type'] == 'corridor':
                                score += 3

                            elif self.data[cell]['type'] == 'room':
                                score += 100

                            score += sum(map(lambda c: not not self.data.get(c, {}).get('neighbors'),
                                             [(cell[0]+1, cell[1]),
                                              (cell[0]-1, cell[1]),
                                              (cell[0], cell[1]+1),
                                              (cell[0], cell[1]-1)]))
                    if best_pos is None or 0 < score < best_pos[0]:
                        best_pos = (score, c)

            self.place_room(best_pos[1], width, height)

    def close_deadends(self, randomness=1.0, deadends_to_close=None):
        """
        Close dead end cells by joining them back to existing cells
        Args:
            deadends_to_close (float): percentage of dead ends to
                                       loop back to a corridor
            randomness (float): percentage of how often the direction
                                of a corridor changes
        """

        if deadends_to_close is None:
            deadends_to_close = 1
        n_deadends_to_close = int(len(self.deadends) * deadends_to_close)

        while n_deadends_to_close and self.deadends:
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

                    # not a connected neighbor and in the bounds
                    if (next_cell not in self.data[cell]['neighbors'] and self.data.get(next_cell) is not None):
                        self.deadends.discard(cell)
                        self.data[cell]['neighbors'].add(next_cell)
                        self.data[next_cell]['type'] = 'corridor'
                        self.data[cell]['type'] = 'corridor'

                        # neighbor is already connected to other cell
                        if self.data[next_cell]['neighbors']:
                            self.data[next_cell]['neighbors'].add(cell)
                            self.deadends.discard(next_cell)
                            done = True
                            n_deadends_to_close -= 1
                            break

                        # otherwise it was previously a wall
                        # carve a corridor and it becomes a deadend
                        else:
                            self.data[next_cell]['neighbors'].add(cell)
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
                if len(self.data[cell]['neighbors']) == 1:
                    nb = self.data[cell]['neighbors'].pop()

                    # remove the cell from its neighbor's neighbors
                    self.data[nb]['neighbors'].discard(cell)

                    # if the neighbor is in turn a deadend, add it to the set
                    if len(self.data[nb]['neighbors']) == 1:
                        self.deadends.add(nb)

                    # disconnect the cell
                    self.data[cell]['neighbors'] = set()
                    self.data[cell]['type'] = 'void'
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
                self.data[cell]['neighbors'].add(next_cell)
                self.data[cell]['type'] = 'corridor'
                self.data[next_cell]['neighbors'].add(cell)
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

        def draw_cell(x, y, node=' '):
            x = x*size
            y = y*size
            for j in range(size):
                for i in range(size):
                    art[y+j][x+i] = node

        def draw_region(top_left, lower_right):
            for j in range(top_left[1], lower_right[1]):
                for i in range(top_left[0], lower_right[0]):
                    draw_cell(i, j, node='r')

        art = [
            ['#' for _ in range((self.w*2+1)*size)]
            for __ in range((self.h*2+1)*size)
        ]
        for y in range(self.h):
            for x in range(self.w):
                cell = (x, y)
                for neighbor in self.data[cell]['neighbors']:
                    xmin = min(x*2+1, neighbor[0]*2+1)
                    xmax = max(x*2+1, neighbor[0]*2+1)
                    for i in range(xmin, xmax):
                        draw_cell(y=y*2+1, x=i, node='c')

                    ymin = min(y*2+1, neighbor[1]*2+1)
                    ymax = max(y*2+1, neighbor[1]*2+1)
                    for j in range(ymin, ymax):
                        draw_cell(y=j, x=x*2+1, node='c')

                if self.data[cell]['neighbors']:
                    draw_cell(y=y*2+1, x=x*2+1, node='c')

        for tl_corner in self.rooms:
            lr_corner = (
                tl_corner[0] + self.rooms[tl_corner]['width'],
                tl_corner[1] + self.rooms[tl_corner]['height'])
            tl_corner = (tl_corner[0]*2+1, tl_corner[1]*2+1)
            lr_corner = (lr_corner[0]*2+1, lr_corner[1]*2+1)
            draw_region(tl_corner, lr_corner)

        return art

    def double(self):
        self.h = self.h*2
        self.w = self.w*2
        doubled = {
            (x, y): {'neighbors': set(), 'type': 'void'}
            for y in range(self.h)
            for x in range(self.w)
        }
        double = lambda x: (x[0] * 2, x[1] * 2)

        for c in self.data:
            dc = double(c)
            for nb in self.data[c]['neighbors']:
                dnb = double(nb)
                inbetween_cell = (dc[0] + (((dc[0]-dnb[0]) / 2) * -1),
                                  dc[1] + (((dc[1]-dnb[1]) / 2) * -1))
                doubled[dc]['neighbors'].add(inbetween_cell)
                doubled[dc]['neighbors'].add(dnb)
                doubled[inbetween_cell]['neighbors'].add(dnb)
                doubled[inbetween_cell]['neighbors'].add(dc)

                doubled[dc]['type'] = self.data[c]['type']
                doubled[inbetween_cell]['type'] = self.data[c]['type']

        self.data = doubled

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
            {'#': (0, 0, 0), 'c': (255, 255, 255), 'r': (0, 255, 255)}[c]
            for row in self._ascii(size=size)
            for c in row
        ]
        img.putdata(art)

        if filename:
            img.save(filename)
        else:
            img.show()
