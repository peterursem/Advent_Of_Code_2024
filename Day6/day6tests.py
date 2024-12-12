import pytest
import day6

GRID = day6.Grid('./Day6/testgrid.txt')

def test_cell_enum():
    for char in ["^","v","<",">"]:
        assert day6.CELL(char) == day6.CELL.GUARD
    assert day6.CELL(".") == day6.CELL.EMPTY
    assert day6.CELL("#") == day6.CELL.OBSTRUCTION

def test_grid_setup():
    data = GRID.data
    print(data)
    assert data == [
        [0,0,0,0,-1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,-1],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,-1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,-1,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,-1,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,-1,0],
        [-1,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,-1,0,0,0],
    ]

def test_locate_guard():
    assert GRID.locate_guard() == {
        "position": {"row": 6, "col": 4},
        "char": "^"
    }

def test_guard_init():
    assert GRID.guard.position == {"row": 6, "col":4}
    assert GRID.guard.heading == day6.HEADING.UP
