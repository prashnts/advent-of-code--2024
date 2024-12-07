import os
from itertools import cycle
from functools import cmp_to_key

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

def parse_data(data: str):
    for line in data.splitlines():
        target, values = line.split(': ')
        yield int(target), list(map(int, values.split()))

def can_solve(target, equation, accum=0, ops=None):
    if ops is None:
        ops = []
    if len(equation) == 1:
        x = accum + equation[0]
        y = accum * equation[0]

        if x == target or y == target:
            return True, ops + ['+'] if x == target else ops + ['*']
        return False
    
    a, *equation = equation

    x = accum + a
    y = accum * a

    if x > target and y > target:
        return False

    return can_solve(target, equation, x, ops + ['+']) or can_solve(target, equation, y, ops + ['*'])

def can_solve_concat(target, equation, accum=0, ops=None):
    if ops is None:
        ops = []
    if len(equation) == 1:
        x = accum + equation[0]
        y = accum * equation[0]
        z = int(str(accum) + str(equation[0]))

        if x == target or y == target or z == target:
            return True, ops + ['+'] if x == target else ops + ['*'] if y == target else ops + ['||']
        return False
    
    a, *equation = equation

    x = accum + a
    y = accum * a
    z = int(str(accum) + str(a))

    if x > target and y > target and z > target:
        return False

    return any([
        can_solve_concat(target, equation, x, ops + ['+']),
        can_solve_concat(target, equation, y, ops + ['*']),
        can_solve_concat(target, equation, z, ops + ['||']),
    ])


def operate(data: str):
    sum_a = 0
    sum_b = 0
    for target, values in parse_data(data):
        if can_solve(target, values):
            sum_a += target
        if can_solve_concat(target, values):
            sum_b += target
    yield sum_a
    yield sum_b 


if __name__=='__main__':
    test = operate(TEST_DATA)
    assert next(test) == 3749
    assert next(test) == 11387

    run = operate(INPUT)
    print(next(run))
    print(next(run))