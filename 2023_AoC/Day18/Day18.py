from __future__ import annotations
import argparse
import logging

global_logger: logging.Logger

from dataclasses import dataclass

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
    
DIRECTIONS = {
    "D": Offset(0,-1),
    "L": Offset(1,0),
    "U": Offset(0,1),
    "R": Offset(-1,0)
}

def load_dig_site_vertices() -> tuple[list[Offset], int]:
    cur_pos = Offset(0,0)
    vertices_coords = []
    vertices_count = 0
    for line in yield_next_input_line():
        if not line:
            continue
        vertices_coords.append(cur_pos)

        direction_char, step_char, _ = line.split(" ")
        step = int(step_char)
        vertices_count += step

        direction = DIRECTIONS[direction_char] * step
        cur_pos += direction
    assert (cur_pos == Offset(0,0))
    
    return vertices_coords, vertices_count

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

def solve_p1():
    global_logger.info("Solving P1")

    vertices_coords, vertices_count = load_dig_site_vertices()
    logging.debug(f"Boundary Points: {vertices_count}")
    interior_points = get_interior_points_from_area(shoelace_formula(vertices_coords), vertices_count)
    logging.debug(f"Interior Points: {interior_points}")
    print(vertices_count + interior_points)

HEX_DIRECTION = "RDLU"

def load_dig_site2() -> tuple[list[Offset], int]:
    cur_pos = Offset(0,0)
    dig_site = []
    vertices = 0
    for line in yield_next_input_line():
        if not line:
            continue
        dig_site.append(cur_pos)

        _, _, hex_str = line.split(" ") # "_ _ (#70c710)"
        
        hex_step =  "0x" + hex_str[2:-2] # Remove leading "(#" and trailing ")"
        step = int(hex_step, 0)
        vertices += step

        hex_dir = hex_str[-2]
        direction_char = HEX_DIRECTION[int(hex_dir)]
        direction = DIRECTIONS[direction_char] * step
        cur_pos += direction
    assert (cur_pos == Offset(0,0))
    
    return dig_site, vertices

def solve_p2():
    global_logger.info("Solving P2")

    dig_site, vertices = load_dig_site2()
    logging.debug(f"Boundary Points: {vertices}")
    interior_points = get_interior_points_from_area(shoelace_formula(dig_site), vertices)
    logging.debug(f"Interior Points: {interior_points}")
    print(vertices + interior_points)

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