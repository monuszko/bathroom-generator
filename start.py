#! /usr/bin/env python3
import random

#TODO: colored mazes (news.ycombinator.com)

#Clockwise:
DIRECTIONS = (
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1)
        )

def chessboard_distance(point1, point2):
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))


class Board:
    def __init__(self, dimensions=None):
        """
        dimensions - (width, length)
        """
        self.fields = {}
        if dimensions:
            for x in range(dimensions[0]):
                for y in range(dimensions[1]):
                    self.fields[x, y] = '#'
            self.width = dimensions[0]
            self.height = dimensions[1]

    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.fields[x, y], end='')
            print()

    def neighbors(self, coords, value=None):
        neighbors = {}
        for di in DIRECTIONS:
            adjacent_coords = (coords[0] + di[0], coords[1] + di[1])
            neigh = self.fields.get(adjacent_coords, None)
            if neigh:
                if not value:
                    neighbors[adjacent_coords] = neigh
                elif value == neigh:
                    neighbors[adjacent_coords] = neigh
        return neighbors 

    def ball(self, coords, radius=1):
        result = ({coords})
        for n in range(radius):
            for field in result.copy():
                result.update(self.neighbors(field))
        return result

    def edges(self):
        edges = []
        for coords in self.fields:
            numdirs = len(DIRECTIONS)
            if len(self.neighbors(coords)) < numdirs:
                edges.append(coords)
        return edges



def generate_depth_first(board):
    exit = random.choice(board.edges()) 

    stack = [exit]

    while stack:
        curr = stack.pop()
        neighbors = list(board.neighbors(curr, value='#'))
        neighbors = [nei for nei in neighbors if len(board.neighbors(nei, value='.')) <= 2]
        if neighbors:
            adjac = random.choice(neighbors)
            stack.append(curr)
            stack.append(adjac)
            board.fields[adjac] = '.'

def generate_prim(board):
    for field in board.fields:
        board.fields[field] = '#'


    in_cells = set()
    frontier_cells = set()
    out_cells = ({cell for cell in board.fields})
    index = random.randint(0, len(out_cells) - 1)
    for nr, cell in enumerate(out_cells):
        if nr == index:
            break
    in_cells.add(cell)
    board.fields[cell] = '@'
    for nei in board.neighbors(cell):
        out_cells.remove(nei)
        frontier_cells.add(nei)

    while frontier_cells:
        index = random.randint(0, len(frontier_cells) - 1)
        for nr, cell in enumerate(frontier_cells):
            if nr == index:
                frontier_cells.remove(cell)
                break
        in_cells.add(cell)
        board.fields[cell] = '.'
        for nei in board.neighbors(cell):
            if nei in frontier_cells:
                frontier_cells.remove(nei)
                in_cells.add(nei)
            if nei in out_cells:
                out_cells.remove(nei)
                frontier_cells.add(nei)


def generate_cellullar_caves(board, reps=3, radius=1, edges='#'):
    for c in board.fields:
        board.fields[c] = '#' if random.random() <= 0.50 else '.'

    #TODO: 4/8/6 directions
    for i in range(reps):
        print('Generation ', i+1)
        board.display()
        before = (sum(1 for field in board.fields.values() if field == '#'))
        last_generation = board.fields.copy()

        allcells = [coords for coords in last_generation]
        for c in allcells:
            ball = board.ball(c, radius=radius)
            walls = sum(1 for b in ball if last_generation[b] == '#')
            expected_fields = pow(2 * radius + 1, 2)
            # Handle edges
            if edges == '#':
                walls += expected_fields - len(ball)
            board.fields[c] = '#' if walls >= expected_fields // 2 + 1 else '.'
        after = (sum(1 for field in board.fields.values() if field == '#'))
        # Progress ?
        if before == after:
            break


def game_of_life(board, reps=1):
    for c in board.fields:
        board.fields[c] = '#' if random.random() <= 0.20 else ' '
    for i in range(reps):
        print('Generation ', i+1)
        board.display()
        before = board.fields.copy() 
        last_generation = board.fields.copy()
        for coords in last_generation:
            nearby = len(board.neighbors(coords, value='#'))
            if last_generation[coords] == '#':
                if not 1 < nearby < 4:
                    board.fields[coords] = ' '
            elif last_generation[coords] == ' ':
                if nearby == 3:
                    board.fields[coords] = '#'
        after = board.fields.copy() 
        # Progress ?
        if before == after:
            break


board = Board((51, 51))
#generate_depth_first(board)
#generate_prim(board)

generate_cellullar_caves(board, edges='.', reps=8, radius=1)
#game_of_life(board, reps=50)

#board.display()
