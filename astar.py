import numpy


obstacles = numpy.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
])


class Node(object):
    def __init__(self, x, y, direction, cost):
        self.direction = direction
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.cost = cost
        # self.state = state


class AStar(object):
    def __init__(self, startx, starty, direction, endx, endy, costs):
        self.opened = []
        self.closed = []
        self.cells = []
        directions = ['N', 'E', 'W', 'S']
        for y in range(10):
            self.cells.append([])
            for x in range(10):
                self.cells[y].append([])
                for d in range(4):
                    self.cells[y][x].append(
                        Node(x, y, directions[d], costs[y][x])
                    )
        self.start = self.get_cell(startx, starty, direction)
        self.end = self.get_cell(endx, endy, direction)

    def get_heuristic(self, cell):
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)

    def get_cell(self, x, y, direction):
        if direction == 'N':
            return self.cells[y][x][0]
        if direction == 'E':
            return self.cells[y][x][1]
        if direction == 'W':
            return self.cells[y][x][2]
        if direction == 'S':
            return self.cells[y][x][3]

    def get_adjacent_cells(self, cell):
        cells = []

        if cell.direction == 'N':
            if cell.y > 0 and obstacles[cell.y - 1][cell.x] == 0:
                cells.append(self.get_cell(cell.x, cell.y - 1, cell.direction))
            cells.append(self.get_cell(cell.x, cell.y, 'E'))
            cells.append(self.get_cell(cell.x, cell.y, 'W'))
        elif cell.direction == 'W':
            if cell.x > 0 and obstacles[cell.y][cell.x - 1] == 0:
                cells.append(self.get_cell(cell.x - 1, cell.y, cell.direction))
            cells.append(self.get_cell(cell.x, cell.y, 'N'))
            cells.append(self.get_cell(cell.x, cell.y, 'S'))
        elif cell.direction == 'E':
            if cell.x < 9 and obstacles[cell.y][cell.x + 1] == 0:
                cells.append(self.get_cell(cell.x + 1, cell.y, cell.direction))
            cells.append(self.get_cell(cell.x, cell.y, 'S'))
            cells.append(self.get_cell(cell.x, cell.y, 'N'))
        elif cell.direction == 'S':
            if cell.y < 9 and obstacles[cell.y + 1][cell.x] == 0:
                cells.append(self.get_cell(cell.x, cell.y + 1, cell.direction))
            cells.append(self.get_cell(cell.x, cell.y, 'N'))
            cells.append(self.get_cell(cell.x, cell.y, 'S'))

        return cells

    def display_path(self):
        cell = self.end

        path = []
        while cell is not self.start:
            path.append((cell.x, cell.y, cell.direction))
            cell = cell.parent
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        adj.g = cell.g + adj.cost
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        for y in range(10):
            for x in range(10):
                for d in range(4):
                    self.cells[y][x][d].h = \
                        self.get_heuristic(self.cells[y][x][d])

        cell = self.start

        self.opened.append((cell.f, cell))

        while len(self.opened):
            self.opened.sort(key=lambda tup: tup[0])
            key, cell = self.opened.pop(0)
            self.closed.append(cell)

            if cell == self.end:
                print('path: ')
                print(self.display_path())
                return self.display_path()

            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.g == 0:
                    adj_cell.g = adj_cell.cost + cell.g
                    adj_cell.parent = cell
                adj_cell.f = adj_cell.g + adj_cell.h
                if adj_cell not in self.closed:
                    self.opened.append((adj_cell.f, adj_cell))
