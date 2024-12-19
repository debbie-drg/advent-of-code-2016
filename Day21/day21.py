import sys

REVERSE_AMOUNTS = {1: 1, 3: 2, 5: 3, 7: 4, 2: 6, 4: 7, 6: 8, 0: 9}


def swap_positions(string: list[str], pos_1: int, pos_2: int) -> list[str]:
    string[pos_1], string[pos_2] = string[pos_2], string[pos_1]
    return string


def swap_letters(string: list[str], letter_1: str, letter_2: str) -> list[str]:
    for index, element in enumerate(string):
        if element == letter_1:
            string[index] = letter_2
        if element == letter_2:
            string[index] = letter_1
    return string


def rotate(string: list[str], direction: str, amount: int) -> list[str]:
    if direction == "right":
        for _ in range(amount):
            string.insert(0, string.pop())
    elif direction == "left":
        for _ in range(amount):
            string.append(string.pop(0))
    return string


def reverse(string, pos_1: int, pos_2: int) -> list[str]:
    string[pos_1 : pos_2 + 1] = string[pos_1 : pos_2 + 1][::-1]
    return string


def move(string, pos_1: int, pos_2: int) -> list[str]:
    string.insert(pos_2, string.pop(pos_1))
    return string


def perform_operation(
    operation: str, string: list[str], reversed: bool = False
) -> list[str]:
    split_operation = operation.split()
    match split_operation[0]:
        case "swap":
            arg_1, arg_2 = split_operation[2], split_operation[5]
            if split_operation[1] == "position":
                return swap_positions(string, int(arg_1), int(arg_2))
            return swap_letters(string, arg_1, arg_2)
        case "rotate":
            if split_operation[1] != "based":
                direction = split_operation[1]
                if reversed:
                    direction = "right" if direction == "left" else "left"
                return rotate(string, direction, int(split_operation[2]))
            amount = string.index(split_operation[-1])
            if reversed:
                amount = REVERSE_AMOUNTS[amount]
                return rotate(string, "left", amount)
            else:
                if amount >= 4:
                    amount += 1
                amount += 1
                return rotate(string, "right", amount)
        case "reverse":
            return reverse(string, int(split_operation[2]), int(split_operation[4]))
        case "move":
            arg_1, arg_2 = int(split_operation[2]), int(split_operation[5])
            if reversed:
                arg_1, arg_2 = arg_2, arg_1
            return move(string, arg_1, arg_2)
        case _:
            raise ValueError


def perform_instructions(
    string: str, operations: list[str], reversed: bool = False
) -> str:
    string_list = list(string)
    if reversed:
        operations = operations[::-1]
    for operation in operations:
        string_list = perform_operation(operation, string_list, reversed)
    return "".join(string_list)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    string = "abcde" if "example" in file_name else "abcdefgh"
    scrambled_string = "fbgdceah"
    instructions = open(file_name).read().strip().split("\n")
    result = perform_instructions(string, instructions)
    print(f"The scrambled password is {result}")
    if "example" not in file_name:
        unscramble = perform_instructions(scrambled_string, instructions, True)
        print(f"The unscrambled password is {unscramble}")
