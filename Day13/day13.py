def read_machines(filename: str) -> list:
    a = []
    b = []
    goal = []
    
    with open(filename) as file:
        i = 0
        for line in file:
            cleanline = line.strip()
            if len(cleanline) == 0:
                i = 0
            else:
                if i == 0:
                    a.append((int(cleanline[11:14]), int(cleanline[17:20])))
                elif i == 1:
                    b.append((int(cleanline[11:14]), int(cleanline[17:20])))
                elif i == 2:
                    goal.append([int(val.split('=')[1]) + 10000000000000 for val in cleanline.split(': ')[1].split(', ')])    
                i+=1
    return a, b, goal

def main():
    total = 0
    a_list, b_list, t_list = read_machines(FILENAME)
    for i in range(len(a_list)):
        det = a_list[i][0] * b_list[i][1] - a_list[i][1] * b_list[i][0]
        det_a = t_list[i][0] * b_list[i][1] - t_list[i][1] * b_list[i][0]
        det_b = a_list[i][0] * t_list[i][1] - a_list[i][1] * t_list[i][0]

        a = det_a / det
        b = det_b / det

        if a % 1 == 0 and b % 1 == 0:
            total += 3*a+b
    print(total)

FILENAME = "./Day13/input.txt"
main()