import heapq
import os

from collections import namedtuple, defaultdict

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''.strip()

TEST_DATA_2 = '''\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
'''.strip()

with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

P = namedtuple('P', 'x y')

def parse_data(data: str):
    board = {}

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == 'S':
                start = P(x, y)
            elif c == 'E':
                end = P(x, y)
            board[P(x, y)] = c

    return board, start, end

def print_board(board, path):
    x_coord, y_coord = zip(*board.keys())
    x_max, y_max = max(x_coord), max(y_coord)

    render = [['.' for _ in range(x_max + 1)] for _ in range(y_max + 1)]

    for k, v in board.items():
        x, y = k
        render[y][x] = v
    
    for p in path:
        if type(p) == str:
            continue
        x, y = p
        render[y][x] = '+'

    return '\n'.join(''.join(row) for row in render)


step_factor = {
    '^': P(0, -1),
    'v': P(0, 1),
    '<': P(-1, 0),
    '>': P(1, 0),
}


def maze_finder(data: str):
    board, start, end = parse_data(data)
    graph = defaultdict(defaultdict)

    for n in board:
        if board[n] == '#':
            continue
        graph[(n, True)][(n, False)] = 1000
        graph[(n, False)][(n, True)] = 1000

        for d in step_factor.values():
            t = P(n.x + d.x, n.y + d.y)
            if board.get(t) == '#' or t not in board:
                continue
            graph[(n, bool(d.y))][(t, bool(d.y))] = 1


    def dijkstra(graph, start, end_nodes):
        all_short_paths = []
        min_cost = float('inf')
        c = 0
        pq = [(0, c, start, [start])]
        pathcosts = defaultdict(lambda: float('inf'))
        pathcosts[start] = 0

        while pq:
            cost, _, node, path = heapq.heappop(pq)
            if cost > min_cost:
                break

            if node in end_nodes:
                if cost < min_cost:
                    min_cost = cost
                    all_short_paths = [path]
                elif cost == min_cost:
                    all_short_paths.append(path)
                continue

            for next_node, edge_cost in graph[node].items():
                new_cost = cost + edge_cost
                if new_cost <= pathcosts[next_node]:
                    pathcosts[next_node] = new_cost
                    c += 1
                    heapq.heappush(pq, (new_cost, c, next_node, path + [next_node]))
        
        return all_short_paths, min_cost

    shortest_path = dijkstra(graph, (start, False), [(end, True), (end, False)])

    yield shortest_path[1]
    yield len({p[0] for path in shortest_path[0] for p in path})


if __name__=='__main__':
    test = maze_finder(TEST_DATA)
    assert next(test) == 7036
    assert next(test) == 45
    assert next(maze_finder(TEST_DATA_2)) == 11048

    run = maze_finder(INPUT)
    print(next(run))
    print(next(run))