import sys, re
from multiprocessing import Pool


def triangle_valid(sides: list[int]) -> bool:
    sides.sort()
    return sides[0] + sides[1] > sides[2]


def vertical_triangles_valid(sides: list[int]) -> int:
    triangles = [[sides[i][j] for i in range(3)] for j in range(3)]
    return sum(map(triangle_valid, triangles))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    instructions = open(file_name).read().strip().splitlines()
    instructions = [
        [int(side) for side in re.findall("[0-9]+", sides)] for sides in instructions
    ]
    pool = Pool(8)
    valid = sum(pool.map(triangle_valid, instructions))
    print(f"The number of valid triangles is {valid}.")
    result = 0
    for index in range(0, len(instructions), 3):
        result += vertical_triangles_valid(instructions[index : index + 3])
    print(f"For the second part, it's {result}")
