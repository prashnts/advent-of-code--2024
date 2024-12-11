import os
from functools import cache

__here__ = os.path.dirname(__file__)

TEST_DATA = '125 17'
INPUT = '872027 227 18 9760 0 4 67716 9245696'


@cache
def split(n: int, times: int):
    if times == 0:
        return 1
    elif n == 0:
        return split(1, times - 1)
    elif len(str(n)) % 2 == 0:
        left = int(str(n)[:len(str(n)) // 2])
        right = int(str(n)[len(str(n)) // 2:])
        return split(left, times - 1) + split(right, times - 1)
    return split(n * 2024, times - 1)

def stones(data: str):
    stones = [int(x) for x in data.split(' ')]

    yield sum(split(s, 25) for s in stones)
    yield sum(split(s, 75) for s in stones)


if __name__=='__main__':
    test = stones(TEST_DATA)
    assert next(test) == 55312

    run = stones(INPUT)
    print(next(run))
    print(next(run))