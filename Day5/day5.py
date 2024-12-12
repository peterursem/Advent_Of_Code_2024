'''
Input list

Load print set
Extract comparisons for each value
Swap comparison order 1|2 -> 2|1
Check for match. If it exists, line is invalid.

'''

FILENAME = "./Day5/input.txt"

def print_inverted_rules(pages: list) -> list:
    rules = []
    for first_index in range(len(pages)):
        for comp_index in range(len(pages)):
            rule = ""
            if comp_index == first_index:
                continue
            # For each pair of numbers, invert them to find the rule they break
            elif comp_index < first_index:
                rule = make_rule(pages[first_index], pages[comp_index])
            else:
                rule = make_rule(pages[comp_index], pages[first_index])
            if not rule in rules:
                rules.append(rule)
    return rules

def make_rule(earlier: int, later: int) -> str:
    return f'{earlier}|{later}'

def print_violation(pages: list, rules: list) -> bool:
    for violation in print_inverted_rules(pages):
        if violation in rules:
            return violation
    return None

def load_file(filename: str) -> list:
    with open(filename) as file:
        clean_lines = [line.strip() for line in file.readlines()]
        split = clean_lines.index('')
        return {"rules": clean_lines[:split], "prints": [[int(val) for val in line.split(',')] for line in clean_lines[split+1:]]}
    
def filter(prints: list, rules: list, valid: bool = True) -> list:
    filtered = []
    for pages in prints:
        if (print_violation(pages, rules) == None) == valid:
            filtered.append(pages)
    return filtered

def sum_middle_pages(prints: list) -> int:
    sum = 0
    for pages in prints:
        sum += middle_page(pages)
    return sum

def middle_page(pages: list) -> int:
    return pages[int(len(pages)/2)]

def fix_print(pages: list, rules: list) -> list:
    print = pages.copy()
    violation = print_violation(print, rules)

    while not violation == None:
        violations = [int(val) for val in violation.split("|")]
        print[print.index(violations[0])] = violations[1]
        print[print.index(violations[1])] = violations[0]
        violation = print_violation(print, rules)
    
    return print

def main():
    file = load_file(FILENAME)
    valid_prints = filter(file["prints"], file["rules"])
    invalid_prints = filter(file["prints"], file["rules"], False)
    fixed_prints = [fix_print(pages, file["rules"]) for pages in invalid_prints]

    print(f'Sum of middle pages of correct prints = {sum_middle_pages(valid_prints)}')
    print(f'Sum of middle pages of fixed prints = {sum_middle_pages(fixed_prints)}')
        
main()