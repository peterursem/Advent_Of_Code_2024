EMPTY_INDEX = -1

def read_file(filename):
    with open(filename) as file:
        return file.read().strip()

def read_map(map):
    files_count = 0
    disk = []
    for i in range(len(map)):
        id = EMPTY_INDEX
        if i % 2 == 0:
            id = files_count
            files_count += 1
        for _ in range(int(map[i])):
            disk.append(id)
    return disk

def disk_listing(disk , places=1):
    out = ""
    for i in range(len(disk)):
        char = disk[i]
        if char == EMPTY_INDEX:
            char = '.'
        else:
            if places == 1:
                char = f'{char:01}'
            else:
                char = f'{char:05}'
        out = out + char
    return out

def find_space(disk, length):
    biggest_space = 0
    for i in range(len(disk)):
        if disk[i] == EMPTY_INDEX:
            biggest_space += 1
        else:
            biggest_space = 0
        if biggest_space == length:
            return i + 1 - biggest_space
    return -1

def locate_file(disk, file):
    return disk.index(file), disk.count(file)

def move_file(disk, num):
    file = max(disk) - num
    file_index, file_len = locate_file(disk, file)
    next_index = find_space(disk, file_len)
    if next_index == -1 or next_index > file_index:
        return disk
    for x in range(next_index, next_index + file_len):
        disk[x] = file
    for x in range(file_index, file_index + file_len):
        disk[x] = EMPTY_INDEX
    
    return disk

def move_condition(disk, count):
    return count <= max(disk)
    
def shuffle_disk(disk, _):
    moving_block = EMPTY_INDEX
    i = 0
    while moving_block == EMPTY_INDEX and i <= len(disk):
        i += 1
        moving_block = disk[len(disk) - i]

    disk[len(disk) - i] = EMPTY_INDEX
    first_space = disk.index(EMPTY_INDEX)

    disk[first_space] = moving_block
    return disk
    
def shuffle_condition(disk, _):
    return disk.index(EMPTY_INDEX) < len(disk) - disk.count(EMPTY_INDEX)

def clean(disk, loop_func, condition, out=False):
    count = 0
    while condition(disk, count):
        loop_func(disk, count)
        if out:
            print(disk_listing(disk))
        count += 1
    return disk

def checksum(disk):
    out = 0
    for i in range(len(disk)):
        if disk[i] == -1:
            continue
        out += i * disk[i]
    return out

def main(map):
    disk = clean(map, move_file, move_condition, out=False)
    #disk = clean(map, shuffle_disk, shuffle_condition)

    # print(disk_listing(disk, places=0))
    print(f'Checksum: {checksum(disk)}')

test_map = read_map('2333133121414131402')
file_map = read_map(read_file('./Day9/input.txt'))
main(file_map)