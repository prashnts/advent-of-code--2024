import os
import networkx as nx

from functools import cache
from collections import namedtuple, defaultdict

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
'''.strip()

with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()


def solve(data: str, k: int = 3):
    G = nx.Graph()
    G.add_edges_from(e.split('-') for e in data.splitlines())

    sum = 0
    for g in nx.simple_cycles(G, k):
        if any([x[0] == 't' for x in g]):
            sum += 1

    yield sum
    yield ','.join(sorted(max(nx.enumerate_all_cliques(G), key=len)))

if __name__=='__main__':
    test = solve(TEST_DATA)
    assert next(test) == 7
    assert next(test) == 'co,de,ka,ta'

    run = solve(INPUT)
    print(next(run))
    print(next(run))



    