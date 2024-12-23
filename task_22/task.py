import os
import networkx as nx

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
1
10
100
2024
'''.strip()

with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

def next_secret(secret: int, times: int = 1):
    mix = lambda n, s: n ^ s
    prune = lambda s: s % 16777216

    s = secret

    for _ in range(times):
        s = prune(mix(s * 64, s))
        s = prune(mix(s // 32, s))
        s = prune(mix(s * 2048, s))

        yield s

def solve(data: str):
    sum = 0

    for s in data.splitlines():
        secrets = list(next_secret(int(s), 2000))
        print(secrets)
        sum += secrets[-1]
    
    yield sum



if __name__=='__main__':
    test = solve(TEST_DATA)
    assert next(test) == 37327623

    run = solve(INPUT)
    print(next(run))
