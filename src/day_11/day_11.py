import sys


def U(x, y,):
    y -= 1

    return x, y


def D(x, y,):
    y += 1

    return x, y


def L(x, y):
    x -= 1

    return x, y


def R(x, y):
    x += 1

    return x, y


# list of colors
list_colors = ['B', 'W']

# can change directions from adjacent directions
list_direction_order = ['>', '^', '<', 'v']
dict_directions = {'^': U, 'v': D, '<': L, '>': R}


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
    initial_list_op_codes = [3,8,1005,8,325,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,29,1006,0,41,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,54,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,102,1,8,76,1,9,11,10,2,5,2,10,2,1107,19,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,110,2,1007,10,10,2,1103,13,10,1006,0,34,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,142,1006,0,32,1,101,0,10,2,9,5,10,1006,0,50,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,179,1,1005,11,10,2,1108,11,10,1006,0,10,1,1004,3,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1002,8,1,216,1,1002,12,10,2,1102,3,10,1,1007,4,10,2,101,7,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,253,2,104,3,10,1006,0,70,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,282,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,305,101,1,9,9,1007,9,962,10,1005,10,15,99,109,647,104,0,104,1,21102,838211572492,1,1,21102,342,1,0,1105,1,446,21102,825326674840,1,1,21101,0,353,0,1106,0,446,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,29086686211,1,21102,1,400,0,1106,0,446,21102,209420786919,1,1,21101,0,411,0,1105,1,446,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,838337298792,1,21101,434,0,0,1105,1,446,21101,988661154660,0,1,21102,1,445,0,1106,0,446,99,109,2,21201,-1,0,1,21101,40,0,2,21101,0,477,3,21101,0,467,0,1105,1,510,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,472,473,488,4,0,1001,472,1,472,108,4,472,10,1006,10,504,1101,0,0,472,109,-2,2106,0,0,0,109,4,1201,-1,0,509,1207,-3,0,10,1006,10,527,21102,0,1,-3,22102,1,-3,1,22102,1,-2,2,21101,0,1,3,21101,546,0,0,1105,1,551,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,574,2207,-4,-2,10,1006,10,574,21201,-4,0,-4,1105,1,642,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,1,593,0,1105,1,551,21202,1,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,612,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,634,21202,-1,1,1,21102,1,634,0,105,1,509,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]
    int_code_runner = INTCodeInterpreter(initial_list_op_codes[:])
    output_codes = []
    ## USE INPUT-VALUE 1 FOR PART-1
    direction = '^'
    color = 'B'
    op = [color, direction]
    i = 0
    paint_cells = {}
    x_rel, y_rel = 0, 0

    while not int_code_runner.is_hault:
        int_code_runner.input_values.append(2)
        output_code = int_code_runner.retrieve_op_codes()
        curr_op = op[i % 2]
        if curr_op == color:
            paint_cells[x_rel, y_rel] = list_colors[output_code]
        elif curr_op == direction:
            if output_code == 0:
                relative_direction = -1
            else:
                relative_direction = 1
            
            new_direction = list_direction_order[direction + relative_direction]
            x_rel, y_rel = dict_directions[new_direction]()

        i += 1
        
    print(output_codes)


    


if __name__ == "__main__":
    main()