import os
import re

__here__ = os.path.dirname(__file__)

TEST_DATA = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
TEST_DATA_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()


def multiply(data: str) -> int:
    PATTERN = re.compile(r'mul\((\d+),(\d+)\)')
    return sum([int(x) * int(y) for x, y in PATTERN.findall(data)])

def conditional_multiply(data: str) -> int:
    PATTERN = re.compile(r'(mul\((\d+),(\d+)\)|do\(\)|don\'t\(\))')
    multiplying = True
    accum = 0
    for match, x, y in PATTERN.findall(data):
        if match[:3] == 'mul' and multiplying:
            accum += int(x) * int(y)
        elif match == 'do()':
            multiplying = True
        elif match == 'don\'t()':
            multiplying = False
    return accum


if __name__=='__main__':
    assert multiply(TEST_DATA) == 161
    assert conditional_multiply(TEST_DATA_2) == 48

    print(multiply(INPUT))
    print(conditional_multiply(INPUT))