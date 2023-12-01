def replace_number_words_with_numbers(text: str):
    ii = 0
    altered_text = ""
    while ii < len(text):
        if text[ii:].startswith("one"):
            altered_text += "1"
        elif text[ii:].startswith("two"):
            altered_text += "2"
        elif text[ii:].startswith("three"):
            altered_text += "3"
        elif text[ii:].startswith("four"):
            altered_text += "4"
        elif text[ii:].startswith("five"):
            altered_text += "5"
        elif text[ii:].startswith("six"):
            altered_text += "6"
        elif text[ii:].startswith("seven"):
            altered_text += "7"
        elif text[ii:].startswith("eight"):
            altered_text += "8"
        elif text[ii:].startswith("nine"):
            altered_text += "9"
        else:
            altered_text += text[ii]
        ii += 1
    return altered_text

def solve():
    with open(r"C:\dev\Others\AoC\input.txt", "r") as in_file:
        vals = list()
        for line in in_file:
            start: chr = ''
            end: chr = ''
            # for c in line.strip():
            for c in replace_number_words_with_numbers(line.strip()):
                if c.isdigit():
                    if not start:
                        start = c
                    end = c
            
            if start:
                val = int(start + end)
                vals.append(val)
        
        print(sum(vals))

if __name__ == "__main__":
    solve()