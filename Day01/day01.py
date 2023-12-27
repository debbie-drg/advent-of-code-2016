import sys

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
INSTRUCTIONS = {"R": 1, "L": -1}


def sum_duples(
    duple_1: tuple[int, int], duple_2: tuple[int, int], times: int
) -> tuple[int, int]:
    return (duple_1[0] + times * duple_2[0], duple_1[1] + times * duple_2[1])


def walk_path(instructions: list[str], twice: bool = False):
    direction_index = 0
    position = (0, 0)
    if twice:
        history = set()
    for instruction in instructions:
        instruction = instruction.strip()
        direction_index += INSTRUCTIONS[instruction[0]]
        direction_index %= 4
        if twice:
            for _ in range(int(instruction[1:])):
                position = sum_duples(position, DIRECTIONS[direction_index], 1)
                if position in history:
                    return sum(map(abs, position))
                history.add(position)
            history.add(position)
        else:
            position = sum_duples(
                position, DIRECTIONS[direction_index], int(instruction[1:])
            )

    return sum(map(abs, position))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    instructions = open(file_name).read().strip().split(",")
    print(f"We are {walk_path(instructions)} blocks away.")
    print(
        f"The first spot visited twice is {walk_path(instructions, True)} blocks away."
    )
