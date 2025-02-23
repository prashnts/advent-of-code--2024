import os
from tqdm import tqdm
from itertools import cycle

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()


def parse_data(data: str):
    lines = data.splitlines()
    board = []
    for i, line in enumerate(lines):
        if '^' in line:
            x, y = line.index('^'), i
        board.append(list(line))
    return board, x, y


def visits(board, a, b):
    directions = cycle(['^', '>', 'v', '<'])

    visited = set()
    directional_visit = set()

    x, y = a, b
    direction = next(directions)

    while True:
        visited.add((x, y))
        dx, dy = {
            '^': (0, -1),
            '>': (1, 0),
            'v': (0, 1),
            '<': (-1, 0)
        }[direction]
        nx, ny = x + dx, y + dy
            
        if (x, y, direction) in directional_visit:
            raise TypeError("Looping")

        directional_visit.add((x, y, direction))

        try:
            if nx < 0 or ny < 0:
                raise IndexError
            if board[ny][nx] == '#':
                direction = next(directions)
                continue
            x, y = nx, ny
        except IndexError:
            break

    return len(visited)

def block_all(board, a, b):
    # Runs in about 40 secs on my machine
    obstructions = 0

    for y, row in tqdm(enumerate(board)):
        for x, cell in tqdm(enumerate(row)):
            if cell == '.':
                board[y][x] = '#'
                try:
                    visits(board, a, b)
                except TypeError:
                    obstructions += 1
                board[y][x] = '.'
    
    return obstructions
                    

if __name__=='__main__':
    board, a, b = parse_data(TEST_DATA)
    assert visits(board, a, b) == 41
    assert block_all(board, a, b) == 6

    board, a, b = parse_data(INPUT)
    print(visits(board, a, b))
    print(block_all(board, a, b))