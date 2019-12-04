import sys

def retrieve_op_codes(list_op_codes):
    i = 0
    while i < len(list_op_codes):
        i += 1
        l = list_op_codes[i]
        if l == 1:
            list_op_codes[list_op_codes[i + 3]] = list_op_codes[list_op_codes[i + 1]] + list_op_codes[list_op_codes[i + 2]]
            i += 3
        elif l == 2:
            list_op_codes[list_op_codes[i + 3]] = list_op_codes[list_op_codes[i + 1]] * list_op_codes[list_op_codes[i + 2]]
            i += 3
        elif l == 99:
           return list_op_codes

    return list_op_codes


def main():
    l1 = 0
    l2 = 0
    initial_list_op_codes = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,2,9,19,23,2,13,23,27,1,6,27,31,2,6,31,35,2,13,35,39,1,39,10,43,2,43,13,47,1,9,47,51,1,51,13,55,1,55,13,59,2,59,13,63,1,63,6,67,2,6,67,71,1,5,71,75,2,6,75,79,1,5,79,83,2,83,6,87,1,5,87,91,1,6,91,95,2,95,6,99,1,5,99,103,1,6,103,107,1,107,2,111,1,111,5,0,99,2,14,0,0]
    i = 0
    for j in range(len(initial_list_op_codes)):
        l1 = j
        for k in range(len(initial_list_op_codes)):
            l2 = k
            list_op_codes = initial_list_op_codes[:]
            list_op_codes[1], list_op_codes[2] = l1, l2
            print(l1, l2)
            rs = retrieve_op_codes(list_op_codes)

            if rs[0] == 19690720:
                print('L1:', l1)
                print('L2:', l2)
                print('RESULT:', 100 * l1 + l2)
                sys.exit()


if __name__ == "__main__":
    main()
