import os
from collections import defaultdict

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

def parse_data(data: str):
    board = {}
    for y, line in enumerate(data.splitlines()):
        for x, cell in enumerate(line):
            board[(x, y)] = cell
    return board

def find_regions(data: str):
    board = parse_data(data)

    regions = defaultdict(set)

    for cell, value in board.items():
        regions[value].add(cell)

    def neighbors(x, y):
        cells = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        for c in cells:
            if c in board:
                yield c
            else:
                yield None

    def fence_perimeter(cell):
        value = board[cell]
        # Count the number of total neighbors non equal.
        return 4 - len([n for n in neighbors(*cell) if n != None and board[n] == value])
    
    def count_sides(cells):
        sides = 0

        for (x, y) in cells:
            left = x - 1
            right = x + 1
            up = y - 1
            down = y + 1
            next_not_in_region = (right, y) not in cells
            down_not_in_region = (x, down) not in cells

            if (x, up) not in cells:
                if next_not_in_region or (right, up) in cells:
                    sides += 1
            if (x, down) not in cells:
                if next_not_in_region or (right, down) in cells:
                    sides += 1
            if (left, y) not in cells:
                if down_not_in_region or (left, down) in cells:
                    sides += 1
            if (right, y) not in cells:
                if down_not_in_region or (right, down) in cells:
                    sides += 1
        
        return sides

    def contiguos_regions(cells):
        # Flood fill algorithm from wikipedia, like every year.
        cell = cells.pop()
        region = {cell}
        q = [cell]

        while q:
            n = q.pop(0)

            for c in neighbors(*n):
                if c in cells and board[c] == board[n]:
                    q.append(c)
                    region.add(c)
                    cells.remove(c)

        yield region

        if cells:
            yield from contiguos_regions(cells)
    
    accum_1 = 0
    accum_2 = 0

    for value, cells in regions.items():
        for region in contiguos_regions(cells):
            area = len(region)
            perimeter = sum(map(fence_perimeter, region))
            sides = count_sides(region)

            accum_1 += area * perimeter
            accum_2 += area * sides

    yield accum_1
    yield accum_2

if __name__=='__main__':
    test = find_regions(TEST_DATA)
    assert next(test) == 1930
    assert next(test) == 1206

    run = find_regions(INPUT)
    print(next(run))
    print(next(run))