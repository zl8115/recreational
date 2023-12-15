import argparse
import logging
from collections import deque

global_logger: logging.Logger

import re
import json
import pprint
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class IndexDirection:
    index: int
    direction: str

@dataclass(frozen=True)
class IndexNode:
    index: int
    node: str

MAP_ENTRY_REGEX = re.compile(r"(\w+) = \((\w+), (\w+)\)")

class CyclicDeque:
    def __init__(self, line:str):
        self._deque = deque((ii, c) for ii, c in enumerate(line))

def load_input() -> tuple[deque, dict]:
    lines = yield_next_input_line()
    sequence = deque(IndexDirection(ii, c) for ii, c in enumerate(next(lines)))
    next(lines)
    network_map = dict()
    for line in lines:
        key, left_val, right_val = MAP_ENTRY_REGEX.search(line).groups()
        network_map[key] = [left_val, right_val]
    return sequence, network_map

def solve_p1():
    global_logger.info("Solving P1")
    sequence, network_map = load_input()
    step_count = 0
    visited_set = set()

    logging.debug(json.dumps(network_map, indent=2))

    cur_key = "AAA"
    while cur_key != "ZZZ":
        step_count += 1
        idx_dir = sequence.popleft()
        logging.debug(f"{cur_key}, {idx_dir.direction}")
        sequence.append(idx_dir)
        
        if idx_dir.direction == "L":
            cur_key = network_map[cur_key][0]
        else:
            cur_key = network_map[cur_key][1]

        visited_node = IndexNode(idx_dir.index, cur_key)
        if visited_node in visited_set:
            raise RuntimeError("Error! Visited this node before")
        visited_set.add(visited_node)

    print(step_count)

@dataclass
class StepsNode():
    steps: int
    node: str

def solve_p2():
    global_logger.info("Solving P2")
    sequence, network_map = load_input()
    sequence_copy = sequence.copy()

    logging.debug(json.dumps(network_map, indent=2))
    start_keys = [key for key in network_map.keys() if key.endswith("A")]
    node_dict = dict()

    for key in start_keys:
        sequence = sequence_copy.copy()
        finish_keys = list()
        cur_key = key
        step_count = 0
        visited_set = set()
        try:
            while True:
                step_count += 1
                idx_dir = sequence.popleft()
                logging.debug(f"{cur_key}, {idx_dir.direction}")
                sequence.append(idx_dir)
                
                if idx_dir.direction == "L":
                    cur_key = network_map[cur_key][0]
                else:
                    cur_key = network_map[cur_key][1]

                visited_node = IndexNode(idx_dir.index, cur_key)
                if visited_node in visited_set:
                    raise RuntimeError("Error! Visited this node before")
                visited_set.add(visited_node)

                if cur_key.endswith("Z"):
                    finish_keys.append(StepsNode(step_count, cur_key))
        except RuntimeError:
            pass
        finally:
            node_dict[key] = finish_keys
    
    pprint.pprint(node_dict) # It looks like it's nice and only give 1 finish key per start
    step_list = [steps[0].steps for steps in node_dict.values()]
    logging.info(step_list)
    # print(naive_increment_till_same(step_list))
    print(lowest_common_multiple(step_list))
    # print(math.lcm(*step_list))

def all_elements_are_equal(in_list: list) -> bool:
    for ii in range(len(in_list) - 1):
        if in_list[ii] != in_list[ii + 1]:
            return False
    return True

def naive_increment_till_same(step_list: list) -> int:
    inc_list = step_list.copy()
    while not all_elements_are_equal(inc_list):
        lowest_idx = inc_list.index(min(inc_list))
        inc_list[lowest_idx] += step_list[lowest_idx]
    return inc_list[0]

# Found this online
def get_prime_numbers(n: int) -> list[int]:
    sieve = [True] * n
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3,n,2) if sieve[i]]

def get_prime_factors(number: int) -> list[int]:
    primes = []
    for prime in get_prime_numbers(number):
        if number % prime == 0:
            primes.append(prime)
    logging.info(f"{number}: {primes}")
    return primes

def lowest_common_multiple(numbers: list[int]) -> int:
    prime_set = set()
    for number in numbers:
        prime_set.update(get_prime_factors(int(number)))
    logging.info(prime_set)
    return math.prod(prime_set)

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