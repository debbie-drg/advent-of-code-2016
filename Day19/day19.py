import sys


# The Josephus Problem
# https://www.youtube.com/watch?v=uCsD3ZGzMgE
def gift_taker(elfs: int) -> int:
    exponent = len(bin(elfs)[2:]) - 1
    remaining = elfs - 2**exponent
    return 2 * remaining + 1


# Obtained from analizing the sequence
def gift_taker_across(elfs: int) -> int:
    if elfs == 1:
        return elfs
    previous_3_power = 1
    while 3 * previous_3_power < elfs:
        previous_3_power *= 3
    if elfs <= 2 * previous_3_power:
        return elfs - previous_3_power
    next_3_power = 3 * previous_3_power
    return 2 * elfs - next_3_power


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    number_elfs = int(open(file_name).read().strip())
    print(f"In the initial arrangement, {gift_taker(number_elfs)} wins")
    print(f"With the new arrangement, it's, {gift_taker_across(number_elfs)} wins")
