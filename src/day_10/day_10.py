

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
    if x > 0 and y > 0:
        return 'I'

    if x < 0 and y > 0:
        return 'II'

    if x < 0 and y < 0:
        return 'III'

    if x > 0 and y < 0:
        return 'IV'


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
                    ratio = '180'
                elif x_diff < 0:
                    ratio = '-180'
            elif x_diff == 0:
                if y_diff > 0:
                    ratio = '360'
                elif y_diff < 0:
                    ratio = '-360'
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

    max_c = max(dict_c_to_asteriods.items(), key=lambda x: len(x[1]))
    print('part-1', len(max_c[1]))


def part_2(coordinate_list, target):
    dict_c_to_asteriods = dict()
    line_of_sight_coorddinates = set()
    prev_count_of_los = 0
    xi, yi = target[0], target[1]
    for xj, yj in coordinate_list:
        # same coordinate or vaporized
        if (xi == xj and yi == yj):
            continue
        
        # add unique ratio & dir. of x_diff/y_diff
        x_diff = xi - xj
        y_diff = yi - yj
        
        # store static values for right angles
        if y_diff == 0:
            if x_diff > 0:
                ratio = '180'
            elif x_diff < 0:
                ratio = '-180'
        elif x_diff == 0:
            if y_diff > 0:
                ratio = '360'
            elif y_diff < 0:
                ratio = '-360'
        else:
            # get line of sight distance and orientation
            quadrant = get_dir(x_diff, y_diff)
            ratio = x_diff / y_diff
            ratio = (ratio, quadrant)
        
        if (xi, yi,) in dict_c_to_asteriods:
            prev_count_of_los = len(dict_c_to_asteriods[(xi, yi,)])
            dict_c_to_asteriods[(xi, yi,)] = dict_c_to_asteriods[(xi, yi,)].union(
                set([ratio])                    
        )
            # if coordinate was added to current line of sight
            if prev_count_of_los < len(dict_c_to_asteriods[(xi, yi,)]):
                line_of_sight_coorddinates.add((xj, yj, ratio))
        else:
            dict_c_to_asteriods[(xi, yi,)] = set([ratio])

    # CUSTOM SORT LOS COODINATES; THEN WHILE ALL ASTEROIDS DONE


def main():
    ## PART-1
    coordinate_list, target = read_input_coordinates()
    part_1(coordinate_list)

    ## PART-2; contains marked 'X' asteroid
    part_2(coordinate_list, target)


if __name__ == "__main__":
    main()
