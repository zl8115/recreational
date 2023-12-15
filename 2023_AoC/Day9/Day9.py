import argparse
import logging

global_logger: logging.Logger

import re

NUMBER_REGEX = re.compile(r"([-]?\d+)")

def all_elements_are_zero(in_list: list) -> bool:
    for ii in range(len(in_list)):
        if in_list[ii] != 0:
            return False
    return True

def str_pyramid(pyramid: list[list[int]]) -> str:
    return "\n" + "\n".join([str(line) for line in reversed(pyramid)])

def generate_pyramid(line: str) -> list[list[int]]:
    cur_line = [int(number) for number in NUMBER_REGEX.findall(line)]
    # logging.debug(cur_line)
    pyramid = [cur_line]

    while not all_elements_are_zero(cur_line):
        new_line = [cur_line[ii + 1] - cur_line[ii] for ii in range(len(cur_line) - 1)]
        if not new_line:
            new_line = [0]
        pyramid.append(new_line)
        cur_line = new_line
    return pyramid

def get_next_number(line: str):
    pyramid = generate_pyramid(line)
    for ii in range(len(pyramid)):
        pyramid[ii] += [0]

    for ii in range(len(pyramid) - 2, -1, -1):
        prev_line = pyramid[ii + 1]
        pyramid[ii][-1] = pyramid[ii][-2] + prev_line[-1]
    logging.debug(str_pyramid(pyramid))
    return pyramid[0][-1]

def solve_p1():
    global_logger.info("Solving P1")
    acc = 0
    for line in yield_next_input_line():
        prediction = get_next_number(line)
        logging.debug(prediction)
        acc += prediction
    print(acc)

# 1639599849 - too low
# 1560857236
# 1939607040 - too high
# 1939607039

def get_prev_number(line: str):
    pyramid = generate_pyramid(line)
    for ii in range(len(pyramid)):
        pyramid[ii] = [0] + pyramid[ii]

    for ii in range(len(pyramid) - 2, -1, -1):
        prev_line = pyramid[ii + 1]
        pyramid[ii][0] = pyramid[ii][1] - prev_line[0]
    logging.debug(str_pyramid(pyramid))
    return pyramid[0][0]

def solve_p2():
    global_logger.info("Solving P2")
    acc = 0
    for line in yield_next_input_line():
        prediction = get_prev_number(line)
        logging.debug(prediction)
        acc += prediction
    print(acc)

# 1041

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