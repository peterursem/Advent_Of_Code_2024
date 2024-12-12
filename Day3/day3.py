import re

VALID_CALL_REGEX = "(mul\([0-9]+,[0-9]+\))|(do\(\))|(don't\(\))"

def read_file(fileName: str) -> str: 
    with open(fileName) as file:
        return file.read()
    
def find_valid_calls(text: str) -> list:
    search = re.findall(VALID_CALL_REGEX, text)
    calls = []
    for results in search:
        result = ""
        for comp in results:
            result += comp
        calls.append(result)
    return calls

def run_mul(call: str) -> int:
        values = [int(val) for val in call.split('mul(')[1].split(')')[0].split(",")]
        return values[0] * values[1]

def main():
    sum = 0
    do = True

    for call in find_valid_calls(read_file('./Day3/input.txt')):
        if call.count("don't") > 0:
            do = False
        elif call.count("do") > 0:
            do = True
        elif call.count("mul") > 0 and do:
            sum += run_mul(call)

    print(sum)

main()