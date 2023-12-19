import argparse
import logging

global_logger: logging.Logger

def load_map() -> list[list[str]]:
    return [[c for c in line] for line in yield_next_input_line() if line]

def move_map_north(cur_map: list[str]) -> list[str]:
    new_map = [[c if c != "O" else "." for c in line] for line in cur_map]

    for ii, line in enumerate(cur_map):
        for jj, c in enumerate(line):
            if c == "O":
                kk = ii
                while kk - 1 in range(ii + 1) and new_map[kk - 1][jj] not in "#O":
                    kk -= 1
                new_map[kk][jj] = c

    return new_map

def print_map(cur_map: list[list[str]]):
    return "\n".join(["", *["".join(line) for line in cur_map]])

def calculate_load_of_map(cur_map: list[list[str]]):
    acc = 0
    for ii, line in enumerate(cur_map[::-1]):
        count = "".join(line).count("O")
        acc += (ii + 1) * count
    return acc

def solve_p1():
    global_logger.info("Solving P1")
    cur_map = load_map()
    logging.debug(print_map(cur_map))
    north_map = move_map_north(cur_map)
    logging.debug(print_map(north_map))
    total = calculate_load_of_map(north_map)
    print(total)

def rotate_map_clockwise(cur_map: list[list[str]]):
    return list(zip(*cur_map[::-1]))

def cycle_map(cur_map: list[list[str]]):
    new_map = cur_map
    for _ in range(4):
        new_map = move_map_north(new_map)
        new_map = rotate_map_clockwise(new_map)
    return new_map

def hash_map(cur_map):
    if cur_map == None:
        return 0
    return hash(tuple(("".join(line) for line in cur_map)))

def cycle_detection(cur_map):
    mu = 0
    tort = cycle_map(cur_map)
    hare = cycle_map(cycle_map(cur_map))
    while hash_map(tort) != hash_map(hare):
        tort = cycle_map(tort)
        hare = cycle_map(cycle_map(hare))

    mu = 0
    tort = cur_map
    while tort != hare:
        tort = cycle_map(tort)
        hare = cycle_map(hare)
        mu += 1
 
    lam = 1
    hare = cycle_map(tort)
    while tort != hare:
        hare = cycle_map(hare)
        lam += 1
 
    return lam, mu

def solve_p2():
    global_logger.info("Solving P2")
    cur_map = load_map()
    logging.debug(print_map(cur_map))
    rotated_map = cur_map

    lam, mu = cycle_detection(cur_map)
    logging.debug(lam)
    logging.debug(mu)

    cycle = (1000000000 - mu) % lam
    rotated_map = cur_map
    for _ in range(mu + cycle):
        rotated_map = cycle_map(rotated_map)
    total = calculate_load_of_map(rotated_map)
    print(total)

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