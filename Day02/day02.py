import sys

LOCATIONS = {
    (0, 0): "1",
    (0, 1): "2",
    (0, 2): "3",
    (1, 0): "4",
    (1, 1): "5",
    (1, 2): "6",
    (2, 0): "7",
    (2, 1): "8",
    (2, 2): "9",
}

LOCATIONS_BATHROOM = {
    (0, -2): "5",
    (0, -1): "6",
    (0, 0): "7",
    (0, 1): "8",
    (0, 2): "9",
    (-1, -1): "2",
    (-1, 0): "3",
    (-1, 1): "4",
    (-2, 0): "1",
    (1, -1): "A",
    (1, 0): "B",
    (1, 1): "C",
    (2, 0): "D",
}

DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def combination(instructions: list[str], bathroom: bool = False) -> str:
    position = (1, 1) if not bathroom else (0, -2)
    combination = ""
    for line in instructions:
        for instruction in line:
            new_position = sum_duples(position, DIRECTIONS[instruction])
            if (not bathroom and new_position in LOCATIONS) or (
                bathroom and new_position in LOCATIONS_BATHROOM
            ):
                position = new_position
        combination += (
            LOCATIONS[position] if not bathroom else LOCATIONS_BATHROOM[position]
        )
    return combination


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    instructions = open(file_name).read().strip().splitlines()
    print(f"The combination is {combination(instructions)}")
    print(f"The combination for the bathroom is {combination(instructions, True)}")
