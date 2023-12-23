from __future__ import annotations
import argparse
import logging

global_logger: logging.Logger

import sys
from dataclasses import dataclass, field
from typing import Union, Any, Callable
from queue import PriorityQueue

# Going to abuse this class to mean x-y coords too;
@dataclass
class Offset:
    x: int
    y: int

    def __add__(self, other: Offset):
        return Offset(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Offset):
        return Offset(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other: int):
        if not isinstance(other, int):
            raise ValueError("Unsupported operation")
        return Offset(self.x * other, self.y * other)
    
    def __eq__(self, other: Offset):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def manhattan_dist(self, other: Offset):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
Grid = dict[Offset, Union[str, int]]
    
class OffsetWithCount(Offset):
    count: int

    def __add__(self, other: Offset):
        return OffsetWithCount(self.x + other.x, self.y + other.y, self.count)
    
    def __sub__(self, other: Offset):
        return Offset(self.x - other.x, self.y - other.y, self.count)
    
    def __eq__(self, other: Offset):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
class GenericMap():
    _grid: dict
    _size: Offset
    
    def __init__(self, initial_grid: list[list[Any]]):
        self._grid = {Offset(x, y): col for y, row in enumerate(initial_grid) for x, col in enumerate(row)}
        self._size = Offset(len(initial_grid[0]), len(initial_grid))

    def __getitem__(self, key):
        return self._grid[key]
        
    def __setitem__(self, key, value: str):
        self._grid[key] = value
    
    def __str__(self):
        if isinstance(next(iter(self._grid.values())),str):
            return "\n" + "\n".join(["".join(row) for row in self.rows()])
        else:
            return "\n" + "\n".join([str(row) for row in self.rows()])
            # return "\n" + "\n".join(["".join([str(i) for i in row]) for row in self.rows()])
    
    def __len__(self):
        return len(self._grid)
    
    def __iter__(self):
        return iter(self._grid)
    
    def get(self, key: Any, default = None):
        return self._grid.get(key, default)

    def size(self) -> Offset:
        return self._size
    
    def rows(self):
        for y in range(self._size.y):
            yield [self._grid[Offset(x,y)] for x in range(self._size.x)]
    
    def cols(self):
        for x in range(self._size.x):
            yield [self._grid[Offset(x,y)] for y in range(self._size.y)]
    
class HeatMap(GenericMap):
    def __init__(self):
        super().__init__([list(map(int,line)) for line in yield_next_input_line() if line])

DIRECTIONS = {
    "N": Offset(0,-1),
    "E": Offset(1,0),
    "S": Offset(0,1),
    "W": Offset(-1,0)
}

POLAR_DIRECTIONS = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E"
}

@dataclass(order=True)
class QueueData:
    priority: int
    state: tuple[Offset, Offset, int]=field(compare=False) # (coord, incoming_direction, incoming_direction_count)
    heat_loss: int

def get_possible_outgoing_directions(incoming_direction: Union[Offset, str], count: int) -> list[Offset]:
    if isinstance(incoming_direction, Offset):
        incoming_direction = next((key for key, value in DIRECTIONS.items() if value == incoming_direction))
    
    return_dirs = [DIRECTIONS[direction] for direction in DIRECTIONS.keys() if direction != POLAR_DIRECTIONS[incoming_direction]]
    if count < 3:
        return return_dirs
    return [direction for direction in return_dirs if direction != DIRECTIONS[incoming_direction]]

def solve(heat_map: HeatMap):
    pq: PriorityQueue[QueueData] = PriorityQueue()
    pq.put(QueueData(0, (Offset(0,0), DIRECTIONS["E"], 0), 0))
    visited_states: dict[Offset, int] = {}
    end_coord = heat_map.size() - Offset(1,1)

    while pq:
        data = pq.get()
        state = data.state
        heat_loss = data.heat_loss
        coord, incoming_direction, incoming_direction_count = state

        next_directions = get_possible_outgoing_directions(incoming_direction, incoming_direction_count)

        for direction in next_directions:
            next_coord = coord + direction
            if not heat_map.get(next_coord):
                continue
            new_heat_loss = heat_loss + heat_map[next_coord]

            if next_coord == end_coord:
                return new_heat_loss
            
            next_state = (next_coord, direction, incoming_direction_count + 1 if direction == incoming_direction else 1)
            if visited_states.get(next_state, sys.maxsize) <= new_heat_loss:
                continue
            visited_states[next_state] = new_heat_loss

            heuristic = new_heat_loss + next_coord.manhattan_dist(end_coord)
            pq.put(QueueData(heuristic, next_state, new_heat_loss))

def solve_p1():
    global_logger.info("Solving P1")
    heat_map = HeatMap()
    logging.debug(heat_map)
    print(solve(heat_map))
    pass

def solve2(heat_map: HeatMap):
    pq: PriorityQueue[QueueData] = PriorityQueue()
    pq.put(QueueData(0, (Offset(0,0), DIRECTIONS["E"], 0), 0))
    visited_states: dict[Offset, int] = {}
    end_coord = heat_map.size() - Offset(1,1)

    while pq:
        data = pq.get()
        state = data.state
        heat_loss = data.heat_loss
        coord, incoming_direction, incoming_direction_count = state

        next_directions = get_possible_outgoing_directions(incoming_direction, incoming_direction_count - 7)

        for direction in next_directions:
            steps = 4 if direction != incoming_direction else 1
            next_coord = coord
            new_heat_loss = heat_loss

            for _ in range(steps):
                next_coord += direction
                new_heat_loss += heat_map.get(next_coord, 0)
            
            if not heat_map.get(next_coord):
                continue

            if next_coord == end_coord:
                return new_heat_loss
            
            next_state = (next_coord, direction, incoming_direction_count + 1 if direction == incoming_direction else 4)
            if visited_states.get(next_state, sys.maxsize) <= new_heat_loss:
                continue
            visited_states[next_state] = new_heat_loss

            heuristic = new_heat_loss + next_coord.manhattan_dist(end_coord)
            pq.put(QueueData(heuristic, next_state, new_heat_loss))

def solve_p2():
    global_logger.info("Solving P2")
    global_logger.info("Solving P1")
    heat_map = HeatMap()
    logging.debug(heat_map)
    print(solve2(heat_map))
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