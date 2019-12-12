import copy
from math import gcd


def read_input():
    with open('input', 'r') as f_open:
        rows = f_open.readlines()
    
    all_moon_coodinates, all_moon_velocities = [], []
    for r in rows:
        x = 0
        r = r.strip('\n')
        print(r)
        moon_coodinates, moon_velocities = [], []
        for i, p in enumerate(r):
            if (p == 'x') or (p == 'y') or (p == 'z'):
                # negative number
                if r[i + 2] == '-':
                    # parse numbers
                    j = i + 3
                else:
                    j = i + 2
                while r[j] != ',' and r[j] != '>':
                    j += 1

                moon_coodinates.append(int(''.join(r[i+2:j])))
                moon_velocities.append(0)
        
        all_moon_coodinates.append(moon_coodinates), all_moon_velocities.append(moon_velocities)

    return all_moon_coodinates, all_moon_velocities


def apply_gravity(all_moon_coordinates, all_moon_velocities):
    for i in range(len(all_moon_velocities) - 1):
        for j in range(i + 1, len(all_moon_velocities)):
            # compare coordinates
            pci = all_moon_coordinates[i]
            pcj = all_moon_coordinates[j]
            
            for k in range(len(pci)):
                vi, vj = pci[k], pcj[k]

                if vi == vj:
                    continue
                elif vi < vj:
                    all_moon_velocities[i][k] += 1
                    all_moon_velocities[j][k] -= 1
                else:
                    all_moon_velocities[i][k] -= 1
                    all_moon_velocities[j][k] += 1

    return all_moon_velocities


def apply_velocity(all_moon_positions, all_moon_velocities):
    for i in range(len(all_moon_positions)):
        pc = all_moon_positions[i]
        vc = all_moon_velocities[i]

        for j in range(len(pc)):
            pc[j] += vc[j]

    return all_moon_positions


def main():
    all_moon_coordinates_initial, all_moon_velocities_initial = read_input()
    all_moon_coordinates = copy.deepcopy(all_moon_coordinates_initial)
    all_moon_velocities = copy.deepcopy(all_moon_velocities_initial)
    ## change to 1000 for PART-1 and remove outer-loop with break cases;
    ##  else repeat till equality of independent axis achieved achieved

    simulate_axis_cycles = []
    # try to achieve repetition between independent axes
    for j in range(len(all_moon_coordinates[0])):
        i = 0
        set_sum_cols = set()
        prev_len_sum_cols = 0
        while True:
            all_moon_coordinates_tup = tuple([a[j] for a in all_moon_coordinates],)
            all_moon_velocities_tup = tuple([a[j] for a in all_moon_velocities],)
            set_sum_cols.add((all_moon_coordinates_tup, all_moon_velocities_tup))
            if len(set_sum_cols) == prev_len_sum_cols:
                break
            
            i += 1
            all_moon_velocities = apply_gravity(all_moon_coordinates, all_moon_velocities,)
            all_moon_coordinates = apply_velocity(all_moon_coordinates, all_moon_velocities,)

            if i % 100000 == 0:
                print(i)
            prev_len_sum_cols = len(set_sum_cols)

        simulate_axis_cycles.append(i)
        
    # potential_energies = [sum(abs(c) for c in m) for m in all_moon_coordinates]
    # kinetic_energies = [sum(abs(c) for c in m) for m in all_moon_velocities]
    # total_energy = sum(potential_energies[i] * kinetic_energies[i] 
    #                   for i in range(len(potential_energies)))  

    # print('number of steps', i)
    # print('potential-energies:', potential_energies)
    # print('kinetic-energies:', kinetic_energies)
    # print('total-energy:', total_energy)
    print(simulate_axis_cycles)

    # LCM of independent cycles
    lcm = simulate_axis_cycles[0]
    for ax_reps in simulate_axis_cycles[1:]:
        lcm = int(lcm * ax_reps/gcd(lcm, int(ax_reps)))
    print('LCM:', lcm)   


if __name__ == "__main__":
    main()
