import csv


def read_input():
    list_rows = []
    with open('input.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            list_rows.append(int(row[0]))
        print('Processed', line_count, 'lines.')

    return list_rows


def fuel_required(fuel_mass):
    list_fuel_required = []
    # initial fuel
    fuel_mass = int(fuel_mass / 3) - 2

    while fuel_mass > 0:
        list_fuel_required.append(fuel_mass)
        fuel_mass = int(fuel_mass / 3) - 2

    return sum(list_fuel_required)


def main():
    list_masses = read_input()
    total_fuel = sum([fuel_required(l) for l in list_masses])
    print(total_fuel)


if __name__ == "__main__":
    main()
