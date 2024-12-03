import os

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
3   4
4   3
2   5
1   3
3   9
3   3
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()


def parse_data(data: str) -> tuple[list, list]:
    left, right = zip(*[map(int, l.split('   ')) for l in data.split('\n')])
    a = sorted(left)
    b = sorted(right)
    return a, b

def total_distance(data: str) -> int:
    a, b = parse_data(data)
    return sum(abs(x - y) for x, y in zip(a, b))

def similarity_score(data: str) -> int:
    a, b = parse_data(data)
    accum = 0
    for x in a:
        accum += x * b.count(x)
    return accum


if __name__=='__main__':
    assert total_distance(TEST_DATA) == 11
    assert similarity_score(TEST_DATA) == 31

    print(total_distance(INPUT))
    print(similarity_score(INPUT))