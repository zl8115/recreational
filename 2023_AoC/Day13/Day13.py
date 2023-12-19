import argparse
import logging

global_logger: logging.Logger

from typing import Optional
import math

def load_maps() -> list[list[list[str]]]:
    new_map = True
    cur_map = list()
    map_list = list()

    for line in yield_next_input_line():
        if not line:
            new_map = True
            continue
        
        if new_map and cur_map:
            map_list.append(cur_map)
            cur_map = list()
        
        new_map = False
        cur_map.append([c for c in line])

    map_list.append(cur_map)
    return map_list

def print_map(cur_map):
    return "\n" + "\n".join(["".join(row) for row in cur_map])

def get_horizontal_reflection(cur_map: list[list[str]]) -> Optional[int]:
    for ii in range(1, len(cur_map)):
        above = cur_map[:ii][::-1]
        below = cur_map[ii:]

        if all((x == y) for x, y in zip(above, below)):
            return ii
    return None

def rotate_map(cur_map: list[list[str]]) -> list[list[str]]:
    return list(zip(*cur_map))

def get_vertical_reflection(cur_map: list[list[str]]) -> Optional[int]:
    return get_horizontal_reflection(rotate_map(cur_map))

def get_reflection(cur_map: list[list[str]]) -> int:
    reflection = get_horizontal_reflection(cur_map)
    if not reflection:
        reflection = get_vertical_reflection(cur_map)
        logging.info(f"Vertical Reflection: {reflection}")
    else:
        reflection *= 100
        logging.info(f"Horizontal Reflection: {reflection}")

    if reflection == None:
        logging.error(print_map(cur_map))
        assert(reflection != None)
    return reflection

def solve_p1():
    global_logger.info("Solving P1")
    maps = load_maps()
    logging.debug(len(maps))
    acc = 0
    for cur_map in maps:
        logging.debug(print_map(cur_map))
        acc += get_reflection(cur_map)
    print(acc)

def get_horizontal_reflection2(cur_map: list[list[str]]) -> Optional[int]:
    for ii in range(1, len(cur_map)):
        above = cur_map[:ii][::-1]
        below = cur_map[ii:]

        if sum(sum(0 if x_c == y_c else 1 for x_c, y_c in zip(x_line, y_line)) for x_line, y_line in zip(above, below)) == 1:
            return ii
    return None

def get_vertical_reflection2(cur_map: list[list[str]]) -> Optional[int]:
    return get_horizontal_reflection2(rotate_map(cur_map))

def get_reflection2(cur_map: list[list[str]]) -> int:
    reflection = get_horizontal_reflection2(cur_map)
    if not reflection:
        reflection = get_vertical_reflection2(cur_map)
        logging.info(f"Vertical Reflection: {reflection}")
    else:
        reflection *= 100
        logging.info(f"Horizontal Reflection: {reflection}")

    if reflection == None:
        logging.error(print_map(cur_map))
        assert(reflection != None)
    return reflection

def solve_p2():
    global_logger.info("Solving P2")
    maps = load_maps()
    logging.debug(len(maps))
    acc = 0
    for cur_map in maps:
        logging.debug(print_map(cur_map))
        acc += get_reflection2(cur_map)
    print(acc)
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