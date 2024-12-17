import sys
import functools
import heapq

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def neighbours(position: tuple[int, int]) -> list[tuple[int, int]]:
    return [sum_duples(position, direction) for direction in DIRECTIONS]


class Maze:
    def __init__(self, favourite_number: int) -> None:
        self.favourite_number = favourite_number

    @functools.cache
    def is_wall(self, position: tuple[int, int]) -> bool:
        if position[0] < 0 or position[1] < 0:
            return True
        x, y = position
        value = x * x + 3 * x + 2 * x * y + y + y * y
        value += self.favourite_number
        number_bits = bin(value)[2:].count("1")
        return number_bits % 2 == 1

    def print_maze(self, height: int, width: int) -> str:
        output = ""
        for row in range(height):
            line = ""
            for col in range(width):
                if self.is_wall((col, row)):
                    line += "#"
                else:
                    line += "."
            output += line + "\n"
        return output.strip()

    def valid_neighbours(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        to_check = neighbours(position)
        return [position for position in to_check if not self.is_wall(position)]

    def path_length(self, goal: tuple[int, int]) -> tuple[int, int]:
        queue = [(0, (1, 1))]
        shortest_distances = {}
        under_fifty = set([(1, 1)])
        while True:
            steps, position = heapq.heappop(queue)
            print(steps, end="\r")
            to_check = self.valid_neighbours(position)
            for next_position in to_check:
                if next_position in shortest_distances:
                    if steps + 1 >= shortest_distances[next_position]:
                        continue
                if steps + 1 <= 50:
                    under_fifty.add(next_position)
                shortest_distances[next_position] = steps + 1
                if next_position == goal:
                    return steps + 1, len(under_fifty)
                heapq.heappush(queue, (steps + 1, next_position))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    favourite_number = int(open(file_name).read().strip())
    maze = Maze(favourite_number)
    goal = (7, 4) if "example" in file_name else (31, 39)
    shortest_path, under_fifty = maze.path_length(goal)
    print(f"The length of the shortest path is {shortest_path}")
    print(f"The number of positions reachable in 50 steps is {under_fifty}")
