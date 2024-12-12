def list_from_file(fileName) -> list: 
    with open(fileName) as file:
        return file.readlines()

def split_list(list) -> list:
    list_a = []
    list_b = []
    for line in list:
        splits = line.split(" ")
        list_a.append(int(splits[0].strip()))
        list_b.append(int(splits[len(splits)-1].strip()))
    return [list_a, list_b]

def similiarity_score(lists) -> int:
    sum = 0
    for line in range(len(lists[0])):
        val = lists[0][line]
        sum += val * lists[1].count(val)
    return sum
            
def main():
    rawList = list_from_file('./input.txt')
    splitLists = split_list(rawList)
    sum = similiarity_score(splitLists)
    print(sum)

main()