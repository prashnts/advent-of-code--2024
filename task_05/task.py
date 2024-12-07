import os
from itertools import combinations
from functools import cmp_to_key

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

def parse_data(data: str):
    rules, updates = data.split('\n\n')
    rules = rules.splitlines()
    updates = [u.split(',') for u in updates.splitlines()]
    return rules, updates

def is_ordered(data: str):
    rules, updates = parse_data(data)
    middle_sum = 0

    for u in updates:
        if all(f'{x}|{y}' in rules for x, y in combinations(u, 2)):
            middle_sum += int(u[len(u) // 2])
    
    return middle_sum

def make_ordered(data: str):
    rules, updates = parse_data(data)
    bad_updates = [u for u in updates if not all(f'{x}|{y}' in rules for x, y in combinations(u, 2))]

    def comparator(a, b):
        for r in rules:
            if r == f'{a}|{b}':
                return -1
            if r == f'{b}|{a}':
                return 1
        return 0
    
    new_updates = [sorted(bu, key=cmp_to_key(comparator)) for bu in bad_updates]

    return sum([int(u[len(u) // 2]) for u in new_updates])


if __name__=='__main__':
    assert is_ordered(TEST_DATA) == 143
    assert make_ordered(TEST_DATA) == 123

    print(is_ordered(INPUT))
    print(make_ordered(INPUT))