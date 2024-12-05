import os

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()


def xmas_count(data: str) -> int:
    board = [list(l) for l in data.split('\n')]
    count = 0

    def check_neighbors(x, y):
        x_max = len(board) - 4
        y_max = len(board[0]) - 4
        x_min = 3
        y_min = 3
        cells = [
            [board[x][y + i] for i in range(4)] if y <= y_max else [], # Down
            [board[x][y - i] for i in range(4)] if y >= y_min else [], # Up
            [board[x + i][y] for i in range(4)] if x <= x_max else [], # Right
            [board[x - i][y] for i in range(4)] if x >= x_min else [], # Left
            [board[x + i][y + i] for i in range(4)] if x <= x_max and y <= y_max else [], # Down Right
            [board[x - i][y + i] for i in range(4)] if x >= x_min and y <= y_max else [], # Down Left
            [board[x + i][y - i] for i in range(4)] if x <= x_max and y >= y_min else [], # Up Right
            [board[x - i][y - i] for i in range(4)] if x >= x_min and y >= y_min else [], # Up Left
        ]
        values = [''.join(c) for c in cells]
        return values.count('XMAS')

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'X':
                count += check_neighbors(i, j)
    return count


def mas_count(data: str) -> int:
    board = [list(l) for l in data.split('\n')]

    def check_neighbors(x, y):
        diag_1 = [
            (x - 1, y - 1),
            (x, y),
            (x + 1, y + 1),
        ]
        diag_2 = [
            (x + 1, y - 1),
            (x, y),
            (x - 1, y + 1),
        ]
        def get_diag(diag):
            try:
                return ''.join([board[x][y] for x, y in diag])
            except IndexError:
                return ''

        check = ['MAS', 'SAM']

        a, b = get_diag(diag_1), get_diag(diag_2)
        if a in check and b in check:
            return 1

        return 0

    count = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'A':
                count += check_neighbors(i, j)
    return count

if __name__=='__main__':
    assert xmas_count(TEST_DATA) == 18
    assert mas_count(TEST_DATA) == 9

    print(xmas_count(INPUT))
    print(mas_count(INPUT))