import sys


class amplifier():
    def __init__(self, list_op_codes):
        self.list_op_codes = list_op_codes
        self.i = -1
        self.is_hault = False
        self.input_values = []

    def retrieve_op_codes(self):
        output_codes = []
        while self.i < len(self.list_op_codes):
            self.i += 1
            l_op = self.list_op_codes[self.i]
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
                li_3 = self.list_op_codes[self.i + 3]
                li_2 = self.list_op_codes[self.i + 2]
                li_1 = self.list_op_codes[self.i + 1]

                # parsed parameter types for immediate modes
                if len(parameter_types) > 0:
                    li_1 = (self.i + 1) if parameter_types[0]==1 else self.list_op_codes[self.i + 1]
                    if len(parameter_types) > 1:
                        li_2 = (self.i + 2) if parameter_types[1]==1 else self.list_op_codes[self.i + 2]

                return li_1, li_2, li_3

            def _parse_2_parameters():
                # default position modes
                # write parameter
                li_2 = self.list_op_codes[self.i + 2]
                li_1 = self.list_op_codes[self.i + 1]

                # parsed parameter types for immediate modes
                if len(parameter_types) > 0:
                    li_1 = (self.i + 1) if parameter_types[0]==1 else self.list_op_codes[self.i + 1]
                    if len(parameter_types) > 1:
                        li_2 = (self.i + 2) if parameter_types[1]==1 else self.list_op_codes[self.i + 2]

                return li_1, li_2

            if l_rem == 1:
                li_1, li_2, li_3 = _parse_3_parameters()
                self.list_op_codes[li_3] = self.list_op_codes[li_1] + self.list_op_codes[li_2]
                self.i += 3
            elif l_rem == 2:
                li_1, li_2, li_3 = _parse_3_parameters()
                self.list_op_codes[li_3] = self.list_op_codes[li_1] * self.list_op_codes[li_2]
                self.i += 3
            # o/p at register address i/p
            elif l_rem == 3:
                # FIFO of values
                input_value = self.input_values.pop(0)
                # write parameter
                self.list_op_codes[self.list_op_codes[self.i + 1]] = input_value
                self.i += 1
            elif l_rem == 4:
                # read only parameter
                if parameter_types and parameter_types[0]:
                    li = self.i + 1
                else:
                    li = self.list_op_codes[self.i + 1]
                output_codes.append(self.list_op_codes[li])
                self.i += 1
                return output_codes
            elif l_rem == 5:
                # jmp parameter
                li_1, li_2 = _parse_2_parameters()
                # set instruction ptr to li_2 if not 0
                if self.list_op_codes[li_1] != 0:
                    self.i = self.list_op_codes[li_2] - 1 
                else:
                    self.i += 2
            elif l_rem == 6:
                # jmp parameter
                li_1, li_2 = _parse_2_parameters()
                # set instruction ptr to li_2 if 0
                if self.list_op_codes[li_1] == 0:
                    self.i = self.list_op_codes[li_2] - 1
                else:
                    self.i += 2
            elif l_rem == 7:
                li_1, li_2, li_3 = _parse_3_parameters()
                # set to 1 if parameter_value_1 < parameter_value_2
                if self.list_op_codes[li_1] < self.list_op_codes[li_2]:
                    self.list_op_codes[li_3] =  1
                # else set to 0
                else:
                    self.list_op_codes[li_3] = 0
                self.i += 3
            elif l_rem == 8:
                li_1, li_2, li_3 = _parse_3_parameters()
                # set to 1 if parameter values not equal
                if self.list_op_codes[li_1] == self.list_op_codes[li_2]:
                    self.list_op_codes[li_3] =  1
                # else set to 0
                else:
                    self.list_op_codes[li_3] = 0
                self.i += 3
            elif l_op == 99:
                self.is_hault = True
                return output_codes

        return output_codes


def main():
    num_amplifiers = 5
    initial_list_op_codes = [3,8,1001,8,10,8,105,1,0,0,21,38,63,72,85,110,191,272,353,434,99999,3,9,102,4,9,9,101,2,9,9,102,3,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,1001,9,5,9,1002,9,5,9,101,3,9,9,4,9,99,3,9,1001,9,2,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,4,9,99,3,9,101,2,9,9,102,2,9,9,1001,9,2,9,1002,9,4,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99]

    max_out = -1
    ## PART 1 OF DAY 7
    for i in range(0, 5):
        for j in range(0, 5):
            if i == j:
                continue
            for k in range(0, 5):
                if i == k or j == k:
                    continue
                for l in range(0, 5):
                    if i == l or j == l or k == l:
                        continue
                    for m in range(0, 5):
                        if i == m or j == m or k == m or l == m:
                            continue
                        phase_setting_sequence = [i,j,k,l,m]
                        amplifier_objects = [amplifier(initial_list_op_codes[:]) for i in range(num_amplifiers)]
                        out = 0
                        # initialize with phase setting i/p sequence
                        for pi, amp_obj in enumerate(amplifier_objects):
                            amp_obj.input_values.append(phase_setting_sequence[pi])

                        for ai, _ in enumerate(amplifier_objects):
                            amp_obj = amplifier_objects[ai]
                            # put o/p value for use if present from last amplifier; else use only phase setting
                            if out >= 0:
                                amp_obj.input_values.append(out)

                            # use corr. obj and phase sequence + o/p
                            output_codes = amp_obj.retrieve_op_codes()

                            # set o/p value for next amplifier if present; else use placeholder value
                            if not output_codes:
                                out = -1
                            else:
                                out = output_codes[0]
                        max_out = max(max_out, out)
    print('part-1', max_out)

    ## PART 2 OF DAY 7
    max_out_2 = -1
    for i in range(5, 10):
        for j in range(5, 10):
            if i == j:
                continue
            for k in range(5, 10):
                if i == k or j == k:
                    continue
                for l in range(5, 10):
                    if i == l or j == l or k == l:
                        continue
                    for m in range(5, 10):
                        if i == m or j == m or k == m or l == m:
                            continue
                        phase_setting_sequence = [i,j,k,l,m]
                        # initialize copies of programs on amp. objects
                        amplifier_objects = [amplifier(initial_list_op_codes[:]) for i in range(num_amplifiers)]
                        # initialize with phase setting i/p sequence
                        for pi, amp_obj in enumerate(amplifier_objects):
                            amp_obj.input_values.append(phase_setting_sequence[pi])

                        out = 0
                        iter = 0
                        while not all(ao.is_hault for ao in amplifier_objects):
                            ai = iter % 5
                            
                            # use corr. obj and phase setting
                            amp_obj = amplifier_objects[ai]

                            # put o/p value for use if present from last amplifier; else use only phase setting
                            if out >= 0:
                                amp_obj.input_values.append(out)

                            # use corr. obj and phase sequence + o/p
                            output_codes = amp_obj.retrieve_op_codes()

                            # set o/p value for next amplifier if present; else use placeholder value
                            if not output_codes:
                                out = -1
                            else:
                                out = output_codes[0]
                            
                            if pi == 4 and not amp_obj.is_hault:
                                max_out_2 = max(max_out_2, out)

                            iter += 1

    print('part-2:', max_out_2)


if __name__ == "__main__":
    main()