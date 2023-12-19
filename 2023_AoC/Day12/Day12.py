import argparse
import logging

global_logger: logging.Logger

import re
BROKEN_PIPE_REGEX = re.compile(r"(#+)")
NUMBER_REGEX = re.compile(r"(\d+)")

def is_valid_line(substr: str, groupings: list[int]):
    regex = BROKEN_PIPE_REGEX.findall(substr)
    if len(regex) != len(groupings):
        return False
    
    for ii, group in enumerate(regex):
        if len(group) != groupings[ii]:
            return False
    
    return True

def possible_arrangements_of_line(substr: str, groupings: list[int], replacements_left: int) -> int:
    replacement_index = substr.find("?")
    if replacement_index == -1:
        if is_valid_line(substr, groupings):
            logging.debug(substr)
            return 1
        else:
            return 0
        
    count = 0
    before, _, after = substr.partition("?")
    if replacements_left > 0:
        count += possible_arrangements_of_line("".join([before, "#", after]), groupings, replacements_left - 1)
        count += possible_arrangements_of_line("".join([before, ".", after]), groupings, replacements_left)
    else:
        count += possible_arrangements_of_line(substr.replace("?","."), groupings, 0)
    return count

def solve_p1():
    global_logger.info("Solving P1")
    acc = 0
    for line in yield_next_input_line():
        substr, _groupings = line.split(" ", 1)
        groupings = [int(g) for g in NUMBER_REGEX.findall(_groupings)]
        total = possible_arrangements_of_line(substr, groupings, sum(groupings))
        acc += total
    print(acc)
    pass

def is_valid_line_so_far(substr: str, groupings: list[int]):
    regex = BROKEN_PIPE_REGEX.findall(substr)
    if len(regex) > len(groupings):
        return False
    
    for ii, group in enumerate(regex[:-1]):
        if len(group) != groupings[ii]:
            return False
    
    return True

cache = dict()

def possible_arrangements_of_line2(substr: str, groupings: list[int]) -> int:
    if substr == "":
        return 1 if groupings == () else 0
    
    if groupings == ():
        return 0 if "#" in substr else 1
    
    key = (substr, groupings)
    if key in cache:
        return cache[key]

    count = 0
    if substr[0] in ".?":
        count += possible_arrangements_of_line2(substr[1:], groupings)
    
    if substr[0] in "#?":
        cur_group = groupings[0]
        if cur_group <= len(substr) and "." not in substr[:cur_group] and (cur_group == len(substr) or substr[cur_group] != "#"):
            count += possible_arrangements_of_line2(substr[cur_group + 1:], groupings[1:])

    cache[key] = count

    return count

def solve_p2():
    global_logger.info("Solving P2")
    acc = 0
    for line in yield_next_input_line():
        substr, _groupings = line.split(" ", 1)
        groupings = tuple(map(int, _groupings.split(",")))
        new_substr = "?".join([substr]*5)
        new_groupings = groupings * 5
        total = possible_arrangements_of_line2(new_substr, new_groupings)
        acc += total
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