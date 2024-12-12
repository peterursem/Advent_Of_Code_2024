from enum import Enum
from itertools import permutations, product

def multiply(a, b):
    return a * b

def add(a, b):
    return a + b

def concat(a, b):
    return int(f"{a}{b}")

class OPERATORS(Enum):
    MULTIPLICATION = multiply, 0
    ADDITION = add, 1
    CONCATINATION = concat, 2
    
    def __init__(self, func, index):
        self.NAME = self.name
        self.FUNC = func
        self.INDEX = index

    @classmethod
    def _missing_(cls, query):
        for member in cls:
            if query in [member.NAME, member.INDEX]:
                return member

def verify(line):
    goal, components = line.strip().split(":")
    values = list(map(int, components.strip().split(" ")))

    num_operations = len(values) - 1
    operations = generate_patterns(num_operations)
    for operation in operations:
        result = values[0]
        for index, op_index in enumerate(operation):
            result = OPERATORS(op_index).FUNC(result, values[index + 1])
        if result == int(goal):
            return result
    
    return None

def generate_patterns(n):
    return list(product(range(len(OPERATORS)), repeat=n))

def sum_valid_lines(file):
    sum = 0
    for line in file:
        result = verify(line)
        if result:
            sum += result
    return sum

def load_file(filename): 
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]

def main():
    file = load_file("./Day7/input.txt")
    print(sum_valid_lines(file))

main()