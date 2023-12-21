from __future__ import annotations

import argparse
import logging

global_logger: logging.Logger

from dataclasses import dataclass
from typing import Optional
from collections import deque

# Going to abuse this class to mean x-y coords too; and vector
@dataclass
class Offset:
    x: int
    y: int

    def __add__(self, other: Offset):
        return Offset(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Offset):
        return Offset(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other: Offset):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class VisitedMap:
    _grid: list[list[str]]

    def __init__(self, grid_map: GridMap):
        self._grid = [["." for _ in row] for row in grid_map._grid]

    def __getitem__(self, key):
        if isinstance(key, Offset):
            return self._grid[key.y][key.x]
        else:
            return self._grid[key]
    
    def __setitem__(self, key, value: str):
        if isinstance(key, Offset):
            self._grid[key.y][key.x] = value
        else:
            self._grid[key] = value
    
    def __str__(self):
        return "\n" + "\n".join(["".join(line) for line in self._grid])
    
    def __len__(self):
        return len(self._grid)
    
    def __iter__(self):
        return iter(self._grid)

class GridMap:
    _grid: list[list[str]]
    _visited_grid: VisitedMap
    _visited_splitters: set
    _direction_queue: deque
    _size: Offset

    def __init__(self):
        self._grid = list()
        for line in yield_next_input_line():
            if line:
                self._grid.append([c for c in line])
        self._visited_splitters = set()
        self._size = Offset(len(self._grid[0]), len(self._grid))
        self._visited_grid = VisitedMap(self)

    def __getitem__(self, key):
        if isinstance(key, Offset):
            return self._grid[key.y][key.x]
        else:
            return self._grid[key]
    
    def __str__(self):
        return "\n" + "\n".join(["".join(line) for line in self._grid])
    
    def __len__(self):
        return len(self._grid)
    
    def travel_until_splitter(self, start_point: Offset, direction: Offset) -> Optional[Offset]:
        if direction == Offset(0,0):
            return

        next_point = start_point
        self._visited_grid[next_point] = "#"
        while True:
            next_point += direction
            if next_point.x < 0 or next_point.y < 0 or next_point.x >= len(self._grid[0]) or next_point.y >= len(self._grid):
                return
            
            self._visited_grid[next_point] = "#"

            if self[next_point] in "|-/\\":
                return next_point

    def get_split_directions(self, splitter_offset: Offset, direction: Offset) -> list[Offset]:
        splitter_char = self[splitter_offset]
        if splitter_char == "|":
            if direction == Offset(1,0) or direction == Offset(-1,0):
                return [Offset(0,1), Offset(0,-1)]
            elif direction == Offset(0,1) or direction == Offset(0,-1):
                return [direction]
            else:
                return []
        elif splitter_char == "-":
            if direction == Offset(0,1) or direction == Offset(0,-1):
                return [Offset(1,0), Offset(-1,0)]
            elif direction == Offset(1,0) or direction == Offset(-1,0):
                return [direction]
            else:
                return []
        elif splitter_char == "\\":
            if direction == Offset(0,1):
                return [Offset(1,0)]
            elif direction == Offset(0,-1):
                return [Offset(-1,0)]
            elif direction == Offset(1,0):
                return [Offset(0,1)]
            elif direction == Offset(-1,0):
                return [Offset(0,-1)]
            else:
                return []
        elif splitter_char == "/":
            if direction == Offset(0,1):
                return [Offset(-1,0)]
            elif direction == Offset(0,-1):
                return [Offset(1,0)]
            elif direction == Offset(1,0):
                return [Offset(0,-1)]
            elif direction == Offset(-1,0):
                return [Offset(0,1)]
            else:
                return []
        else:
            raise RuntimeError(f"Unexpected splitter character {splitter_char}")
        
    def travel(self, _start_point = Offset(0,0), _direction = Offset(1,0)):
        start_point = _start_point
        direction = _direction
        direction_queue = deque()
        visited_splitters = set()

        while True:
            if (start_point, direction) not in visited_splitters:
                splitter_offset = self.travel_until_splitter(start_point, direction)
                logging.debug(self._visited_grid)
                if splitter_offset:
                    for new_direction in self.get_split_directions(splitter_offset, direction):
                        direction_queue.append((splitter_offset, new_direction))
                
                visited_splitters.add((start_point, direction))
            
            logging.debug(direction_queue)
            if not direction_queue:
                break

            start_point, direction = direction_queue.popleft()
        return self

    def count_energised(self):
        acc = 0
        for line in self._visited_grid:
            acc += line.count("#")
        return acc

def solve_p1():
    global_logger.info("Solving P1")
    grid = GridMap()
    logging.debug(grid)
    grid.travel()
    print(grid.count_energised())
    pass

def solve_p2():
    global_logger.info("Solving P2")
    grid1 = GridMap()
    c_max = 0
    width = len(grid1._grid[0])
    length = len(grid1)

    c_max = 0
    for ii in range(length):
        c_max = max(c_max, GridMap().travel(Offset(0,ii), Offset(1,0)).count_energised())
        c_max = max(c_max, GridMap().travel(Offset(width - 1,ii), Offset(-1,0)).count_energised())
    for jj in range(width):
        c_max = max(c_max, GridMap().travel(Offset(jj,0), Offset(0,1)).count_energised())
        c_max = max(c_max, GridMap().travel(Offset(jj, length - 1), Offset(0,-1)).count_energised())
    print(c_max)
    pass

def yield_next_input_line() -> str:
    input_file = r"input.txt" if not USE_TEST_INPUT else r"test-input.txt"

    with open(input_file, "r") as in_file:
        for line in in_file:
            yield line.strip()

def log_level_type(x):
    x = int(x)
    if x > 5:
        raise argparse.ArgumentTypeError("Maximum log level is 5")
    return x

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p2", help="Solves Part 2 instead of Part 1", action='store_true', default=False)
    parser.add_argument("--test", "-t", help="Use test-input.txt instead of input.txt", action='store_true', default=False)
    parser.add_argument("--log", "-l", help="Sets the log level between 0-5. 0 is all, 5 is Critical-only. Default=3", type=log_level_type, default=3)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    logging.basicConfig(level=(args.log*10)) # Logs to stderr
    global_logger = logging.getLogger()
    USE_TEST_INPUT = args.test

    if not args.p2:
        solve_p1()
    else:
        solve_p2()