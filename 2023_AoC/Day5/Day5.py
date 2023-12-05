from __future__ import annotations
import argparse
import re
from dataclasses import dataclass
from typing import Optional
import pprint

NUMBER_REGEX = re.compile(r"(\d+)")
SEED_PAIRING_REGEX = re.compile(r"(\d+\s+\d+)")
MAP_HEADER_REGEX = re.compile(r"(\w+)-to-(\w+) map:")
MAP_ENTRY_REGEX = re.compile(r"(\d+)\s+(\d+)\s+(\d+)")

def parse_input_mapping(seeds_is_range_instead_of_list: bool = False):
    mapping_dict = dict()
    current_map = None
    for line in yield_next_input_line():
        if line.startswith("seeds:"):
            seeds = []
            if not seeds_is_range_instead_of_list:
                for number in NUMBER_REGEX.findall(line):
                    seeds.append(int(number))
            else:
                seeds = parse_seeds_range_line(line)
            mapping_dict["seeds"] = seeds
        elif map_header := MAP_HEADER_REGEX.search(line):
            source, dest = map_header.groups()
            mapping_dict.setdefault("destinations", dict())[source] = dest
            current_map = dict()
            mapping_dict[source] = current_map
        elif map_entry := MAP_ENTRY_REGEX.search(line):
            destination_start, source_start, range_length = (int(val) for val in map_entry.groups())
            source_key = Range(source_start, source_start + range_length - 1)
            offset = destination_start - source_start
            current_map[source_key] = offset
    return mapping_dict

def get_seed_location(seed: int, mapping_dict: map):
    source_value = seed
    source_key = "seed"

    conversion_path = list()
    conversion_path.append(f"{source_key}: {source_value}")
    while destination_key := mapping_dict["destinations"].get(source_key):
        destination_value = source_value
        for value_range, offset in mapping_dict[source_key].items():
            if value_range.start <= source_value and source_value <= value_range.end:
                destination_value = source_value + offset
        
        source_key = destination_key
        source_value = destination_value
        conversion_path.append(f"{destination_key}: {destination_value}")
    # print(", ".join(conversion_path))
    return source_value

def solve_p1():
    mapping_dict = parse_input_mapping()
    # pprint.pprint(mapping_dict)
    # get_seed_location(mapping_dict["seeds"][0], mapping_dict)
    locations = [get_seed_location(seed, mapping_dict) for seed in mapping_dict["seeds"]]
    minimum_loc = min(locations)
    # print(locations, minimum_loc)
    print(minimum_loc)

# 88151870

@dataclass
class Range:
    start: int
    end: int

    def overlap(self, other: Range) -> Optional[Range]:
        max_start = max(self.start, other.start)
        min_end = min(self.end, other.end)
        if max_start > min_end:
            return None
        else:
            return Range(max_start, min_end)
        
    def ltrim(self, new_start: int) -> Optional[Range]:
        if new_start > self.end:
            return None
        
        return Range(new_start, self.end)
    
    def rtrim(self, new_end: int) -> Optional[Range]:
        if new_end < self.start:
            return None
        return Range(self.start, new_end)
    
    def split_overlap(self, other: Range) -> tuple[Optional[Range], Optional[Range], Optional[Range]]:
        overlap = self.overlap(other)
        left_remainder = None
        right_remainder = None
        if overlap:
            left_remainder = self.rtrim(overlap.start)
            right_remainder = self.ltrim(overlap.end)
        return (left_remainder, overlap, right_remainder)
    
    def __hash__(self):
        return hash(tuple([self.start, self.end]))

def parse_seeds_range_line(line: str) -> list[Range]:
    seeds_ranges = list()
    for seed_pair in SEED_PAIRING_REGEX.findall(line):
        seed_start, length = (int(val) for val in NUMBER_REGEX.findall(seed_pair))
        seeds_ranges.append(Range(seed_start, seed_start + length - 1))
    return seeds_ranges

def map_source_ranges_to_destination(ranges: list[Range], destination_map: dict[Range]):
    source_value = seed
    source_key = "seed"

    conversion_path = list()
    conversion_path.append(f"{source_key}: {source_value}")
    while destination_key := mapping_dict["destinations"].get(source_key):
        destination_value = source_value
        for value_range, offset in mapping_dict[source_key].items():
            if value_range[0] <= source_value and source_value <= value_range[1]:
                destination_value = source_value + offset
        
        source_key = destination_key
        source_value = destination_value
        conversion_path.append(f"{destination_key}: {destination_value}")
    # print(", ".join(conversion_path))
    return source_value

def solve_p2():
    mapping_dict = parse_input_mapping(seeds_is_range_instead_of_list=True)
    pprint.pprint(mapping_dict["seeds"])
    return 
    # get_seed_location(mapping_dict["seeds"][0], mapping_dict)
    locations = [get_seed_location(seed, mapping_dict) for seed in mapping_dict["seeds"]]
    minimum_loc = min(locations)
    # print(locations, minimum_loc)
    print(minimum_loc)

def yield_next_input_line() -> str:
    with open(r"input.txt", "r") as in_file:
        for line in in_file:
            yield line.strip()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p2", help="Solves Part 2 instead of Part 1", action='store_true', default=False)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    if not args.p2:
        solve_p1()
    else:
        solve_p2()