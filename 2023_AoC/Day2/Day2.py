import re
import math
import argparse

GAME_SET_REGEX = re.compile(r"(\d+) (\w+)")
GAME_ID_REGEX = re.compile(r"Game (\d+)")

def get_game_sets(line: str) -> str:
    return [game.strip() for game in line.split(":")[1][1:].split(";")]

def possible_game(line: str):
    game_sets = get_game_sets(line)
    for game_set in game_sets:
        for match in GAME_SET_REGEX.findall(game_set):
            if match[1] == 'red' and int(match[0]) > 12:
                print(match)
                return False
            elif match[1] == 'green' and int(match[0]) > 13:
                print(match)
                return False
            elif match[1] == 'blue' and int(match[0]) > 14:
                print(match)
                return False
    return True

def get_game_power_set(line: str):
    game_sets = get_game_sets(line)
    min_cubes_dict = {
        'red': 0,
        'green': 0,
        'blue': 0
    }

    for game_set in game_sets:
        for match in GAME_SET_REGEX.findall(game_set):
            if int(match[0]) > min_cubes_dict[match[1]]:
                min_cubes_dict[match[1]] = int(match[0])
    return math.prod(min_cubes_dict.values())

def get_game_id(line: str) -> int:
    id = int(GAME_ID_REGEX.findall(line)[0])
    print(id)
    return id

def solve(isPart2: bool = False):
    with open(r"input.txt", "r") as in_file:
        accumulator = 0
        for line in in_file:
            if not isPart2 and possible_game(line):
                accumulator += get_game_id(line)
            elif isPart2:
                accumulator += get_game_power_set(line)
        
        print(accumulator)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p2", help="Solves Part 2 instead of Part 1", action='store_true', default=False)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    solve(args.p2)