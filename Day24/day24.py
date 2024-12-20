import sys
import heapq
from itertools import combinations, permutations

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def neighbours(duple: tuple[int, int]) -> list[tuple[int, int]]:
    return [sum_duples(duple, direction) for direction in DIRECTIONS]


class AirDuct:
    def __init__(self, duct_map: str) -> None:
        self.walls = set()
        self.goals = {}
        for row, line in enumerate(duct_map.split("\n")):
            for col, char in enumerate(line):
                if char == "#":
                    self.walls.add((row, col))
                if char.isnumeric():
                    self.goals[char] = (row, col)
        self.distances = None

    def valid_neighbours(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        return [
            neighbour
            for neighbour in neighbours(position)
            if not neighbour in self.walls
        ]

    def shortest_path(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        queue = [(0, start)]
        visited = set()
        while True:
            steps, position = heapq.heappop(queue)
            neighbours_to_check = self.valid_neighbours(position)
            for neighbour in neighbours_to_check:
                if neighbour in visited:
                    continue
                visited.add(neighbour)
                if neighbour == end:
                    return steps + 1
                heapq.heappush(queue, (steps + 1, neighbour))

    def pairwise_distances(self):
        self.distances = {}
        for goal_1, goal_2 in combinations(self.goals, 2):
            self.distances[frozenset([goal_1, goal_2])] = self.shortest_path(
                self.goals[goal_1], self.goals[goal_2]
            )

    def min_path_all_goals(self, end_at_0: bool = False) -> int:
        if self.distances is None:
            self.pairwise_distances()
        min_distance = float("inf")
        for permutation in permutations([goal for goal in self.goals if goal != "0"]):
            current_distance = self.distances[frozenset(["0", permutation[0]])]
            for index in range(len(permutation) - 1):
                current_distance += self.distances[
                    frozenset([permutation[index], permutation[index + 1]])
                ]
            if end_at_0:
                current_distance += self.distances[frozenset(["0", permutation[-1]])]
            min_distance = min(min_distance, current_distance)
        return int(min_distance)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    duct_map = open(file_name).read().strip()
    air_duct = AirDuct(duct_map)
    min_distance = air_duct.min_path_all_goals()
    print(f"The minimum number of steps to visit all goals is {min_distance}")
    min_distance = air_duct.min_path_all_goals(True)
    print(f"Returning to 0, it's {min_distance}")
