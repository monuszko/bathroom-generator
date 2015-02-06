#! /usr/bin/env python3
import random
from re import match

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

RULES = {
        # Creates nice cavern-like organic shapes:
        'Vote': '45678/5678',
        'Vote 4/5': '35678/4678',
        # Creates mazes:
        'Maze': '12345/3',
        # Like above, walls tend to be longer:
        'Mazecetric': '1234/3',
        # The remaining rules are mostly for fun:
        'Game of Life': '23/2',
        'Gnarl': '1/1',
        'Replicator': '1357/1357',
        'Coral': '45678/3',#
        'Assimilation': '4567/345',
        'Diamoeba': '5678/35678',#
        '2x2': '125/36',
        'Move': '245/368',
        'Stains': '235678/3678',
        'Day & Night': '34678/3678',#
        'Coagulations': '235678/378',
        'Walled Cities': '2345/45678',
        'Fredkin': '02468/1357',
        'Seeds': '/2',
        'Live Free or Die': '0/2',
        'Amoeba': '1358/357',#
        'Life Without Death': '012345678/3',
        'Serviettes': '/234',
        }

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
        neighbors = [nei for nei in neighbors if len(board.neighbors(nei, value='.')) <= 1]
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


def cellular_automata(board, rulestring, reps=1, edges=' '):
    numbers = '0?1?2?3?4?5?6?7?8?'
    pattern = '({0}/{0}|S{0}/B{0}|B{0}/S{0})'.format(numbers)
    if not match(pattern, rulestring):
        print('Bad rulestring. The following formats are accepted:')
        print('23/2')
        print('S23/B2')
        print('B17/S12')

    if 'S' not in rulestring:
        survival, birth = rulestring.split('/')
    elif rulestring.startswith('S'):
        survival, birth = rulestring.strip('/')
    elif rulestring.startswith('B'):
        birth, survival = rulestring.strip('/')
    survival = tuple(int(letter) for letter in survival.strip('S'))
    birth = tuple(int(letter) for letter in birth.strip('B'))

    for c in board.fields:
        board.fields[c] = '#' if random.random() <= 0.50 else ' '

    for i in range(reps):
        print('Generation ', i+1)
        board.display()
        last_generation = board.fields.copy()
        for coords in last_generation:
            nearby = board.neighbors(coords)
            missing_fields = 8 - len(nearby)
            nearby = sum(1 for n in nearby if last_generation[n] == '#')
            if edges == '#':
                nearby += missing_fields
            if last_generation[coords] == '#':
                if nearby not in survival:
                    board.fields[coords] = ' '
            elif last_generation[coords] == ' ':
                if nearby in birth:
                    board.fields[coords] = '#'

        # Progress ?
        if last_generation == board.fields:
            break

board = Board((51, 51))
#generate_depth_first(board)
#generate_prim(board)

cellular_automata(board, rulestring=RULES['Vote'], edges=' ', reps=5)

