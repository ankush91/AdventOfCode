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


def part_2():
    pass


def main():
    list_digits = read_input()
    # pattern list
    x_pattern = [0, 1, 0, -1]
    
    ## PART-1
    output_list = part_1(list_digits, x_pattern, num_phases=100)
    print('part-1', output_list)

    ## PART-2 ANALYSIS
    print(len(list_digits))
    print(len(list_digits) * 10000)
    print((len(list_digits) * 10000) / 2)

    print(part_1(list_digits[:] * 10000, x_pattern, num_phases=100))

    # retrieve index for 1st 7 digits
    # output_indx = int(''.join([str(xi) for xi in x_input[:7]]))
    # print(x_input[:7])
    # print(output_indx)
    # print(x_input[output_indx:(output_indx + 8)])


if __name__ == "__main__":
    main()
