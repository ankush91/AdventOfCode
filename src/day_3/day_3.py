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
    list_wire_coordinates = []
    # store coordinates by tracing wires
    for w in list_wire_directions:
        coordinates = [(0, 0,)]
        for dv in w:
            direction, v = dv[0], (int(dv[1:]) + 1)
            x_prev, y_prev = coordinates[-1]
            if direction == 'U':
                coordinates.extend([(x_prev, y_prev + vi,) for vi in range(1, v)])
            elif direction == 'D':
                coordinates.extend([(x_prev, y_prev - vi,) for vi in range(1, v)])
            elif direction == 'R':
                coordinates.extend([(x_prev + vi, y_prev,) for vi in range(1, v)])
            elif direction == 'L':
                coordinates.extend([(x_prev - vi, y_prev,) for vi in range(1, v)])

        list_wire_coordinates.append(coordinates)

    # PART 1
    # set_w1, set_w2 = set(list_wire_coordinates[0]), set(list_wire_coordinates[1])
    # sort by manhattan distances OR sort by sum(i)
    # md_tup = sorted(list(set_w1.intersection(set_w2)), key=lambda x: (abs(x[0]) + abs(x[1])))[1]
    # print(md_tup[0] + md_tup[1])

    # PART 2
    min_len = None
    set_w1, set_w2 = set(list_wire_coordinates[0]), set(list_wire_coordinates[1])
    intersection_tups = list(set_w1.intersection(set_w2))
    for wc in intersection_tups:
        # find location of intersection coordinates
        i = list_wire_coordinates[0].index(wc)
        j = list_wire_coordinates[1].index(wc)
        new_len = (i + j)
        if new_len == 0:
            continue
        else:
            if not min_len:
                min_len = new_len
            else:
                min_len = min(min_len, new_len)

    print(min_len)


if __name__ == "__main__":
    main()
