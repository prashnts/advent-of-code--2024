import heapq
import os
import networkx as nx

from tqdm import tqdm
from collections import namedtuple, defaultdict, Counter

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''.strip()

with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

P = namedtuple('P', 'x y')

def parse_data(data: str):
    board = {}
    for y, row in enumerate(data.splitlines()):
        for x, cell in enumerate(row):
            board[P(x, y)] = cell
            if cell == 'S':
                start = P(x, y)
            elif cell == 'E':
                end = P(x, y)
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

def maze_finder(data: str, target: int):
    board, start, end = parse_data(data)
    graph = defaultdict(defaultdict)
    cheats = []

    for n in board:
        if board[n] == '#':
            continue

        for d in step_factor.values():
            t = P(n.x + d.x, n.y + d.y)
            if t not in board or d not in board:
                continue
            if board[t] == '#':
                for c in step_factor.values():
                    s = P(t.x + c.x, t.y + c.y)
                    if s not in board or s == d:
                        continue
                    if board[s] == '#':
                        continue
                    if n != s:
                        cheats.append((n, s))
                continue
            graph[n][t] = 1
            graph[t][n] = 1

    def dijkstra(graph, start, end_nodes):
        all_short_paths = []
        min_cost = float('inf')
        pq = [(0, 0, start, [start])]
        pathcosts = defaultdict(lambda: float('inf'))
        pathcosts[start] = 0

        while pq:
            cost, d, node, path = heapq.heappop(pq)
            if cost >= min_cost:
                break

            if node in end_nodes:
                if cost < min_cost:
                    min_cost = cost
                    all_short_paths = [path]
                elif cost == min_cost:
                    all_short_paths.append(path)
                break

            for next_node, edge_cost in graph[node].items():
                new_cost = cost + edge_cost
                if new_cost < pathcosts[next_node]:
                    pathcosts[next_node] = new_cost
                    heapq.heappush(pq, (new_cost, d + 1, next_node, path + [next_node]))
        
        return all_short_paths, min_cost

    _, max_cost = dijkstra(graph, start, [end])

    G = nx.Graph()
    G.add_weighted_edges_from([(n, s, 1) for n in graph for s in graph[n]])
    
    min_costs = []
    print(f'Max cost: {max_cost}')

    for c in tqdm(set(cheats), disable=max_cost < 100):
        n, s = c

        G.add_weighted_edges_from([(n, s, 2)])

        mc = nx.shortest_path_length(G, start, end, weight='weight')

        if (nc := max_cost - mc) > 0:
            min_costs.append(nc)
        
        G.remove_edges_from([(n, s)])

    costs = Counter(min_costs)

    yield costs[target]
    yield costs


if __name__=='__main__':
    assert next(maze_finder(TEST_DATA, 2)) == 14
    assert next(maze_finder(TEST_DATA, 4)) == 14
    assert next(maze_finder(TEST_DATA, 6)) == 2
    assert next(maze_finder(TEST_DATA, 64)) == 1

    run = maze_finder(INPUT, 100)
    next(run)
    print(sum([v for k, v in next(run).items() if k >= 100]))