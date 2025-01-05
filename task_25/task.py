import os
from itertools import product

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
'''.strip()

with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()


def parse_data(data: str):
    lks = data.split('\n\n')
    keys = []
    locks = []

    for line in lks:
        l = line.splitlines()
        rows = list(zip(*l))
        pat = [r.count('#') - 1 for r in rows]

        if l[0] == '#####':
            locks.append(pat)
        else:
            keys.append(pat)
    return keys, locks

def solve(data: str):
    keys, locks = parse_data(data)
    combinations = product(keys, locks)
    sum = 0

    for k, l in combinations:
        if all([(a + b) <= 5 for a, b in zip(k, l)]):
            sum += 1

    yield sum
    yield 0


if __name__=='__main__':
    test = solve(TEST_DATA)
    assert next(test) == 3

    run = solve(INPUT)
    print(next(run))
