import argparse
import re
import math

NUMBER_REGEX = re.compile(r"(\d+)")
USE_TEST_INPUT = False

def get_time_distance_pairs(strip_whitespace: False) -> list[tuple[int, int]]:
    times = list()
    distances = list()
    for line in yield_next_input_line():
        if strip_whitespace:
            line = line.replace(" ","")
        if line.startswith("Time:"):
            for time in NUMBER_REGEX.findall(line):
                times.append(int(time))
        elif line.startswith("Distance:"):
            for dist in NUMBER_REGEX.findall(line):
                distances.append(int(dist))
    assert(len(times) == len(distances))
    return [(times[ii], distances[ii]) for ii in range(len(times))]

def get_number_of_ways_to_beat_the_record(record_time: int, record_dist: int) -> int:
    sqrt = math.sqrt((record_time**2) - (4*record_dist))
    lower_bound = (record_time - sqrt)/2
    lower_bound = lower_bound + 1 if lower_bound.is_integer() else math.ceil(lower_bound)
    upper_bound = (record_time + sqrt)/2
    upper_bound = upper_bound - 1 if upper_bound.is_integer() else math.floor(upper_bound)
    # print(lower_bound, upper_bound)
    return int(upper_bound - lower_bound + 1)

def solve_p1():
    num_list = list()
    for time, dist in get_time_distance_pairs():
        num_list.append(get_number_of_ways_to_beat_the_record(time, dist))
    # print(num_list)
    print(math.prod(num_list))

def solve_p2():
    num_list = list()
    for time, dist in get_time_distance_pairs(strip_whitespace=True):
        num_list.append(get_number_of_ways_to_beat_the_record(time, dist))
    # print(num_list)
    print(math.prod(num_list))

def yield_next_input_line() -> str:
    input_file = r"input.txt" if not USE_TEST_INPUT else r"test-input.txt"

    with open(input_file, "r") as in_file:
        for line in in_file:
            yield line.strip()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p2", help="Solves Part 2 instead of Part 1", action='store_true', default=False)
    parser.add_argument("--test", "-t", help="Use test-input.txt instead of input.txt", action='store_true', default=False)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    USE_TEST_INPUT = args.test

    if not args.p2:
        solve_p1()
    else:
        solve_p2()