import pytest
import day9

BASEMAP = '2333133121414131402'
DISK = [0, 0, -1, -1, -1, 1, 1, 1, -1, -1, -1, 2, -1, -1, -1, 3, 3, 3, -1, 4, 4, -1, 5, 5, 5, 5, -1, 6, 6, 6, 6, -1, 7, 7, 7, -1, 8, 8, 8, 8, 9, 9]
LISTING = '00...111...2...333.44.5555.6666.777.888899'
CLEANED = [0, 0, 9, 9, 8, 1, 1, 1, 8, 8, 8, 2, 7, 7, 7, 3, 3, 3, 6, 4, 4, 6, 5, 5, 5, 5, 6, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

def test_read_map():
    out = day9.read_map(BASEMAP)
    assert out == DISK

def test_disk_listing():
    assert day9.disk_listing(DISK) == LISTING

def test_shuffle_disk():
    disk = DISK.copy()
    print(disk)
    day9.shuffle_disk(disk, 0)
    print(disk)
    assert disk == [0, 0, 9, -1, -1, 1, 1, 1, -1, -1, -1, 2, -1, -1, -1, 3, 3, 3, -1, 4, 4, -1, 5, 5, 5, 5, -1, 6, 6, 6, 6, -1, 7, 7, 7, -1, 8, 8, 8, 8, 9, -1]

def move_file():
    disk = disk.copy()
    day9.move_file(disk)
    print(disk)
    assert disk == [0, 0, 9, 9, -1, 1, 1, 1, -1, -1, -1, 2, -1, -1, -1, 3, 3, 3, -1, 4, 4, -1, 5, 5, 5, 5, -1, 6, 6, 6, 6, -1, 7, 7, 7, -1, 8, 8, 8, 8, -1, -1]

def test_clean():
    disk = DISK.copy()
    assert day9.clean(disk, day9.shuffle_disk, day9.shuffle_condition) == CLEANED
    assert day9.clean([0, 0, -1, -1, -1, 1, 1, 1, -1, -1, -1, 2, -1, -1, -1, 3, 3, 3, -1, 4, 4, -1, 5, 5, 5, 5, -1, 6, 6, 6, -1, 7, 7, 7, -1, 8, 8, 8, 8, 9, 9], day9.shuffle_disk, day9.shuffle_condition) == [0, 0, 9, 9, 8, 1, 1, 1, 8, 8, 8, 2, 7, 7, 7, 3, 3, 3, 6, 4, 4, 6, 5, 5, 5, 5, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

def test_chcksum():
    assert day9.checksum(CLEANED) == 1928
    assert day9.checksum([0,0,9,9,2,1,1,1,7,7,7,-1,4,4,-1,3,3,3,-1,-1,-1,-1,5,5,5,5,-1,6,6,6,6,-1,-1,-1,-1,-1,8,8,8,8,-1,-1]) == 2858

def test_find_space():
    assert day9.find_space(day9.shuffle_disk(DISK.copy(), 0), 3) == 8
    assert day9.find_space(DISK, 2) == 2
    assert day9.find_space(DISK, 1) == 2

def test_locate_file():
    file_index, file_len = day9.locate_file(DISK, 0)
    assert file_index == 0
    assert file_len == 2
    file_index, file_len = day9.locate_file(DISK, 9)
    assert file_index == 40
    assert file_len == 2

def test_move_file():
    disk = DISK.copy()
    assert day9.move_file(disk, 0) == [0, 0, 9, 9, -1, 1, 1, 1, -1, -1, -1, 2, -1, -1, -1, 3, 3, 3, -1, 4, 4, -1, 5, 5, 5, 5, -1, 6, 6, 6, 6, -1, 7, 7, 7, -1, 8, 8, 8, 8, -1, -1]
    assert day9.move_file(disk, 1) == [0, 0, 9, 9, -1, 1, 1, 1, -1, -1, -1, 2, -1, -1, -1, 3, 3, 3, -1, 4, 4, -1, 5, 5, 5, 5, -1, 6, 6, 6, 6, -1, 7, 7, 7, -1, 8, 8, 8, 8, -1, -1]
    assert day9.move_file(disk, 2) == [0, 0, 9, 9, -1, 1, 1, 1, 7, 7, 7, 2, -1, -1, -1, 3, 3, 3, -1, 4, 4, -1, 5, 5, 5, 5, -1, 6, 6, 6, 6, -1, -1, -1, -1, -1, 8, 8, 8, 8, -1, -1]

def test_move_condition():
    assert day9.move_condition(DISK, 10) == False
    assert day9.move_condition(DISK, 9) == True
    assert day9.move_condition(DISK, 0) == True

