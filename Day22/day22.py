import sys
from itertools import combinations
import heapq

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def neighbours(duple: tuple[int, int]) -> list[tuple[int, int]]:
    return [sum_duples(duple, direction) for direction in DIRECTIONS]


class Node:
    def __init__(self, df_line: str):
        split_line = df_line.split()
        self.size, self.used, self.avail = (
            int(element.removesuffix("T")) for element in split_line[1:4]
        )
        path = split_line[0].split("-")
        self.pos = (int(path[1].removeprefix("x")), int(path[2].removeprefix("y")))

    def compatible(self, __other) -> bool:
        if self.pos == __other.pos:
            return False
        self_fits_in_other = self.used < __other.avail
        other_fits_in_self = __other.used < self.avail
        if self.used == 0:
            return other_fits_in_self
        if __other.used == 0:
            return self_fits_in_other
        return other_fits_in_self or self_fits_in_other


class DriveMap:
    def __init__(self, df_output: list[str]):
        self.nodes = {}
        for line in df_output[2:]:
            node = Node(line)
            if node.used == 0:
                self.empty = node.pos
            self.nodes[node.pos] = node
        x_pos = [pos[0] for pos in self.nodes]
        self.min_x, self.max_x = min(x_pos), max(x_pos)
        y_pos = [pos[1] for pos in self.nodes]
        self.min_y, self.max_y = min(y_pos), max(y_pos)
        self.goal = (self.max_x, 0)

    def count_compatible(self) -> int:
        count = 0
        for node_1, node_2 in combinations(self.nodes, 2):
            count += self.nodes[node_1].compatible(self.nodes[node_2])
        return count

    def in_bounds(self, position: tuple[int, int]) -> bool:
        return (
            self.min_x <= position[0] <= self.max_x
            and self.min_y <= position[1] <= self.max_y
        )

    def shortest_path(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        obstacles: set[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        queue = [(0, start, [start])]
        if start == self.empty:
            obstacles.update(
                {position for position in self.nodes if self.nodes[position].used > 100}
            )
        visited = set()
        while True:
            steps, position, path = heapq.heappop(queue)
            next_steps = neighbours(position)
            for neighbour in next_steps:
                if neighbour in visited:
                    continue
                if not self.in_bounds(position):
                    continue
                if neighbour in obstacles:
                    continue
                if neighbour == end:
                    return path + [neighbour]
                visited.add(neighbour)
                heapq.heappush(queue, (steps + 1, neighbour, path + [neighbour]))

    def min_steps(self) -> int:
        start_to_end = self.shortest_path((0, 0), self.goal, set())
        empty_to_end = self.shortest_path(self.empty, start_to_end[-2], {self.goal})
        return len(empty_to_end) + 5 * (len(start_to_end) - 2)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    df_output = open(file_name).read().strip().split("\n")
    drive_map = DriveMap(df_output)
    compatible = drive_map.count_compatible()
    print(f"The number of compatible pairs is {compatible}")
    min_steps = drive_map.min_steps()
    print(f"The minimum number of steps to move the data is {min_steps}")
