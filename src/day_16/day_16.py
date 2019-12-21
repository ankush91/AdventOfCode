import math
import sys


def read_input():
    with open('input', 'r') as file:
        input_str = file.read().strip('\n')
        list_digits = [int(c) for c in input_str]   

    return list_digits


def part_1(x_input, x_pattern, num_phases=1):
    # for each phase, take remainder after absolute value
    p = 0
    ## PART-1 soln
    while p < num_phases:
        output_list = []
        # row-wise
        for i in range(len(x_input)):
            total_row_sum, ff_idx = 0, 0
            # start from -1 to allow left shifted sequence
            # mutliply pattern idx to num. rows i/p values
            
            for j in range(-1, len(x_input), i + 1):
                ff_idx = ff_idx % len(x_pattern)
                ff_multiplier = x_pattern[ff_idx]
                ff_idx += 1

                # slice and multiply pattern value till i + 1 values
                total_row_sum += sum([ff_multiplier * xi for xi in x_input[j: j + i + 1]])
            output_list.append(abs(total_row_sum) % 10)

        p += 1
        print(p)
        x_input = output_list

    return output_list


def part_2(input_digits, scalar):
    p = 0
    while p < 100:
        fn_input = 0
        last_loc = len(input_digits) - 1
        for digit in input_digits[::-1]:
            fn_input += (digit * scalar)
            input_digits[last_loc] = abs(fn_input) % 10
            last_loc -= 1
        p += 1
        print(p)

    return input_digits


def main():
    list_digits = read_input()
    # pattern list
    x_pattern = [0, 1, 0, -1]
    
    ## PART-1
    output_list = part_1(list_digits, x_pattern, num_phases=100)
    print('part-1', output_list[:8])

    ## PART-2 ANALYSIS
    # PART-2 currently is implemented using special knowledge of the starting 7 digit input loc
    # If the intended offset of 7 digits >= len(list_digits) / 2 then due to the triangluar matrix,
    # fn(input_i) = fn(input_i + 1) + (input_i) * pattern[1]
    # digit(input_i) = abs(fn(input_i)) % 10
    # **The generalized implementation is currently pending**
    
    part_2_input = list_digits[:] * 10000
    output_indx = int(''.join([str(xi) for xi in part_2_input[:7]]))
    mid_loc = math.floor(len(part_2_input) / 2)

    # solving using specialized soln
    if output_indx > mid_loc:
        output_digits = part_2(part_2_input[output_indx:], x_pattern[1])
        print('part-2', output_digits[:8])
    else:
        print('Need general solution; currently not supported')
        sys.exit(1)


if __name__ == "__main__":
    main()
