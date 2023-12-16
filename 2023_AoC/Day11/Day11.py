from __future__ import annotations
import argparse
import logging

global_logger: logging.Logger

from dataclasses import dataclass
import itertools

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

def load_map() -> list[list[str]]:
    star_map = list()
    for line in yield_next_input_line():
        if line:
            star_map.append([c for c in line])
    return star_map

def expand_star_map(star_map: list[list[str]]) -> list[list[str]]:
    original_width = len(star_map[0])
    original_len = len(star_map)

    columns_to_expand = list()
    rows_to_expand = list()
    
    for ii, row in enumerate(star_map):
        if all([c == "." for c in row]):
            rows_to_expand.append(ii)
    
    for jj in range(original_width):
        col = [star_map[ii][jj] for ii in range(original_len)]
        if all([c == "." for c in col]):
            columns_to_expand.append(jj)
    
    # Expand map
    expanded_map = list()
    new_width = original_width + len(columns_to_expand)
    for ii in range(original_len):
        new_row = list()
        for jj in range(original_width):
            new_row.append(star_map[ii][jj])
            if jj in columns_to_expand:
                new_row.append(".")
        expanded_map.append(new_row)
        if ii in rows_to_expand:
            expanded_map.append(["."] * new_width)
    return expanded_map

def str_star_map(star_map: list[list[str]]):
    return "\n" + "\n".join(["".join(row) for row in star_map])

def get_galaxy_coords(star_map: list[list[str]]) -> list[Offset]:
    galaxy_coords = list()
    for y, row in enumerate(star_map):
        for x, c in enumerate(row):
            if c == "#":
                galaxy_coords.append(Offset(x,y))
    return galaxy_coords

def calc_city_board_dist(p1: Offset, p2: Offset) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def sum_shortest_path_of_galaxies(star_map: list[list[str]]) -> int:
    galaxy_coords = get_galaxy_coords(star_map)
    global_logger.debug(galaxy_coords)
    acc = 0
    for pair in itertools.combinations(galaxy_coords, 2):
        total = calc_city_board_dist(pair[0], pair[1]) 
        global_logger.debug(f"{pair}: {total}")
        acc += total
    return acc

def solve_p1():
    global_logger.info("Solving P1")
    star_map = load_map()
    global_logger.debug(str_star_map(star_map))
    expanded_star_map = expand_star_map(star_map)
    global_logger.debug(str_star_map(expanded_star_map))
    print(sum_shortest_path_of_galaxies(expanded_star_map))
    pass

def get_expansion_indices(star_map):
    original_width = len(star_map[0])
    original_len = len(star_map)

    columns_to_expand = list()
    rows_to_expand = list()
    
    for ii, row in enumerate(star_map):
        if all([c == "." for c in row]):
            rows_to_expand.append(ii)
    
    for jj in range(original_width):
        col = [star_map[ii][jj] for ii in range(original_len)]
        if all([c == "." for c in col]):
            columns_to_expand.append(jj)
    return rows_to_expand, columns_to_expand

def get_galaxy_coords2(star_map: list[list[str]]) -> list[Offset]:
    rows_to_expand, columns_to_expand = get_expansion_indices(star_map)
    MULTIPLIER = 1000000

    galaxy_coords = list()
    for ii, row in enumerate(star_map):
        for jj, c in enumerate(row):
            if c == "#":
                row_expansion = next((x[0] for x in enumerate(rows_to_expand) if x[1] > ii), len(rows_to_expand))
                row_offset = MULTIPLIER * row_expansion - row_expansion
                y = ii + row_offset

                col_expansion = next((x[0] for x in enumerate(columns_to_expand) if x[1] > jj), len(columns_to_expand))
                col_offset = MULTIPLIER * col_expansion - col_expansion
                x = jj + col_offset
                galaxy_coords.append(Offset(x,y))
    return galaxy_coords

def sum_shortest_path_of_galaxies2(star_map: list[list[str]]) -> int:
    galaxy_coords = get_galaxy_coords2(star_map)
    global_logger.debug(galaxy_coords)
    acc = 0
    for pair in itertools.combinations(galaxy_coords, 2):
        total = calc_city_board_dist(pair[0], pair[1]) 
        global_logger.debug(f"{pair}: {total}")
        acc += total
    return acc

def solve_p2():
    global_logger.info("Solving P2")
    star_map = load_map()
    global_logger.debug(str_star_map(star_map))
    print(sum_shortest_path_of_galaxies2(star_map))
    pass

# 15595358

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