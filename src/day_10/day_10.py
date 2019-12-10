

def read_input_coordinates():
    with open('input', 'r') as f_open:
        rows = f_open.readlines()
    
    asteroid_coodinates = []
    target = None
    x, y = 0, 0
    for r in rows:
        x = 0
        r = r.strip('\n')
        print(r)
        for xy in r:
            if xy != '.':
                asteroid_coodinates.append((x, y,))
            if xy == 'X':
                target = (x, y,)
            x += 1
        y += 1

    return asteroid_coodinates, target


def get_dir(x, y):
    if x < 0 and y > 0:
        return 1.5

    if x > 0 and y > 0:
        return 4.5

    if x < 0 and y < 0:
        return 2.5

    if x > 0 and y < 0:
        return 3.5


def part_1(coordinate_list):
    dict_c_to_asteriods = dict()
    for xi, yi in coordinate_list:
        for xj, yj in coordinate_list:
            if xi == xj and yi == yj:
                continue
            
            # add unique ratio & dir. of x_diff/y_diff
            x_diff = xi - xj
            y_diff = yi - yj
            
            # store static values for right angles
            if y_diff == 0:
                if x_diff > 0:
                    ratio = (0, 4)
                elif x_diff < 0:
                    ratio =  (0, 2)
            elif x_diff == 0:
                if y_diff > 0:
                    ratio =  (0, 1)
                elif y_diff < 0:
                    ratio = (0, 3)
            else:
                # get line of sight distance and orientation
                quadrant = get_dir(x_diff, y_diff)
                ratio = x_diff / y_diff
                ratio = (ratio, quadrant)
            
            if (xi, yi,) in dict_c_to_asteriods:
                dict_c_to_asteriods[(xi, yi,)] = dict_c_to_asteriods[(xi, yi,)].union(
                    set([ratio])                    
            )
            else:
                dict_c_to_asteriods[(xi, yi,)] = set([ratio])

    max_c, max_c_count = max(dict_c_to_asteriods.items(), key=lambda x: len(x[1]))
    print('part-1', len(max_c_count))

    return  max_c[0], max_c[1]


def part_2(coordinate_list, target):
    xi, yi = target[0], target[1]
    rc = 0
    print(target)
    vaporized_asteroids = []
    while len(coordinate_list) > 1:
        print('--RC--', rc)
        dict_c_to_asteriods = dict()
        line_of_sight_coorddinates = dict()

        # full 360 degree rotation
        for xj, yj in coordinate_list:
            # same coordinate
            if (xi == xj and yi == yj):
                continue
            
            # add unique ratio & dir. of x_diff/y_diff
            x_diff = xi - xj
            y_diff = yi - yj
            
            # store static values for right angles
            if y_diff == 0:
                if x_diff > 0:
                    ratio = (0, 4)
                elif x_diff < 0:
                    ratio =  (0, 2)
            elif x_diff == 0:
                if y_diff > 0:
                    ratio =  (0, 1)
                elif y_diff < 0:
                    ratio = (0, 3)
            else:
                # get line of sight distance and orientation
                quadrant = get_dir(x_diff, y_diff)
                ratio = x_diff / y_diff
                # clockwise in reverse order for appropriate sort
                ratio = -1 * ratio 
                ratio = (ratio, quadrant)

            if (xi, yi,) in dict_c_to_asteriods:
                dict_c_to_asteriods[(xi, yi,)] = dict_c_to_asteriods[(xi, yi,)].union(
                    set([ratio])                    
            )
                # if coordinate angle was added to current line of sight
                if len(line_of_sight_coorddinates.keys()) < len(dict_c_to_asteriods[(xi, yi,)]):
                    line_of_sight_coorddinates[ratio] = (xj, yj, x_diff, y_diff,)
                else:
                    x_diff_prev = line_of_sight_coorddinates[ratio][2]
                    y_diff_prev = line_of_sight_coorddinates[ratio][3]
                    # add contending coordinate as nearest to target at angle
                    if (abs(x_diff) < abs(x_diff_prev)) or (abs(y_diff) < abs(y_diff_prev)):
                        line_of_sight_coorddinates[ratio] = (xj, yj, x_diff, y_diff,)

            else:
                line_of_sight_coorddinates[ratio] = (xj, yj, x_diff, y_diff,)
                dict_c_to_asteriods[(xi, yi,)] = set([ratio])

        curr_rotation_vaporized_asteroids = list(line_of_sight_coorddinates.items())
        # sort by nearest clockwise angles and nearest line of sight (abs. value)
        curr_rotation_vaporized_asteroids.sort(key=lambda x: (x[0][1], x[0][0], abs(x[1][2]), abs(x[1][3])))
        vaporized_asteroids.extend(curr_rotation_vaporized_asteroids)

        rc += sum(1 for i in range(len(curr_rotation_vaporized_asteroids)))
        
        # remove current rotation vaporized asteroid coordinates from coodrinates list
        for vc in curr_rotation_vaporized_asteroids:
            coordinate_list.remove((vc[1][0], vc[1][1],))

    print(vaporized_asteroids[199][1][0] * 100 + vaporized_asteroids[199][1][1])


def main():
    ## PART-1
    coordinate_list, target = read_input_coordinates()
    x, y = part_1(coordinate_list)

    if not target:
        target = (x, y,)
    ## PART-2; contains marked 'X' asteroid
    part_2(coordinate_list, target)


if __name__ == "__main__":
    main()
