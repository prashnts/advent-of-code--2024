import heapq
import os
from tqdm import tqdm, trange
from collections import namedtuple, defaultdict


TEST_DATA = {
    'A': 729,
    'program': [0,1,5,4,3,0]
}

INPUT = {
    'A': 63281501,
    'program': [2,4, 1,5, 7,5, 4,5, 0,3, 1,6, 5,5, 3,0],
}

def computer(program, A):
    A = A
    B = 0
    C = 0
    pc = 0
    output = []

    def combo(oper):
        if oper < 4:
            return oper
        if oper == 4:
            return A
        if oper == 5:
            return B
        if oper == 6:
            return C
        raise ValueError(f'Unknown combo operand: {oper}')

    while True:
        if pc >= len(program):
            break
        inst, opr = program[pc], program[pc + 1]
        copr = combo(opr)

        match inst:
            case 0: # adv
                A = A // (2 ** copr)
            case 1: # bxl
                B = B ^ opr
            case 2: # bst
                B = copr % 8
            case 3: # jnz
                pc = opr if A != 0 else pc + 2
                continue
            case 4: # bxc
                B = B ^ C
            case 5: # out
                output.append(copr % 8)
            case 6: # bdv
                B = A // (2 ** copr)
            case 7: # cdv
                C = A // (2 ** copr)

        pc += 2

    return output

def func(a):
    # Equivalent to my input.
    while True:
        b = (a % 8) ^ 5
        c = a // (2 ** b)
        b = b ^ c ^ 6
        a = a // (2 ** 3)
        yield b % 8
        if a == 0:
            return

def brute_force(start, prog):
    # Brute force/iterate the problem space. Since each iteration
    # affects next group of  bits, we can jump faster.
    if not prog:
        yield start // 8
        return

    for a in range(start, start + 8):
        if next(func(a)) == prog[-1]:
            yield from brute_force(a * 8, prog[:-1])

if __name__=='__main__':
    test = computer(**TEST_DATA)
    assert test == [4,6,3,5,6,3,5,2,1,0]

    run = computer(**INPUT)
    print(','.join(map(str, run)))

    min_a = float('inf')
    for sol in brute_force(0, INPUT['program']):
        assert list(func(sol)) == INPUT['program']
        if sol < min_a:
            min_a = sol
    print(min_a)