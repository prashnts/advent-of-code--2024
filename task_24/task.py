import os

from collections import namedtuple
from itertools import combinations, permutations

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
'''.strip()
TEST_DATA_2 = '''\
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z00
x01 AND y01 -> z01
x02 AND y02 -> z02
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z05
'''


with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()


Conn = namedtuple('Conn', 'x op y v')

def parse_data(data: str):
    ivalues, iconnections = data.split('\n\n')

    values = {}
    connections = [Conn(*c.replace(' -> ', ' ').split(' ')) for c in iconnections.splitlines()]
    
    for v in ivalues.splitlines():
        k, v = v.split(': ')
        values[k] = int(v)

    return values, connections


def evaluate(x, op, y):
    match op:
        case 'AND':
            return x & y
        case 'OR':
            return x | y
        case 'XOR':
            return x ^ y


def pick(values, prefix):
    vals = sorted(((k, v) for k, v in values.items() if k.startswith(prefix)), key=lambda x: x[0], reverse=True)
    return int(''.join(str(v) for _, v in vals), base=2)


def solve(data: str, swaps: int = 4):
    values, connections = parse_data(data)

    def calculate(values, connections):
        values = values.copy()
        connections = connections[:]
        while len(connections) > 0:
            for i, conn in enumerate(connections):
                if conn.x not in values or conn.y not in values:
                    continue
                x = values[conn.x]
                y = values[conn.y]
                values[conn.v] = evaluate(x, conn.op, y)
                del connections[i]
        return pick(values, 'x'), pick(values, 'y'), pick(values, 'z')

    x, y, z = calculate(values, connections)

    yield z
    print(f'{z=}')

    pairs = list(combinations(connections, 2))
    pairs_of_4 = list(combinations(pairs, 4))
    print(pairs_of_4)
    print(f'Pairs: {len(pairs_of_4)}')

    while pairs_of_4:
        # Swap connections
        conns = connections[:]
        swap = pairs_of_4.pop()
        for sa, sb in swap:
            ia = connections.index(sa)
            ib = connections.index(sb)
            a = connections[ia]
            b = connections[ib]
            conns[ia] = Conn(a.x, a.op, a.y, b.v)
            conns[ib] = Conn(b.x, b.op, b.y, a.v)
        # swap = [conns.index(s) for s in pairs_of_4.pop()]
        # print(f'{swap=}')
        # a = conns[swap[0]]
        # b = conns[swap[1]]
        # if swaps == 4:
        #     c = conns[swap[2]]
        #     d = conns[swap[3]]
        #     conns[swap[2]] = Conn(c.x, c.op, c.y, d.v)
        #     conns[swap[3]] = Conn(d.x, d.op, d.y, c.v)
        # conns[swap[0]] = Conn(a.x, a.op, a.y, b.v)
        # conns[swap[1]] = Conn(b.x, b.op, b.y, a.v)


        x, y, z = calculate(values, conns)

        print(x, y, x + y, z)
        if x + y == z:
            yield z
            break



if __name__=='__main__':
    test = solve(TEST_DATA)
    assert next(test) == 2024
    test = solve(TEST_DATA_2, 4)
    next(test)
    assert next(test) == 2024

    run = solve(INPUT, 4)
    print(next(run))
    print(next(run))
