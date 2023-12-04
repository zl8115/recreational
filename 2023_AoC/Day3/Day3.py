import argparse

def is_symbol(char: str):
    return char != '.' and not char.isdigit()

def get_middle_line_part_numbers(prev_line: str, cur_line: str, next_line: str) -> list[int]:
    acc_list = []
    ii = 0
    while ii < len(cur_line):
        if cur_line[ii].isdigit():
            num_start = ii
            num_end = ii
            while num_end < len(cur_line) and cur_line[num_end].isdigit():
                num_end += 1
            
            is_part_number = False
            left_index = num_start - 1 if num_start > 0 else num_start
            right_index = num_end + 1 if num_end < len(cur_line) else num_end
            for jj in range(left_index, right_index):
                top_char = prev_line[jj]
                bottom_char = next_line[jj]
                if is_symbol(top_char):
                    is_part_number = True
                    break
                if is_symbol(bottom_char):
                    is_part_number = True
                    break
            if num_start > 0 and is_symbol(cur_line[num_start - 1]):
                is_part_number = True
                
            if num_end < len(cur_line) and is_symbol(cur_line[num_end]):
                is_part_number = True
                
            if is_part_number:
                number = cur_line[num_start:num_end]
                acc_list.append(int(number))
            if ii == num_end:
                ii += 1
            else:
                ii = num_end
        else:
            ii += 1
    return acc_list

def solve_p1():
    acc = 0
    prev_line = "." * 140
    prev_prev_line = prev_line
    line_number = 0
    for line in yield_next_input_line():
        acc_list = get_middle_line_part_numbers(prev_prev_line, prev_line, line)
        print(f"Line {line_number}: {acc_list}")
        acc += sum(acc_list)
        prev_prev_line = prev_line
        prev_line = line
        line_number += 1

    acc_list = get_middle_line_part_numbers(prev_prev_line, prev_line, "." * 140)
    print(f"Line {line_number}: {acc_list}")
    acc += sum(acc_list)    
    print(acc)

# 346384 - too low
# 347650 - too low
# 534300 - ???
# 540025

def is_gear_symbol(char: str):
    return char == "*"

def get_line_values(line: str, search_range: list[int]) -> list[int]:
    altered_search_range = search_range
    values = []
    for idx in search_range:
        if idx not in altered_search_range:
            continue
        if line[idx].isdigit():
            start = idx
            end = idx
            while start >= 0 and line[start].isdigit():
                start -= 1
            while end < len(line) and line[end].isdigit():
                end += 1
                if end in altered_search_range:
                    altered_search_range.pop(altered_search_range.index(end))
            values.append(int(line[start+1:end]))
    return values

def get_middle_line_gear_ratios(prev_line, cur_line, next_line):
    gear_ratios = []
    for idx, char in enumerate(cur_line):
        if is_gear_symbol(char):
            start_idx = idx - 1 if idx > 0 else idx
            end_idx = idx + 1 if idx + 1 < len(cur_line) else idx
            values = []
            values += get_line_values(prev_line, list(range(start_idx, end_idx + 1)))
            values += get_line_values(cur_line, list(range(start_idx, end_idx + 1)))
            values += get_line_values(next_line, list(range(start_idx, end_idx + 1)))
            if len(values) == 2:
                gear_ratios.append(values)
    return gear_ratios

def solve_p2():
    acc = 0
    prev_line = "." * 140
    prev_prev_line = prev_line
    line_number = 0
    for line in yield_next_input_line():
        gear_ratios = get_middle_line_gear_ratios(prev_prev_line, prev_line, line)
        print(f"Line {line_number}: {gear_ratios}")
        acc += sum([ratio[0]*ratio[1] for ratio in gear_ratios])
        prev_prev_line = prev_line
        prev_line = line
        line_number += 1

    gear_ratios = get_middle_line_gear_ratios(prev_prev_line, prev_line, "." * 140)
    print(f"Line {line_number}: {gear_ratios}")
    acc += sum([ratio[0]*ratio[1] for ratio in gear_ratios])
    print(acc)

# 84584891

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