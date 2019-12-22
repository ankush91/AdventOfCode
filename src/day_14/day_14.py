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


def recurse_required_quantities(input_to_output_compounds, input_chemical, fuel_required=1):
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
                                        input_to_output_compounds, output_compound, fuel_required
                                    ) / min_output_quantity
                                )

        # if required fuel quantity is more than base, then change input quantity needed
        if output_compound == 'FUEL' and fuel_required > 1:
            input_quantity *= fuel_required

        sum_input_due_to_output  = int(input_quantity * total_required_output)

        sum_inputs += sum_input_due_to_output
        # DEBUG STATEMENTS FOR RECURSIVE FLOW
        # print('input quant', input_quantity, 'output quant', min_output_quantity)
        # print('amount of', input_chemical, 'due to', output_compound, sum_input_due_to_output)

    # print('total of', input_chemical, 'consumed:', sum_inputs)

    return sum_inputs


def binary_search_fuel_required(low, high, target_ore_supply, input_to_output_compounds):
    # fuel required
    mid = math.ceil((low + high) / 2)

    # redefine minimum required fuel quantity
    input_to_output_compounds['FUEL'][0] = mid

    required_ore = recurse_required_quantities(input_to_output_compounds, 'ORE', mid)
    ## DEBUG STATEMENTS
    # print('fuel generated',  mid)
    # print('ore required', required_ore)
    # print('target ore', target_ore_supply)
    # print()

    # no more fuel can be generated using target ore supply
    if (mid + 1) >= high and required_ore <= target_ore_supply:
        return mid
    # more ore required than target supply; lesser fuel can be generated
    elif required_ore > target_ore_supply:
        return binary_search_fuel_required(low, mid - 1, target_ore_supply, input_to_output_compounds)
    # lesser ore required than supplied; more fuel can be generated
    elif required_ore < target_ore_supply:
        return binary_search_fuel_required(mid + 1, high, target_ore_supply, input_to_output_compounds)


def main():
    input_to_output_compounds = read_input()
    ore_for_1_fuel = recurse_required_quantities(input_to_output_compounds, 'ORE')
    print('part-1', ore_for_1_fuel)

    ## PART-2
    total_ores_supply = 1000000000000

    # low indicates 1 fuel is generated using target ore supply
    low_initial = 1
    
    # high indicates x units of fuel is generated for x units of ore
    # i.e. 1 unit of ore translates to 1 unit of fuel (only whole number units)
    high_initial = total_ores_supply

    print(binary_search_fuel_required(low_initial, high_initial, 
                                      total_ores_supply,
                                      dict(input_to_output_compounds)))


if __name__ == "__main__":
    main()
