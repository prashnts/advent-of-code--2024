import os
from collections import defaultdict
from itertools import combinations, permutations

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

def parse_data(data: str):
    board = {}
    trailheads = []
    for y, line in enumerate(data.splitlines()):
        for x, cell in enumerate(line):
            if cell == '.':
                continue
            c = int(cell)
            if c == 0:
                trailheads.append((x, y))
            board[(x, y)] = c
    return board, trailheads

def find_trails(board, head, allow_paths=False):
    def neighbors(x, y):
        cells = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        for c in cells:
            if c in board and board[c] == board[(x, y)] + 1:
                yield c

    def trails(node, path):
        path.append(node)

        if board[node] == 9:
            yield path

        for cell in neighbors(*node):
            if not allow_paths and cell in path:
                continue
            yield from trails(cell, path)
        else:
            yield None

    yield from trails(head, [])


def trail_count(data: str):
    board, trailheads = parse_data(data)

    sum_a = 0
    sum_b = 0

    for head in trailheads:
        distinct_trails = {tuple(t) for t in find_trails(board, head) if t}
        sum_a += len(distinct_trails)
        distinct_paths = {tuple(t) for t in find_trails(board, head, True) if t}
        sum_b += len(distinct_paths)

    yield sum_a
    yield sum_b

if __name__=='__main__':
    test = trail_count(TEST_DATA)
    assert next(test) == 36
    assert next(test) == 81

    run = trail_count(INPUT)
    print(next(run))
    print(next(run))