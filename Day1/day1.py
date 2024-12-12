"""
Todo:

Get two lists from txt file
Organize list
compare / sum

"""

def list_from_file(fileName) -> list: 
    with open(fileName) as file:
        return file.readlines()
    
def split_lists(lists):
    list_a = [int(line.split(" ")[0].strip()) for line in lists]
    list_b = [int(line.split(" ")[len(line.split(" "))-1].strip()) for line in lists]
    return [list_a, list_b]

def organize(list_a, list_b) -> list:
    list_a.sort()
    list_b.sort()
    return [list_a, list_b]

def sum_differences(lists) -> int:
    sum = 0
    for line in range(len(lists[0])):
        sum += abs(lists[0][line] - lists[1][line])
    return sum

def similiarity_score(lists) -> int:
    sum = 0
    for line in range(len(lists[0])):
        val = lists[0][line]
        sum += val * lists[1].count(val)
    return sum
            
def main():
    rawList = list_from_file('./Day1/input.txt')
    splitlists = split_lists(rawList)
    organized_lists = organize(splitlists[0].copy(), splitlists[1].copy())
    sum = sum_differences(organized_lists)
    score = similiarity_score(splitlists)

    print(f'{"Sum:":<18}{sum}\nSimilarity Score: {score}')

main()