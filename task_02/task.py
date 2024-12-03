import os

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()


def parse_data(data: str) -> list[list[int]]:
    return [list(map(int, l.split(' '))) for l in data.split('\n')]

def is_sort(d: list) -> str:
    if d == sorted(d):
        return True
    elif d == sorted(d, reverse=True):
        return True
    return False

def is_safe(d: list) -> bool:
    # safe if Any two adjacent levels differ by at least one and at most three.
    return all(0 < abs(x - y) <= 3 for x, y in zip(d, d[1:])) and is_sort(d)

def safety_report(data: str) -> int:
    reports = parse_data(data)
    return sum(is_safe(d) for d in reports)

def can_be_safe(r: list[int]) -> list[int] | None:
    # Probably a better way exists.
    # Eg. some emperical rules can be derived. For example if only one pair of equal
    # numbers exists, then one can be removed.
    for i in range(len(r)):
        if is_safe(r[:i] + r[i+1:]):
            return True
    return False

def dampened(data: str) -> int:
    reports = parse_data(data)
    accum = 0

    for r in reports:
        if is_safe(r):
            accum += 1
        elif can_be_safe(r):
            accum += 1
        
    return accum

if __name__=='__main__':
    assert safety_report(TEST_DATA) == 2
    assert dampened(TEST_DATA) == 4

    print(safety_report(INPUT))
    print(dampened(INPUT))