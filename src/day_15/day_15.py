import time
import sys
import copy


STATUS_NAMES = ['WALL', 'EMPTY', 'OXYGEN_SYSTEM']

STATUS_ICONS = {'WALL': '#', 'EMPTY': '.','OXYGEN_SYSTEM': 'O'}


class INTCodeInterpreter():
    def __init__(self, list_op_codes, input_values, fn=None):
        self.list_op_codes = list_op_codes
        self.i = -1
        self.relative_base = 0
        self.is_hault = False
        self.input_values = input_values
        self.fn = fn

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
                # if func provided, exec func to retrieve input_value
                if self.fn:
                    self.input_values.append(self.fn())
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


def draw_display(xd, yd, min_x, min_y, max_x, max_y, xy_to_symbols):
    for y in range(min_y, max_y + 1):
        row_x_symbols = []
        for x in range(min_x, max_x + 1):
            if x == xd and y == yd:
                row_x_symbols.append('D')
            # valid symbol
            elif (x, y,) in xy_to_symbols:
                symbol_icon = STATUS_ICONS[xy_to_symbols[(x, y,)]]
                row_x_symbols.append(symbol_icon)
            # empty space
            else:
                row_x_symbols.append('_')
        print(''.join(row_x_symbols))
    print()


def BFS(list_op_codes, simulation_speed=0.01):
    int_code_runner = INTCodeInterpreter(list_op_codes, [])
    xy_to_symbol_names = {}
    limits = {'min_x': 0, 'min_y': 0, 'max_x': 0, 'max_y': 0}
    xd, yd = 0, 0

    fewest_steps = 0
    loc_oxygen_system = None
    loc_visited = set()
    queue_directions = [(xd, yd, int_code_runner, 0)]
    
    def evaluate_loc(x, y, input_value, int_code_runner,):
        int_code_runner.input_values.append(input_value)
        out_value = int_code_runner.retrieve_op_codes()

        # index of coordinates to symbols
        symbol_name_i = STATUS_NAMES[out_value]
        xy_to_symbol_names[(x, y,)] = symbol_name_i

        limits['min_x'] = min(limits['min_x'], x)
        limits['min_y'] = min(limits['min_y'], y)
        limits['max_x'] = max(limits['max_x'], x)
        limits['max_y'] = max(limits['max_y'], y)

        # consider wall as visited loc
        if out_value == 0:
            loc_visited.add((x, y,))
        elif out_value == 2:
            return int_code_runner, (x, y,)

        return int_code_runner, None

    def directions(x, y, int_code_runner, fewest_steps):
        dir_list = [(x, y - 1, 1,),  (x, y + 1, 2,), (x - 1, y, 3,), (x + 1, y, 4,),]
        fewest_steps += 1
        
        for xi, yi, input_i in dir_list:
            if ((xi, yi,) in loc_visited):
                continue

            # if location not visited then consider for evaluation
            int_code_runner_copy = copy.deepcopy(int_code_runner)
            dir_int_code_runner, loc_oxygen_system = evaluate_loc(xi, yi, input_i, int_code_runner_copy)
            
            # if not oxygen system continue evaluation
            if not loc_oxygen_system:
                queue_directions.append((xi, yi, dir_int_code_runner, fewest_steps,))
            else:
                return loc_oxygen_system

    # upper limit of i
    i = 0
    while not loc_oxygen_system:
        # FIFO accces to queue
        xd, yd, int_code_runner, fewest_steps = queue_directions.pop(0)

        # evaluate drone loc directions if not wall
        if (xd, yd,) not in loc_visited:
            loc_oxygen_system = directions(xd, yd, int_code_runner, fewest_steps)

        loc_visited.add((xd, yd,))

        # draw the segment display
        if simulation_speed:
            draw_display(xd, yd,
                        limits['min_x'], limits['min_y'],
                        limits['max_x'], limits['max_y'], xy_to_symbol_names)

            time.sleep(simulation_speed)

        i += 1

    print('location of oxygen system:', loc_oxygen_system)
    print('fewest steps:', fewest_steps + 1)
    print('end state of BFS WALK')

    # draw end state
    draw_display(xd, yd,
                 limits['min_x'], limits['min_y'],
                 limits['max_x'], limits['max_y'], xy_to_symbol_names)


def main():
    initial_list_op_codes = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1002,1034,1,1039,1001,1036,0,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,1001,1034,0,1039,102,1,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,101,0,1035,1040,102,1,1038,1043,1001,1037,0,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1001,1035,0,1040,102,1,1038,1043,1001,1037,0,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,9,1032,1006,1032,165,1008,1040,5,1032,1006,1032,165,1101,0,2,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,40,1044,1106,0,224,1101,0,0,1044,1106,0,224,1006,1044,247,102,1,1039,1034,101,0,1040,1035,101,0,1041,1036,1001,1043,0,1038,1001,1042,0,1037,4,1044,1106,0,0,26,29,83,66,1,36,14,44,33,12,3,15,20,56,9,35,51,55,6,20,13,71,15,23,94,38,45,15,47,30,89,39,11,55,5,9,47,29,41,36,78,12,4,65,48,66,36,94,76,30,63,41,32,1,73,1,35,65,87,46,18,90,11,44,30,73,87,8,38,46,17,78,51,34,19,53,37,26,20,24,46,64,17,6,26,41,10,62,14,88,23,94,13,55,5,45,10,39,83,99,32,34,72,30,58,33,71,47,21,38,97,38,46,41,18,39,37,8,86,55,35,4,92,19,21,53,61,6,55,69,16,85,62,26,63,17,80,33,10,53,91,2,37,94,37,93,7,97,18,55,54,36,17,62,89,12,92,32,69,4,46,47,19,89,25,12,51,91,9,1,71,35,56,39,98,48,7,49,24,95,15,45,2,1,93,82,19,7,11,70,30,64,28,27,58,4,39,30,94,72,33,43,90,98,26,32,70,1,81,25,35,47,17,31,92,15,73,13,27,72,65,30,67,2,22,89,77,30,47,12,58,26,79,22,37,74,41,3,42,30,39,67,24,18,62,98,19,59,95,25,6,67,42,35,85,51,48,7,63,17,67,53,45,13,25,43,1,54,4,65,55,20,73,32,70,1,33,39,93,88,19,35,56,21,13,53,73,31,21,44,73,31,13,69,30,42,26,51,25,90,16,49,9,93,50,28,60,24,18,61,23,11,98,19,45,77,12,61,31,3,66,56,4,77,24,59,87,31,38,65,67,7,9,23,71,9,59,35,55,83,22,12,94,17,67,87,96,63,8,29,32,34,15,55,39,60,41,74,39,81,47,51,25,26,57,28,18,60,84,20,16,66,42,14,25,16,94,2,22,74,85,19,63,32,9,19,11,91,44,34,21,1,56,12,87,8,52,18,56,7,90,5,86,81,24,98,21,9,80,59,68,10,80,53,18,75,50,9,14,43,26,29,57,86,39,41,93,3,69,55,16,84,15,22,84,30,72,19,13,15,19,80,97,79,32,68,77,82,30,19,4,71,45,67,14,95,17,54,80,88,25,13,80,41,37,96,15,28,26,33,73,32,45,79,21,52,23,98,82,21,16,13,64,32,39,93,17,33,95,61,36,12,21,3,84,4,88,22,26,59,80,27,82,2,85,79,29,33,52,17,23,95,8,64,16,56,23,42,43,18,41,11,9,84,42,62,4,67,17,98,76,99,1,16,72,72,10,79,19,76,4,54,9,99,34,33,7,97,85,19,76,93,38,6,90,37,90,2,83,61,19,43,39,2,91,17,60,21,79,2,32,94,38,32,7,64,8,14,7,68,23,28,75,24,73,50,29,63,22,89,4,51,66,2,7,33,82,13,23,84,81,23,55,68,15,27,9,97,27,79,42,86,75,56,13,95,74,5,88,25,44,99,33,14,24,29,21,78,4,15,75,32,92,74,11,56,24,57,10,28,73,8,10,90,77,30,96,8,60,3,71,20,41,9,33,89,38,74,95,4,95,35,13,18,55,10,81,9,60,17,67,7,34,48,48,15,54,79,37,66,43,22,64,28,28,4,91,5,9,92,30,64,37,98,66,15,92,2,3,25,70,25,33,61,56,25,70,58,30,41,97,18,54,10,49,45,3,1,30,57,30,46,8,55,79,39,58,46,35,19,38,80,86,4,36,75,29,62,39,71,2,41,6,66,36,99,21,61,39,72,3,48,29,43,31,59,84,71,12,52,61,82,11,56,23,51,30,60,88,65,35,48,24,58,76,49,93,51,33,72,0,0,21,21,1,10,1,0,0,0,0,0,0]
    
    ## PART-1
    BFS(initial_list_op_codes[:], simulation_speed=0.01)


if __name__ == "__main__":
    main()
