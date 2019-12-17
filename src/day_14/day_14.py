import math
import re


def read_input():
    var_split_re = r'[,\s=>]+' 
    with open('input', 'r') as f_open:
        rows = f_open.readlines()

    # quantity of ORE produced is atleast 1
    input_to_output_compounds = {'ORE': [1]}
    for r in rows:
        const_var_list = re.split(var_split_re, r.strip('\n'))
        # inverse index i/p expr. to o/p expression with quantities supplied by i/p
        output_compound, min_output_quantity = const_var_list[-1], const_var_list[-2]

        # initialize with minimum o/p quantity produced else change o/p seen in i/p
        if output_compound not in input_to_output_compounds:
            input_to_output_compounds[output_compound] = [int(min_output_quantity)]
        else:
            input_to_output_compounds[output_compound][0] = int(min_output_quantity)
        
        # add output compound and supplied input quantity to input index
        i = 0
        while i < (len(const_var_list) - 2):
            input_quantity = int(const_var_list[i])
            input_compound = const_var_list[i + 1]

            tup_input = (input_quantity, output_compound,)
            # minimum of 1 assumed if no o/p exprsession for input seen yet
            if input_compound not in input_to_output_compounds:
                input_to_output_compounds[input_compound] = [1]

            input_to_output_compounds[input_compound].append(tup_input)
            i += 2

    return input_to_output_compounds


def recurse_required_quantities(input_to_output_compounds, input_chemical):
    # base-case minimum fuel produced
    if input_chemical == 'FUEL':
        return input_to_output_compounds[input_chemical][0]

    sum_inputs = 0
    for input_quantity, output_compound in input_to_output_compounds[input_chemical][1:]:
        # minimum output produced due to input
        min_output_quantity = input_to_output_compounds[output_compound][0]

        # collect all required output needed; 
        # round by minimum output quantity produceable;
        # multiply by quantity of input used to produce output
        total_required_output = math.ceil(
                                    recurse_required_quantities(
                                        input_to_output_compounds, output_compound
                                    ) / min_output_quantity
                                )

        sum_input_due_to_output  = (input_quantity * total_required_output)

        sum_inputs += sum_input_due_to_output
        # DEBUG STATEMENTS FOR RECURSIVE FLOW
        # print('input quant', input_quantity, 'output quant', min_output_quantity)
        # print('amount of', input_chemical, 'due to', output_compound, sum_input_due_to_output)

    # print('total of', input_chemical, 'consumed:', sum_inputs)

    return sum_inputs

# def recurse_new_quantities(input_to_output_compound, input_chemical):


def main():
    input_to_output_compounds = read_input()
    print('part-1', recurse_required_quantities(input_to_output_compounds, 'ORE'))

    ## PART-2
    total_ores_supply = 1000000000000


if __name__ == "__main__":
    main()
