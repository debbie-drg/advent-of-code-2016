import sys
from hashlib import md5
import heapq

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRECTION_KEYS = ["U", "D", "L", "R"]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def md5_hash_doors(input_string: str) -> str:
    return md5(input_string.encode("utf-8")).hexdigest()[:4]


def in_bounds(position: tuple[int, int]) -> bool:
    return 0 <= position[0] < 4 and 0 <= position[1] < 4


def open_doors(passcode: str, path: str) -> list[int]:
    hash_instructions = md5_hash_doors(passcode + path)
    open_doors = []
    for index in range(4):
        if hash_instructions[index] in {"b", "c", "d", "e", "f"}:
            open_doors.append(index)
    return open_doors


def shortest_path(passcode: str) -> tuple[int, int]:
    queue = [(0, (0, 0), "")]
    paths = []
    while queue:
        steps, position, path = heapq.heappop(queue)
        doors_to_check = open_doors(passcode, path)
        for door in doors_to_check:
            next_position = sum_duples(position, DIRECTIONS[door])
            if not in_bounds(next_position):
                continue
            if next_position == (3, 3):
                paths.append(path + DIRECTION_KEYS[door])
            else:
                heapq.heappush(
                    queue, (steps + 1, next_position, path + DIRECTION_KEYS[door])
                )
    return paths[0], max(len(path) for path in paths)


if __name__ == "__main__":
    try:
        passcode = sys.argv[1]
    except IndexError:
        passcode = "ihgpwlah"
    path, longest_path_length = shortest_path(passcode)
    print(f"The shortest path is {path}")
    print(f"The length of the longest path is {longest_path_length}")
