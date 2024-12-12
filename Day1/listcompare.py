"""
Todo:

Get two lists from txt file
Organize list
compare / sum

"""

def list_from_file(fileName) -> list: 
    with open(fileName) as file:
        return file.readlines()

def split_and_organize(list) -> list:
    list_a = [int(line.split(" ")[0].strip()) for line in list]
    list_b = [int(line.split(" ")[len(line.split(" "))-1].strip()) for line in list]
    list_a.sort()
    list_b.sort()
    return [list_a, list_b]

def sum_differences(lists) -> int:
    sum = 0
    for line in range(len(lists[0])):
        sum += abs(lists[0][line] - lists[1][line])
    return sum
            
def main():
    rawList = list_from_file('./input.txt')
    print(rawList)
    splitLists = split_and_organize(rawList)
    print(splitLists)
    sum = sum_differences(splitLists)
    print(sum)

main()