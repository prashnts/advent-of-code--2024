import os
from collections import namedtuple

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

Box = namedtuple('Box', 'x y')

def parse_data(data: str):
    map_, moves_ = data.split('\n\n')

    board = {}
    initial_pos = None

    for y, line in enumerate(map_.splitlines()):
        for x, cell in enumerate(line):
            if cell == '@':
                initial_pos = (x, y)
            if cell == '[':
                board[(x, y)] = Box(x, y)
                board[(x + 1, y)] = Box(x, y)
            elif cell == ']':
                continue
            else:
                board[(x, y)] = cell
    
    moves = moves_.replace('\n', '')

    return board, initial_pos, moves

def enlarge_board(data):
    data = (data
        .replace('#', '##')
        .replace('O', '[]')
        .replace('.', '..')
        .replace('@', '@.')
    )

    return parse_data(data)


step_factor = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}

def move(board, direction, pos):
    x, y = pos
    fx, fy = step_factor[direction]

    next_pos = (x + fx, y + fy)
    next_board = board.copy()

    if next_pos not in board:
        return board, pos
    
    if board[next_pos] == '#':
        return board, pos
    
    if board[next_pos] == '.':
        next_board[pos] = '.'
        next_board[next_pos] = '@'
        return next_board, next_pos
    
    # move boxes
    # find all the boxes until we get empty space or wall
    boxes = []
    bx, by = next_pos
    do_move = False
    while True:
        if board.get((bx, by)) == 'O':
            boxes.append((bx, by))
            bx += fx
            by += fy
            continue
        elif board.get((bx, by)) == '.':
            # There is an empty space, we can move the boxes
            do_move = True
            break
        else:
            # There is a wall
            break

    if not do_move:
        return board, pos
    
    # move the boxes
    for bx, by in boxes[::-1]:
        next_board[(bx, by)] = '.'
        next_board[(bx + fx, by + fy)] = 'O'

    next_board[pos] = '.'
    next_board[next_pos] = '@'

    return next_board, next_pos

def move_2(board, direction, pos):
    x, y = pos
    fx, fy = step_factor[direction]

    next_pos = (x + fx, y + fy)
    next_board = board.copy()

    if next_pos not in board:
        return board, pos
    
    if board[next_pos] == '#':
        return board, pos
    
    if board[next_pos] == '.':
        next_board[pos] = '.'
        next_board[next_pos] = '@'
        return next_board, next_pos

    box = board[next_pos]
    assert type(box) == Box
    boxes = [box]
    new_boxes = {box}

    do_move = True
    while new_boxes:
        b = new_boxes.pop()

        b1 = (b.x + fx, b.y + fy)
        b2 = (b.x + 1 + fx, b.y + fy)

        if type(board.get(b1)) == Box and board[b1] not in boxes:
            new_boxes.add(board[b1])
            boxes.append(board[b1])
        if type(board.get(b2)) == Box and board[b2] not in boxes:
            new_boxes.add(board[b2])
            boxes.append(board[b2])

        if board.get(b1) == '#' or board.get(b2) == '#':
            do_move = False
            break

    if not do_move:
        return board, pos

    for box in boxes:
        next_board[(box.x, box.y)] = '.'
        next_board[(box.x + 1, box.y)] = '.'

    for box in boxes:
        next_box = Box(box.x + fx, box.y + fy)
        next_board[(next_box.x, next_box.y)] = next_box
        next_board[(next_box.x + 1, next_box.y)] = next_box

    next_board[pos] = '.'
    next_board[next_pos] = '@'

    return next_board, next_pos


def print_board(board):
    x_coord, y_coord = zip(*board.keys())
    x_max, y_max = max(x_coord), max(y_coord)

    render = [['.' for _ in range(x_max + 1)] for _ in range(y_max + 1)]

    for k, v in board.items():
        x, y = k
        if type(v) == Box:
            if v.x == x:
                render[y][x] = '['
            else:
                render[y][x] = ']'
        else:
            render[y][x] = v

    return '\n'.join(''.join(row) for row in render)

def gps_sum(data: str):
    board, pos, moves = parse_data(data)

    for dir in moves:
        board, pos = move(board, dir, pos)

    total = 0

    for k, v in board.items():
        if v == 'O':
            x, y = k
            total += (100 * y + x)

    yield total

    board, pos, moves = enlarge_board(data)

    for dir in moves:
        board, pos = move_2(board, dir, pos)
        # print(print_board(board))

    total = 0

    for box in set(b for b in board.values() if type(b) == Box):
        x, y = box
        total += (100 * y + x)

    yield total

if __name__=='__main__':
    test = gps_sum(TEST_DATA)
    assert next(test) == 10092
    assert next(test) == 9021

    run = gps_sum(INPUT)
    print(next(run))
    print(next(run))