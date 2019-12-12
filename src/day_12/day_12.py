import copy


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
    i = 0
    ## change to 1000 for PART-1; else repeat till equality achieved
    while True:
        i += 1
        all_moon_velocities = apply_gravity(all_moon_coordinates, all_moon_velocities,)
        all_moon_coordinates = apply_velocity(all_moon_coordinates, all_moon_velocities,)

        if ((all_moon_coordinates == all_moon_coordinates_initial) and 
            (all_moon_velocities == all_moon_velocities_initial)):
            print(all_moon_coordinates_initial)
            break

    potential_energies = [sum(abs(c) for c in m) for m in all_moon_coordinates]
    kinetic_energies = [sum(abs(c) for c in m) for m in all_moon_velocities]

    print('number of steps', i)
    print('potential-energies:', potential_energies)
    print('kinetic-energies:', kinetic_energies)
    total_energy = sum(potential_energies[i] * kinetic_energies[i] 
                       for i in range(len(potential_energies)))
    print('total-energy:', total_energy)


if __name__ == "__main__":
    main()
