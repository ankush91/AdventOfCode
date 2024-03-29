import sys


def retrieve_op_codes(list_op_codes, input_value):
    i = -1
    output_codes = []
    while i < len(list_op_codes):
        i += 1
        l_op = list_op_codes[i]
        parameter_types = []

        # single digit
        if l_op < 9:
            l_rem = l_op
        else:
            # last 2 digits
            l_rem = l_op % 100
            l_div = int(l_op / 100)
            if l_div > 0:
                parameter_types = [int(lp) for lp in str(l_div)]
                parameter_types.reverse()

        def _parse_3_parameters():
            # default position modes
            # write parameter
            li_3 = list_op_codes[i + 3]
            li_2 = list_op_codes[i + 2]
            li_1 = list_op_codes[i + 1]

            # parsed parameter types for immediate modes
            if len(parameter_types) > 0:
                li_1 = (i + 1) if parameter_types[0]==1 else list_op_codes[i + 1]
                if len(parameter_types) > 1:
                    li_2 = (i + 2) if parameter_types[1]==1 else list_op_codes[i + 2]

            return li_1, li_2, li_3

        def _parse_2_parameters():
            # default position modes
            # write parameter
            li_2 = list_op_codes[i + 2]
            li_1 = list_op_codes[i + 1]

            # parsed parameter types for immediate modes
            if len(parameter_types) > 0:
                li_1 = (i + 1) if parameter_types[0]==1 else list_op_codes[i + 1]
                if len(parameter_types) > 1:
                    li_2 = (i + 2) if parameter_types[1]==1 else list_op_codes[i + 2]

            return li_1, li_2

        if l_rem == 1:
            li_1, li_2, li_3 = _parse_3_parameters()
            list_op_codes[li_3] = list_op_codes[li_1] + list_op_codes[li_2]
            i += 3
        elif l_rem == 2:
            li_1, li_2, li_3 = _parse_3_parameters()
            list_op_codes[li_3] = list_op_codes[li_1] * list_op_codes[li_2]
            i += 3
        # o/p at register address i/p
        elif l_rem == 3:
            # write parameter
            list_op_codes[list_op_codes[i + 1]] = input_value
            i += 1
        elif l_rem == 4:
            # read only parameter
            if parameter_types and parameter_types[0]:
                li = i + 1
            else:
                li = list_op_codes[i + 1]
            output_codes.append(list_op_codes[li])
            i += 1
        ## PART-2 POTENTIAL SOLUTIONS
        elif l_rem == 5:
            # jmp parameter
            li_1, li_2 = _parse_2_parameters()
            # set instruction ptr to li_2 if not 0
            if list_op_codes[li_1] != 0:
                i = list_op_codes[li_2] - 1 
            else:
                i += 2
        elif l_rem == 6:
            # jmp parameter
            li_1, li_2 = _parse_2_parameters()
            # set instruction ptr to li_2 if 0
            if list_op_codes[li_1] == 0:
                i = list_op_codes[li_2] - 1
            else:
                i += 2
        elif l_rem == 7:
            li_1, li_2, li_3 = _parse_3_parameters()
            # set to 1 if parameter_value_1 < parameter_value_2
            if list_op_codes[li_1] < list_op_codes[li_2]:
                list_op_codes[li_3] =  1
            # else set to 0
            else:
                list_op_codes[li_3] = 0
            i += 3
        elif l_rem == 8:
            li_1, li_2, li_3 = _parse_3_parameters()
            # set to 1 if parameter values not equal
            if list_op_codes[li_1] == list_op_codes[li_2]:
                list_op_codes[li_3] =  1
            # else set to 0
            else:
                list_op_codes[li_3] = 0
            i += 3
        elif l_op == 99:
           return output_codes

    return output_codes


def main():
    initial_list_op_codes = [3,225,1,225,6,6,1100,1,238,225,104,0,1002,43,69,224,101,-483,224,224,4,224,1002,223,8,223,1001,224,5,224,1,224,223,223,1101,67,60,225,1102,5,59,225,1101,7,16,225,1102,49,72,225,101,93,39,224,101,-98,224,224,4,224,102,8,223,223,1001,224,6,224,1,224,223,223,1102,35,82,225,2,166,36,224,101,-4260,224,224,4,224,102,8,223,223,101,5,224,224,1,223,224,223,102,66,48,224,1001,224,-4752,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1001,73,20,224,1001,224,-55,224,4,224,102,8,223,223,101,7,224,224,1,223,224,223,1102,18,41,224,1001,224,-738,224,4,224,102,8,223,223,101,6,224,224,1,224,223,223,1101,68,71,225,1102,5,66,225,1101,27,5,225,1101,54,63,224,1001,224,-117,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1,170,174,224,101,-71,224,224,4,224,1002,223,8,223,1001,224,4,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1007,226,226,224,1002,223,2,223,1006,224,329,1001,223,1,223,1007,226,677,224,102,2,223,223,1006,224,344,1001,223,1,223,108,677,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,374,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,389,101,1,223,223,7,226,226,224,1002,223,2,223,1005,224,404,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,419,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,434,101,1,223,223,1008,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,7,226,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,108,677,226,224,102,2,223,223,1005,224,479,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,494,101,1,223,223,8,226,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,524,1001,223,1,223,1107,226,226,224,102,2,223,223,1005,224,539,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,554,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,569,1001,223,1,223,1108,226,677,224,1002,223,2,223,1005,224,584,1001,223,1,223,1107,226,677,224,1002,223,2,223,1005,224,599,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,614,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,629,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,644,101,1,223,223,107,677,677,224,1002,223,2,223,1005,224,659,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]
    output_codes = retrieve_op_codes(initial_list_op_codes, 5)
    print(output_codes)


if __name__ == "__main__":
    main()