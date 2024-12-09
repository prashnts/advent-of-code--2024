import os
from collections import defaultdict
from itertools import combinations

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

def parse_data(data: str):
    board = defaultdict(list)
    for y, line in enumerate(data.splitlines()):
        for x, cell in enumerate(line):
            if not cell == '.':
                board[cell].append((x, y))
    return board, x, y

def antinodes(a, b):
    v = (b[0] - a[0], b[1] - a[1])
    v_s = (v[0] ** 2 + v[1] ** 2) ** 0.5
    u = (v[0] / v_s, v[1] / v_s)

    d1 = -1 * v_s
    d2 = -2 * v_s

    p1 = (int(a[0] - d1 * u[0]), int(a[1] - d1 * u[1]))
    p2 = (int(a[0] - d2 * u[0]), int(a[1] - d2 * u[1]))

    return p2[::1], p1[::1]

def check_distance(pt, a, b):
    distance = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5

    dab = distance(a, b)
    dpa = distance(pt, a)
    dpb = distance(pt, b)

    if dab * 2 == dpa or dab * 2 == dpb:
        return True

def print_board(board, x_max, y_max, nodes):
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            if (x, y) in nodes:
                print('X', end='')
                continue
            for k, v in board.items():
                if (x, y) in v:
                    print(k, end='')
                    break
            else:
                print('.', end='')
        print()


def radio(data: str):
    board, x_max, y_max = parse_data(data)
    nodes = set()

    bounded = lambda x, y: 0 <= x <= x_max and 0 <= y <= y_max

    for antenna, coords in board.items():
        for a, b in combinations(coords, 2):
            anodes = [*antinodes(b, a)]
            for n in anodes:
                if bounded(*n) and check_distance(n, a, b):
                    nodes.add(n)
    
    print(nodes, len(nodes))
    print_board(board, x_max, y_max, nodes)

    yield len(nodes)

if __name__=='__main__':
    test = radio(TEST_DATA)
    assert next(test) == 14
    # assert next(test) == 11387

    run = radio(INPUT)
    print(next(run))
    # print(next(run))