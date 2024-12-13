import re
import os
from sympy import Symbol, Integer
from sympy.solvers import solve

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

def parse_data(data: str):
    machines = data.split('\n\n')
    pattern = r'[\w ]+: X[+=](\d+), Y[+=](\d+)'

    for m in machines:
        lines = m.splitlines()
        ax, ay = map(int, re.match(pattern, lines[0]).groups())
        bx, by = map(int, re.match(pattern, lines[1]).groups())
        px, py = map(int, re.match(pattern, lines[2]).groups())
        yield (ax, ay), (bx, by), (px, py)

def minimize(a, b, p):
    ta = Symbol('ta')
    tb = Symbol('tb')

    eq1 = ta * a[0] + tb * b[0] - p[0]
    eq2 = ta * a[1] + tb * b[1] - p[1]

    val = solve([eq1, eq2], (ta, tb), dict=True)
    assert len(val) == 1

    va = val[0][ta]
    vb = val[0][tb]

    if type(va) is Integer and type(vb) is Integer:
        return 3 * int(va) + int(vb)
    return 0


def min_tokens(data: str):
    tokens_1 = 0
    tokens_2 = 0

    for a, b, p in parse_data(data):
        tokens_1 += minimize(a, b, p)
        tokens_2 += minimize(a, b, (p[0] + 10000000000000, p[1] + 10000000000000))

    yield tokens_1
    yield tokens_2

if __name__=='__main__':
    test = min_tokens(TEST_DATA)
    assert next(test) == 480

    run = min_tokens(INPUT)
    print(next(run))
    print(next(run))