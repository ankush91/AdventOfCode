import numpy as np


def read_input():
    with open('input', 'r') as file:
        input_str = file.read().strip('\n')
        list_digits = [int(c) for c in input_str]   

    return list_digits


def main():
    list_digits = read_input()
    # vectorize input
    X_input = np.array([list_digits])

    # pattern matrix
    x_pattern, pattern_list = [0, 1, 0, -1], []
    for i in range(1, len(list_digits) + 1):
        row = []
        j = 0
        while len(row) < (len(list_digits) + 1):
            row.extend([x_pattern[j]] * i)
            # phase 
            if len(row) >= (len(list_digits) + 1):
                row = row[:len(list_digits) + 1]
            j += 1
            j = j % len(x_pattern)
        pattern_list.append(row)

    # drop 1st pattern unit for phase transformations
    X_pattern = np.array(pattern_list)[:,1:]
    
    # for each phase, take remainder after absolute value
    p = 0
    ## PART-1 soln
    while p < 100:
        X_output = np.absolute(X_input.dot(X_pattern.T)) % 10
        # DEBUG
        # print(X_output)
        X_input = X_output
        p += 1

    print(X_output)


if __name__ == "__main__":
    main()
