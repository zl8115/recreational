import argparse
import re

CARD_NUMBER_REGEX = re.compile(r"Card\s+(\d+):")
NUMBER_REGEX = re.compile(r"(\d+)")

def numbers_line_to_dict(line: str):
    numbers_list = list(NUMBER_REGEX.findall(line))
    numbers_dict = dict(zip(numbers_list, list(range(1, len(numbers_list) + 1))))
    return numbers_dict

def get_line_winners(line: str):
    numbers = line.split(":")[1].strip()
    my_numbers, winning_numbers = numbers.split("|", 1)
    my_numbers = list(NUMBER_REGEX.findall(my_numbers))
    winning_numbers_dict = numbers_line_to_dict(winning_numbers)

    winners = list()
    for number in my_numbers:
        if winning_numbers_dict.get(number):
            winners.append(number)
    return winners

def solve_p1():
    acc = 0
    for line in yield_next_input_line():
        card_number = CARD_NUMBER_REGEX.findall(line)[0]
        winners = get_line_winners(line)
        winners.sort()
        if len(winners) > 0:
            value = 2**(len(winners) - 1)
            print(value)
            acc += value
        print(f"Card {card_number}: {winners}")
    print(acc)

# 19377 - too low
# 23750

def solve_p2():
    acc = 0
    card_count = [1] * 10 # 10 is maximum no of wins
    for line in yield_next_input_line():
        card_number = CARD_NUMBER_REGEX.findall(line)[0]

        cur_card_count = card_count.pop(0)
        card_count.append(1)

        winners = get_line_winners(line)
        acc += cur_card_count

        for ii in range(len(winners)):
            card_count[ii] += cur_card_count
        print(f"Card {card_number}: {winners} x{cur_card_count}")
    print(acc)

# 26523700 - too high
# 13261850

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