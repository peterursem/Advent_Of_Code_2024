import math
import functools

def run_rules(value):
    if value == 0:
        return (1, None)
    
    digits = math.floor(math.log10(value)) + 1
    
    if digits % 2 == 0:
        half = digits // 2
        tens = 10 ** half
        return (value // tens, value % tens)
    
    return (value * 2024, None)

@functools.cache
def update_count(stone, depth):
    l, r = run_rules(stone)

    if depth == 1:
        if r == None:
            return 1
        else:
            return 2
    
    else:
        out = update_count(l, depth-1)
        if r != None:
            out += update_count(r, depth-1)
        return out

def loop(stones, count):
    number = 0
    for stone in stones:
        number += update_count(stone, count)
    print(f'{number} Stones after {count} blinks')
    
def main():
    stones = [5,62914,65,972,0,805922,6521,1639064]
    loop(stones, 25)
    loop(stones, 75)
    loop(stones, 497)

main()