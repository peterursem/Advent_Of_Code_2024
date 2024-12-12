def list_from_file(fileName: str) -> list: 
    with open(fileName) as file:
        return file.readlines()

def measurements_from_text(lines: list) -> list:
    return [[int(val.strip()) for val in line.split(" ")] for line in lines]

def deltas_from_values(measurements: list) -> list:
    return [measurements[index-1]-measurements[index] for index in range(1, len(measurements))]
            
def signs_match(deltas: list) -> int:
    infraction_totals = []
    for expected in (True, False):
        infraction_count = 0
        for value in deltas:
            if (value > 0) != expected:
                infraction_count += 1
        infraction_totals.append(infraction_count)
    return min(infraction_totals)

def acceptable_change(deltas: list) -> int:
    infraction_count = 0
    for value in deltas:
        if abs(value) < 1 or abs(value) > 3:
            infraction_count += 1
    return infraction_count

def is_safe(measurements: list) -> bool:
    infraction_test_totals = []
    for ignore in range(len(measurements)):
        test_measurements = [measurements[index] for index in range(len(measurements)) if index != ignore]
        test_deltas = deltas_from_values(test_measurements)
        
        infraction_test_totals.append(signs_match(test_deltas) + acceptable_change(test_deltas))

    return min(infraction_test_totals) == 0

def main():
    text_list = list_from_file("./Day2/input.txt")
    measurements = measurements_from_text(text_list)

    safecount = 0
    for measurement_set in measurements:
        if is_safe(measurement_set):
            safecount += 1

    print(f'{safecount} Safe reports found out of {len(measurements)}. {100*safecount/len(measurements)}%')

main()