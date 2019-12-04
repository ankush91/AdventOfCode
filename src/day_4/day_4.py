import csv


def valid_password(x):
    digits = [int(d) for d in str(x)]
    prev_d, cont_d_count = -1, 0
    valid_pwd = False

    for d in digits:
        # increasing/same digits
        if d < prev_d:
            return False
        # doubles
        elif d == prev_d:
            ## PART-2
            # keep track of largest span count
            cont_d_count += 1
        else:
            # at-least 1 double
            if cont_d_count == 2:
                valid_pwd = True
            cont_d_count = 1
    
        prev_d = d

    # terminal-case for doubles check
    if cont_d_count == 2:
        return True

    # Atleast 1 non-overlapping doubles
    return valid_pwd


def main():
    min_bound, max_bound = 134564, 585159
    pwd_count = 0
    for i in range(min_bound, max_bound + 1):
        if valid_password(i):
            pwd_count += 1

    print(pwd_count)


if __name__ == "__main__":
    main()
