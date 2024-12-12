import pytest
import day5

RULES = [
    "47|53",
    "97|13",
    "97|61",
    "97|47",
    "75|29",
    "61|13",
    "75|53",
    "29|13",
    "97|29",
    "53|29",
    "61|53",
    "97|53",
    "61|29",
    "47|13",
    "75|47",
    "97|75",
    "47|61",
    "75|61",
    "47|29",
    "75|13",
    "53|13"
]

PRINTS = [
    [75,47,61,53,29],
    [97,61,53,29,13],
    [75,29,13],
    [75,97,47,61,53],
    [61,13,29],
    [97,13,75,29,47]
]

VALIDPRINTS = [
    [75,47,61,53,29],
    [97,61,53,29,13],
    [75,29,13],
    [97,75,47,61,53],
    [61,29,13],
    [97,13,75,29,47]
]

RULECOMPONENTS = [
    [47,53],
    [97,13],
    [97,61],
    [97,47],
    [75,29],
    [61,13],
    [75,53],
    [29,13],
    [97,29],
    [53,29],
    [61,53],
    [97,53],
    [61,29],
    [47,13],
    [75,47],
    [97,75],
    [47,61],
    [75,61],
    [47,29],
    [75,13],
    [53,13]
]

VIOLATION = [
    None,
    None,
    None,
    "97|75",
    "29|13",
    "75|13"
]

MIDDLES = [
    61,
    53,
    29,
    47,
    13,
    75
]

MIDDLESUM = 278

VIOLATIONS = [
    ['47|75', '61|75', '53|75', '29|75', '61|47', '53|47', '29|47', '53|61', '29|61', '29|53'],
    ['61|97', '53|97', '29|97', '13|97', '53|61', '29|61', '13|61', '29|53', '13|53', '13|29'],
    ['29|75', '13|75', '13|29'],
    ['97|75', '47|75', '61|75', '53|75', '47|97', '61|97', '53|97', '61|47', '53|47', '53|61'],
    ['13|61', '29|61', '29|13'],
    ['13|97', '75|97', '29|97', '47|97', '75|13', '29|13', '47|13', '29|75', '47|75', '47|29']
]

def test_violations_in_print():
    for index in range(len(PRINTS)):
        assert day5.print_inverted_rules(PRINTS[index]) == VIOLATIONS[index]

def test_make_rule():
    for index in range(len(RULECOMPONENTS)):
        assert day5.make_rule(RULECOMPONENTS[index][0], RULECOMPONENTS[index][1]) == RULES[index]

def test_check_validity():
    for index in range(len(PRINTS)):
        valid = day5.print_violation(PRINTS[index], RULES)
        assert valid == VIOLATION[index]

def test_middle_page(prints = PRINTS, middles = MIDDLES):
    for index in range(len(prints)):
        assert day5.middle_page(prints[index]) == middles[index]

def test_sum_middle_page(prints = PRINTS, middle_sum = MIDDLESUM):
    assert day5.sum_middle_pages(prints) == middle_sum

def test_fix_print():
    for index in range(len(VIOLATION)):
        if VIOLATION[index] == False:
            assert day5.fix_print(PRINTS[index]) == VALIDPRINTS[index]