from __future__ import annotations

import argparse
import logging

global_logger: logging.Logger

def hash_func(input: str):
    cur_value = 0
    for c in input:
        cur_value += ord(c)
        cur_value *= 17
        cur_value %= 256
    return cur_value

def yield_input():
    for line in yield_next_input_line():
        if line:
            yield from line.split(",")

def solve_p1():
    global_logger.info("Solving P1")

    acc = 0
    for input in yield_input():
        value = hash_func(input)
        logging.debug(f"{input}: {value}")
        acc += value
    print(acc)
    print(hash_func("cm"))
    pass

class LensWithLabel:
    def __init__(self, label: str, lens: int):
        self.label = label
        self.lens = lens

    def __eq__(self, other: LensWithLabel):
        if isinstance(other, LensWithLabel):
            return self.label == other.label
        elif isinstance(other, str):
            return self.label == other
        else:
            return False
        
    def __str__(self):
        return __repr__(self)

    def __repr__(self):
        return f"({self.label}, {self.lens})"
    
def print_boxes(boxes):
    out_line = [""]
    for ii, box in enumerate(boxes):
        if box and any(filter(lambda x: x!=None, box)):
            out_line.append(f"{ii}: {box}")
    return "\n".join(out_line)
    
def remove_lens(boxes: list[list], label: str):
    label_hash = hash_func(label)
    if label in boxes[label_hash]:
        remove_index = boxes[label_hash].index(label)
        boxes[label_hash].pop(remove_index)
    
def add_lens(boxes: list[list], label: str, lens: int):
    label_hash = hash_func(label)
    if label in boxes[label_hash]:
        boxes[label_hash][boxes[label_hash].index(label)] = LensWithLabel(label, lens)
    else:
        boxes[label_hash].append(LensWithLabel(label, lens))

def operate_input(boxes: list[list], input: str) -> None:
    if "=" in input:
        label, _, _lens = input.partition("=")
        add_lens(boxes, label, int(_lens))
    else:
        label, _, _ = input.partition("-")
        remove_lens(boxes, label)

def validate_lenses(boxes: list[list]):
    validation = dict()
    for ii, box in enumerate(boxes):
        for optional_lens in box:
            if optional_lens == None:
                continue
            if optional_lens.label in validation:
                raise RuntimeError(f"Existing label {optional_lens.label} exists in box {ii}")
            validation[optional_lens.label] = 1

def sum_lenses(boxes: list[list]):
    acc = 0
    for ii, box in enumerate(boxes):
        for jj, optional_lens in enumerate(box):
            if optional_lens == None:
                continue
            total = (ii + 1) * (jj + 1) * optional_lens.lens
            logging.debug(total)
            acc += total
    return acc

def solve_p2():
    global_logger.info("Solving P2")
    boxes = [[] for _ in range(256)]
    for input in yield_input():
        operate_input(boxes, input)
    validate_lenses(boxes)
    logging.debug(print_boxes(boxes))
    print(sum_lenses(boxes))

# 973259 - Too High
# 259333

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