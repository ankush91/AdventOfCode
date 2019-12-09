import sys


class INTCodeInterpreter():
    def __init__(self, list_op_codes):
        self.list_op_codes = list_op_codes
        self.i = -1
        self.relative_base = 0
        self.is_hault = False
        self.input_values = []

    def determine_mode(self, pi, p_value):
        if p_value == 0:
            return self.list_op_codes[pi]
        
        if p_value == 1:
            return pi

        if p_value == 2:
            return self.list_op_codes[pi] + self.relative_base
    
    def dynamic_memory_resize(self, max_i):
        if max_i < len(self.list_op_codes):
            return

        increment = max_i - len(self.list_op_codes) + 1
        self.list_op_codes = self.list_op_codes + ([0] * increment)

    def retrieve_op_codes(self):
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
                li_3 = self.list_op_codes[self.i + 3]
                li_2 = self.list_op_codes[self.i + 2]
                li_1 = self.list_op_codes[self.i + 1]

                # parsed parameter types for immediate modes
                if len(parameter_types) > 0:
                    li_1 = self.determine_mode(self.i + 1, parameter_types[0])
                    if len(parameter_types) > 1:
                        li_2 = self.determine_mode(self.i + 2, parameter_types[1])
                        if len(parameter_types) > 2:
                            li_3 = self.determine_mode(self.i + 3, parameter_types[2])

                max_li = max(li_1, li_2, li_3)
                self.dynamic_memory_resize(max_li)

                return li_1, li_2, li_3

            def _parse_2_parameters():
                # default position modes
                # write parameter
                li_2 = self.list_op_codes[self.i + 2]
                li_1 = self.list_op_codes[self.i + 1]

                # parsed parameter types for immediate modes
                if len(parameter_types) > 0:
                    li_1 = self.determine_mode(self.i + 1, parameter_types[0])
                    if len(parameter_types) > 1:
                        li_2 = self.determine_mode(self.i + 2, parameter_types[1])

                max_li = max(li_1, li_2,)
                self.dynamic_memory_resize(max_li)

                return li_1, li_2

            def _parse_1_parameter():
                # default position modes
                # write parameter
                li_1 = self.list_op_codes[self.i + 1]

                # parsed parameter types for immediate modes
                if len(parameter_types) > 0:
                    li_1 = self.determine_mode(self.i + 1, parameter_types[0])

                self.dynamic_memory_resize(li_1)

                return li_1

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
                li = _parse_1_parameter()
                self.list_op_codes[li] = input_value
                self.i += 1
            elif l_rem == 4:
                # read only parameter
                li = _parse_1_parameter()
                output_code = self.list_op_codes[li]
                self.i += 1
                return output_code
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
            # adjust relative base by value of only parameter
            elif l_rem == 9:
                li = _parse_1_parameter()
                self.relative_base = self.relative_base + self.list_op_codes[li]
                self.i += 1
            elif l_op == 99:
                self.is_hault = True
                return


def main():
    initial_list_op_codes = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,3,0,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,1,37,1000,1101,856,0,1029,1101,286,0,1025,1101,39,0,1004,1101,861,0,1028,1101,845,0,1026,1102,28,1,1002,1102,1,0,1020,1101,0,892,1023,1101,0,291,1024,1101,35,0,1018,1101,0,27,1006,1102,1,26,1011,1101,33,0,1019,1102,31,1,1014,1102,1,36,1010,1102,23,1,1007,1101,0,32,1016,1101,29,0,1008,1101,20,0,1001,1102,1,25,1015,1101,38,0,1017,1101,0,24,1012,1102,1,22,1005,1101,1,0,1021,1101,0,21,1003,1102,1,838,1027,1102,1,30,1013,1101,895,0,1022,1101,0,34,1009,109,7,1208,0,22,63,1005,63,201,1001,64,1,64,1105,1,203,4,187,1002,64,2,64,109,-6,2102,1,5,63,1008,63,24,63,1005,63,223,1105,1,229,4,209,1001,64,1,64,1002,64,2,64,109,17,21102,40,1,-6,1008,1012,40,63,1005,63,255,4,235,1001,64,1,64,1106,0,255,1002,64,2,64,109,-15,21108,41,41,9,1005,1012,277,4,261,1001,64,1,64,1106,0,277,1002,64,2,64,109,11,2105,1,10,4,283,1105,1,295,1001,64,1,64,1002,64,2,64,109,-9,21101,42,0,8,1008,1013,44,63,1005,63,315,1105,1,321,4,301,1001,64,1,64,1002,64,2,64,109,13,1206,3,337,1001,64,1,64,1106,0,339,4,327,1002,64,2,64,109,-10,1208,0,29,63,1005,63,361,4,345,1001,64,1,64,1106,0,361,1002,64,2,64,109,2,2108,27,-4,63,1005,63,383,4,367,1001,64,1,64,1105,1,383,1002,64,2,64,109,-4,1207,2,30,63,1005,63,405,4,389,1001,64,1,64,1105,1,405,1002,64,2,64,109,22,1205,-8,417,1106,0,423,4,411,1001,64,1,64,1002,64,2,64,109,-27,2108,19,0,63,1005,63,443,1001,64,1,64,1106,0,445,4,429,1002,64,2,64,109,13,21108,43,45,-1,1005,1013,461,1106,0,467,4,451,1001,64,1,64,1002,64,2,64,109,1,21107,44,45,4,1005,1019,485,4,473,1105,1,489,1001,64,1,64,1002,64,2,64,109,-8,2102,1,-7,63,1008,63,37,63,1005,63,515,4,495,1001,64,1,64,1106,0,515,1002,64,2,64,109,1,2107,38,-4,63,1005,63,533,4,521,1105,1,537,1001,64,1,64,1002,64,2,64,109,4,21107,45,44,1,1005,1013,553,1106,0,559,4,543,1001,64,1,64,1002,64,2,64,109,-7,2107,21,-4,63,1005,63,575,1106,0,581,4,565,1001,64,1,64,1002,64,2,64,109,9,1205,7,599,4,587,1001,64,1,64,1105,1,599,1002,64,2,64,109,-11,2101,0,-3,63,1008,63,40,63,1005,63,619,1105,1,625,4,605,1001,64,1,64,1002,64,2,64,109,1,2101,0,-2,63,1008,63,28,63,1005,63,651,4,631,1001,64,1,64,1106,0,651,1002,64,2,64,109,1,21102,46,1,7,1008,1012,44,63,1005,63,671,1106,0,677,4,657,1001,64,1,64,1002,64,2,64,109,4,1201,-7,0,63,1008,63,28,63,1005,63,699,4,683,1105,1,703,1001,64,1,64,1002,64,2,64,109,-6,1207,-3,36,63,1005,63,719,1105,1,725,4,709,1001,64,1,64,1002,64,2,64,109,-4,1201,6,0,63,1008,63,23,63,1005,63,745,1106,0,751,4,731,1001,64,1,64,1002,64,2,64,109,8,1202,-6,1,63,1008,63,20,63,1005,63,777,4,757,1001,64,1,64,1105,1,777,1002,64,2,64,109,5,1202,-5,1,63,1008,63,25,63,1005,63,801,1001,64,1,64,1105,1,803,4,783,1002,64,2,64,109,8,21101,47,0,-6,1008,1014,47,63,1005,63,829,4,809,1001,64,1,64,1106,0,829,1002,64,2,64,109,1,2106,0,6,1001,64,1,64,1106,0,847,4,835,1002,64,2,64,109,11,2106,0,-4,4,853,1105,1,865,1001,64,1,64,1002,64,2,64,109,-15,1206,3,883,4,871,1001,64,1,64,1106,0,883,1002,64,2,64,109,14,2105,1,-8,1105,1,901,4,889,1001,64,1,64,4,64,99,21102,1,27,1,21102,1,915,0,1106,0,922,21201,1,57564,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,1,942,0,1105,1,922,22101,0,1,-1,21201,-2,-3,1,21101,957,0,0,1105,1,922,22201,1,-1,-2,1106,0,968,21202,-2,1,-2,109,-3,2106,0,0]
    int_code_runner = INTCodeInterpreter(initial_list_op_codes[:])
    output_codes = []
    ## USE INPUT-VALUE 1 FOR PART-1
    while not int_code_runner.is_hault:
        int_code_runner.input_values.append(2)
        output_code = int_code_runner.retrieve_op_codes()
        if output_code:
            output_codes.append(output_code)
        
    print(output_codes)


if __name__ == "__main__":
    main()