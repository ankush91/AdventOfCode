import csv


def read_input():
    list_wires = []
    with open('input.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            list_wires.append(row)

    return list_wires


def main():
    list_wire_directions = read_input()
    list_wire_md = []
    for w in list_wire_directions:
        coordinates = [(0, 0, 0,)]
        for direction in w:
            v = int(direction[1:])
            md = coordinates[-1][2]
            if direction.startswith('U'):
                coordinates.extend([(coordinates[-1][0], coordinates[-1][1] + vi, md + vi,) for vi in range(1, v)])
            elif direction.startswith('D'):
                coordinates.extend([(coordinates[-1][0], coordinates[-1][1] - vi, md - vi,) for vi in range(1, v)])
            elif direction.startswith('R'):
                coordinates.extend([(coordinates[-1][0] + vi, coordinates[-1][1], md + vi,) for vi in range(1, v)])
            elif direction.startswith('L'):
                coordinates.extend([(coordinates[-1][0] - vi, coordinates[-1][1], md - vi,) for vi in range(1, v)])

        coordinates.sort(key = lambda x: x[-1])
        list_wire_md.append(coordinates)

    w1, w2 = list_wire_md
    i, j = 0, 0
    wc1 = w1[0]
    for wc2 in w2[1:]:
        if wc1[-1] > wc2[-1]:
            j += 1
            wc2 = w2[j]
        elif wc1[-1] < wc2[-1]:
            i += 1
            wc1 = w1[i]
        else:
            print(wc1,)
            break


if __name__ == "__main__":
    main()
