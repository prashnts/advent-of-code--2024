import heapq
import os

from functools import cache
from collections import namedtuple, defaultdict

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''.strip()

with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

def parse_data(data: str):
    patts, designs = data.split('\n\n')
    patterns = defaultdict(list)

    for p in patts.split(', '):
        patterns[p[0]].append(p)

    return patterns, designs.splitlines()


def solve(data: str):
    patterns, designs = parse_data(data)

    @cache
    def validate(design: str):
        if not design:
            return 1
        sum = 0
        for p in patterns.get(design[0], []):
            if design[:len(p)] == p:
                sum += validate(design[len(p):])
        return sum
    
    yield sum(bool(validate(d)) for d in designs)
    yield sum(validate(d) for d in designs)


if __name__=='__main__':
    test = solve(TEST_DATA)
    assert next(test) == 6
    assert next(test) == 16

    run = solve(INPUT)
    print(next(run))
    print(next(run))