import os
from collections import defaultdict
from itertools import combinations

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
2333133121414131402
'''.strip()
with open(f'{__here__}/input.txt') as fp:
    INPUT = fp.read().strip()

def parse_data(data: str):
    file_num = 0
    for i, c in enumerate(data):
        if i % 2 == 1:
            # Free space
            yield from [-1 for _ in range(int(c))]
        else:
            # Disk
            yield from [file_num for _ in range(int(c))]
            file_num += 1

def print_disk(disk):
    for c in disk[:100]:
        if c == -1:
            print('.', end='')
        else:
            print(c, end='')
    print()


def defrag_1(disk: list):
    disk = disk[:]
    is_defragged = lambda d: all(c == -1 for c in d[d.index(-1):])

    while not is_defragged(disk):
        # Find the first file from the end of the disk
        findex, fid = [(i, f) for i, f in enumerate(disk) if f != -1][-1]
        # Find first empty space from the beginning of the disk
        eindex = disk.index(-1)

        # Move the file to the empty space
        disk[eindex] = fid
        disk[findex] = -1
    return disk

def defrag_2(data):
    disk = []
    file_num = 0
    for i, c in enumerate(data):
        if i % 2 == 1:
            # Free space
            disk.append((-1, int(c)))
        else:
            disk.append((file_num, int(c)))
            file_num += 1

    file_num -= 1

    def merge_spaces(d):
        prev_spaces = 0
        for i, (fid, size) in enumerate(d):
            if fid == -1:
                prev_spaces += size
            else:
                if prev_spaces > 0:
                    yield (-1, prev_spaces)
                    prev_spaces = 0
                yield (fid, size)

    while file_num > 0:
        # Merge empty spaces
        disk = list(merge_spaces(disk))
        # Find the current file
        findex = [i for i, c in enumerate(disk) if c[0] == file_num][0]
        fsize = disk[findex][1]

        # Find the first empty space equal or greater than the file size
        try:
            eindex = [i for i, (fid, size) in enumerate(disk) if fid == -1 and size >= fsize and i < findex][0]
        except IndexError:
            # No empty space, continue.
            file_num -= 1
            continue
        # Move the file to the empty space
        prev_size = disk[eindex][1]
        disk[eindex] = disk[findex]
        disk[findex ] = (-1, fsize)
        if prev_size >= fsize:
            disk.insert(eindex + 1, (-1, prev_size - fsize))

        file_num -= 1

    disk_2 = []

    for fid, size in disk:
        if fid == -1:
            disk_2.extend([-1 for _ in range(size)])
        else:
            disk_2.extend([fid for _ in range(size)])

    return disk_2

def checksum(data: str):
    disk = list(parse_data(data))
    disk_1 = defrag_1(disk)
    yield sum([i * fid for i, fid in enumerate(disk_1) if fid != -1])

    disk = defrag_2(data)
    yield sum([i * fid for i, fid in enumerate(disk) if fid != -1])


if __name__=='__main__':
    test = checksum(TEST_DATA)
    assert next(test) == 1928
    assert next(test) == 2858

    print("Tests passed")

    run = checksum(INPUT)
    print(next(run))
    print(next(run))