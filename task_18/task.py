import heapq
import os

from collections import namedtuple, defaultdict

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''.strip()

with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

P = namedtuple('P', 'x y')

def parse_data(data: str):
    for line in data.splitlines():
        x, y = map(int, line.split(','))
        yield P(x, y)

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

def maze_finder(data: str, bounds, count):
    coords = list(parse_data(data))

    def make_boards(cnt):
        board = {}
        graph = defaultdict(defaultdict)


        for y in range(bounds[1] + 1):
            for x in range(bounds[0] + 1):
                board[P(x, y)] = '.'

        for c in coords[:cnt]:
            board[c] = '#'
        

        for n in board:
            if board[n] == '#':
                continue

            for d in step_factor.values():
                t = P(n.x + d.x, n.y + d.y)
                if board.get(t) == '#' or t not in board:
                    continue
                graph[n][t] = 1
                graph[t][n] = 1

        return board, graph

    def dijkstra(graph, start, end_nodes):
        all_short_paths = []
        min_cost = float('inf')
        c = 0
        pq = [(0, c, start, [start])]
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
                    # c += 1
                    heapq.heappush(pq, (new_cost, d+1, next_node, path + [next_node]))
        
        return all_short_paths, min_cost
    

    board, graph = make_boards(count)
    shortest_path = dijkstra(graph, P(0, 0), [P(*bounds)])

    print(print_board(board, shortest_path[0][0]))

    yield shortest_path[1]

    lim = count

    while True:
        lim += 1
        board, graph = make_boards(lim)
        shortest_path = dijkstra(graph, P(0, 0), [P(*bounds)])

        if not shortest_path[0]:
            yield ','.join(map(str, coords[lim - 1]))
            break


if __name__=='__main__':
    test = maze_finder(TEST_DATA, (6, 6), 12)
    assert next(test) == 22
    assert next(test) == '6,1'

    run = maze_finder(INPUT, (70, 70), 1024)
    print(next(run))
    print(next(run))