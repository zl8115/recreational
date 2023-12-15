from __future__ import annotations
import argparse
import logging

global_logger: logging.Logger

from dataclasses import dataclass
from collections import deque

# Going to abuse this class to mean x-y coords too
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
    
class PipeMap:
    _map: list[list[str]]
    start: Offset

    def __init__(self):
        self._map = list()
        is_first_line = True
        line_idx = 1
        for line in yield_next_input_line():
            if is_first_line:
                self._map.append(["."]*(len(line) + 2))
                is_first_line = False
            self._map.append(["."] + list(line) + ["."])
            if "S" in self._map[line_idx]:
                self.start = Offset(self._map[line_idx].index("S"), line_idx)
            line_idx += 1
        self._map.append(["."]*len(line))

    def __getitem__(self, offset: Offset):
        return self._map[offset.y][offset.x]
    
    def __str__(self):
        return "\n" + "\n".join(["".join(line) for line in self._map])
    
    def __len__(self):
        return len(self._map)
    
class VisitedMap:
    _map: list[list[int]]
    start: Offset

    def __init__(self, pipe_map: PipeMap|VisitedMap):
        self._map = list()
        for _ in range(len(pipe_map)):
            self._map.append([-1] * len(pipe_map._map[0]))

    def __getitem__(self, offset: Offset):
        return self._map[offset.y][offset.x]
    
    def __setitem__(self, offset: Offset, value: bool):
        self._map[offset.y][offset.x] = value
    
    def __str__(self):
        return "\n" + "\n".join(["".join(str(line)) for line in self._map])
    
    def __len__(self):
        return len(self._map)
    
    def __iter__(self):
        return iter(self._map)
    
def get_farthest_distance(pipe_map: PipeMap, visited_map: VisitedMap):
    queue = deque()
    queue.append(pipe_map.start)
    depth = 0

    while True:
        logging.debug(queue)
        new_queue = deque()
        while queue:
            cur_coord = queue.popleft()
            visited_map[cur_coord] = depth
            neighbors = get_possible_neighbouring_pipes(pipe_map, cur_coord)
            for neighbor in neighbors:
                if visited_map[neighbor]  != -1:
                    continue
                new_queue.append(neighbor)
        if not new_queue:
            break
        depth += 1
        queue = new_queue
    logging.debug(visited_map)
    return depth

POSSIBLE_PIPE_CONNECTIONS = {
    "|": [Offset(0,1),Offset(0,-1)],
    "-": [Offset(1,0),Offset(-1,0)],
    "L": [Offset(0,-1),Offset(1,0)],
    "J": [Offset(0,-1),Offset(-1,0)],
    "7": [Offset(0,1),Offset(-1,0)],
    "F": [Offset(0,1),Offset(1,0)],
    "S": [Offset(1,0),Offset(0,1),Offset(-1,0),Offset(0,-1)],
    ".": []
}

def pipe_can_return_to_origin(pipe_symbol:str, pipe_coords: Offset, original_coords: Offset):
    for offset in POSSIBLE_PIPE_CONNECTIONS[pipe_symbol]:
        if pipe_coords + offset == original_coords:
            return True
    return False

def get_possible_neighbouring_pipes(pipe_map: PipeMap, coords: Offset) -> list[Offset]:
    neighbors = []
    visible_offsets = POSSIBLE_PIPE_CONNECTIONS[pipe_map[coords]]
    for offset in visible_offsets:
        new_coords = coords + offset
        if pipe_can_return_to_origin(pipe_map[new_coords], new_coords, coords):
            neighbors.append(new_coords)
    return neighbors

def solve_p1():
    global_logger.info("Solving P1")
    
    pipe_map = PipeMap()
    logging.debug(pipe_map)
    logging.debug(f"Start Offset: {pipe_map.start}")
    visited_map = VisitedMap(pipe_map)

    print(get_farthest_distance(pipe_map, visited_map))
    logging.info(visited_map)

def get_vertex_points(pipe_map: PipeMap, visited_map: VisitedMap):
    # Mad Science behavior. We know that the pipes can only ever have 2 possible neighbors
    # so besides the start point, each pipe will only have 1 neighbor. So when traversing
    # the DFS, each depth will traverse the first pipe path, then the second. So we string
    # the paths that way, and we reverse append the second path to get the remaining half
    # of the pipe loop.
    vertices = [list(), list()]

    queue = deque()
    queue.append(pipe_map.start)
    depth = 0

    while True:
        logging.debug(queue)
        new_queue = deque()
        for ii, cur_coord in enumerate(queue):
            vertices[ii].append(cur_coord)
            visited_map[cur_coord] = depth
            neighbors = get_possible_neighbouring_pipes(pipe_map, cur_coord)
            for ii, neighbor in enumerate(neighbors):
                if visited_map[neighbor]  != -1:
                    continue
                new_queue.append(neighbor)
        if not new_queue:
            break
        depth += 1
        queue = new_queue
    logging.debug(visited_map)

    return_vertices = [*vertices[0]] + list(reversed(vertices[1]))
    return return_vertices

def cross_product(l_coord: Offset, r_coord: Offset):
    return (l_coord.x * r_coord.y) - (r_coord.x * l_coord.y)

def shoelace_formula(coordinates: list[Offset]):
    acc = 0
    looped_list = [*coordinates, coordinates[0]]
    for ii in range(len(coordinates)):
        acc += cross_product(looped_list[ii], looped_list[ii + 1])
    return acc / 2

# Pick's Theorem
def get_interior_points_from_area(area: int, boundary_points: float):
    interior = abs(area) - (boundary_points/2) + 1
    return int(interior)

def solve_p2():
    global_logger.info("Solving P2")
    pipe_map = PipeMap()
    visited_map = VisitedMap(pipe_map)

    boundary_coords = get_vertex_points(pipe_map, visited_map)
    logging.debug(boundary_coords)
    area = shoelace_formula(boundary_coords)
    logging.debug(area)
    interior_points = get_interior_points_from_area(area, len(boundary_coords))
    print(interior_points)

# 352 - but I have an off by 1 error so it's 353 and correct 🤷

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