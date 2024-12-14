import re
import os
from tqdm import tqdm
from collections import defaultdict
from functools import cache

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

def parse_data(data: str):
    pattern = r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)'

    for l in data.splitlines():
        px, py, vx, vy = map(int, re.match(pattern, l).groups())
        yield (px, py), (vx, vy)


@cache
def simulate(p, v, x_max, y_max, steps):
    for _ in range(steps):
        n_p = (p[0] + v[0], p[1] + v[1])
        if n_p[0] < 0:
            n_p = (x_max + n_p[0], n_p[1])
        if n_p[1] < 0:
            n_p = (n_p[0], y_max + n_p[1])
        if n_p[0] >= x_max:
            n_p = (n_p[0] - x_max, n_p[1])
        if n_p[1] >= y_max:
            n_p = (n_p[0], n_p[1] - y_max)
        p = n_p
    return p


def print_board(positions, x_max, y_max):
    board = [['.' for _ in range(x_max)] for _ in range(y_max)]

    for p in positions:
        board[p[1]][p[0]] = '#'

    return '\n'.join(''.join(row) for row in board)

def safety_factor(data: str, x_max: int, y_max: int):
    factors = defaultdict(int)

    for p, v in parse_data(data):
        pos = simulate(p, v, x_max, y_max, 100)
        factors[pos] += 1

    quadrants = [
        ((0, 0), (x_max // 2, y_max // 2)),
        ((x_max // 2 + 1, 0), (x_max, y_max // 2)),
        ((0, y_max // 2 + 1), (x_max // 2 , y_max)),
        ((x_max // 2 + 1, y_max // 2 + 1), (x_max, y_max)),
    ]

    items_in_quads = [[], [], [], []]

    for pos, count in factors.items():
        for i, q in enumerate(quadrants):
            if q[0][0] <= pos[0] < q[1][0] and q[0][1] <= pos[1] < q[1][1]:
                items_in_quads[i].append(count)

    yield sum(items_in_quads[0]) * sum(items_in_quads[1]) * sum(items_in_quads[2]) * sum(items_in_quads[3])

    pos_vel = [(p, v) for p, v in parse_data(data)]

    for i in range(0, 9000):
        factors = defaultdict(int)
        next_pos = []

        for p, v in pos_vel:
            pos = simulate(p, v, x_max, y_max, 1)
            factors[pos] += 1
            next_pos.append((pos, v))
        
        pos_vel = next_pos

        board = print_board(factors.keys(), x_max, y_max)

        if match := re.search(r'(#{4,})', board):
            if len(match.group(1)) >= 8:
                print("STEP: ", i + 1)
                print(board)
                yield i + 1
                break

if __name__=='__main__':
    test = safety_factor(TEST_DATA, 11, 7)
    assert next(test) == 12

    run = safety_factor(INPUT, 101, 103)
    print(next(run))
    print(next(run))