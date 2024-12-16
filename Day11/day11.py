import sys
import functools
from copy import copy
import heapq
from itertools import combinations


def parse(input_data: str) -> str:
    split_data = input_data.split("\n")
    split_lines = [line.split() for line in split_data]
    chips = ""
    generators = ""
    elements = set()
    for line in split_lines:
        for index, word in enumerate(line):
            if "generator" in word:
                elements.add(line[index - 1])
    element_dict = {element: index for index, element in enumerate(elements)}
    for index, line in enumerate(split_data):
        for element in element_dict:
            if f"{element}-compatible" in line:
                chips += "1"
            else:
                chips += "0"
            if f"{element} generator" in line:
                generators += "1"
            else:
                generators += "0"
    return generators + chips


def add_elements(input_data: str, number_to_add: int) -> str:
    middle_point = len(initial_state) // 2
    number_elements = middle_point // 4
    generators, chips = input_data[: len(input_data) // 2], input_data[len(input_data) // 2 :]
    starts = [index * number_elements for index in range(4)]
    ends = [(index + 1) * number_elements for index in range(4)]
    chips_per_line = [chips[starts[index]:ends[index]] for index in range(4)]
    generators_per_line = [generators[starts[index]:ends[index]] for index in range(4)]
    chips_per_line[0] += "1" * number_to_add
    generators_per_line[0] += "1" * number_to_add
    for index in range(1,4):
        chips_per_line[index] += "0" * number_to_add
        generators_per_line[index] += "0" * number_to_add
    return "".join(generators_per_line) + "".join(chips_per_line)


@functools.cache
def is_safe(state: str) -> bool:
    generators, chips = (
        state[: len(state) // 2],
        state[len(state) // 2 :],
    )
    number_elements = len(generators) // 4
    for floor in range(4):
        gen_floor, chips_floor = (
            generators[(number_elements * floor) : (number_elements * (floor + 1))],
            chips[(number_elements * floor) : (number_elements * (floor + 1))],
        )
        for index, chip in enumerate(chips_floor):
            if chip == "1" and gen_floor[index] != "1" and "1" in gen_floor:
                return False
    return True


def min_steps(initial_state: str) -> int:
    queue = [(0, 0, initial_state)]
    visited = set([(0, initial_state)])
    middle_point = len(initial_state) // 2
    number_elements = middle_point // 4
    starts = [index * number_elements for index in range(4)]
    ends = [(index + 1) * number_elements for index in range(4)]
    end_state = ["0"] * number_elements * 3 + ["1"] * number_elements
    end_state += end_state
    while True:
        steps, elevator, state = heapq.heappop(queue)
        state_list = list(state)
        movable_1 = [
            index
            for index in range(starts[elevator], ends[elevator])
            if state_list[index] == "1"
        ]
        movable_2 = [
            index + middle_point
            for index in range(starts[elevator], ends[elevator])
            if state_list[index + middle_point] == "1"
        ]
        movable = movable_1 + movable_2
        for value in [-1, 1]:
            next_elevator = elevator + value
            if next_elevator < 0 or next_elevator >= 4:
                continue
            for element in movable:
                new_state = copy(state_list)
                new_state[element] = "0"
                new_state[element + value * number_elements] = "1"
                if new_state == end_state:
                    return steps + 1
                new_state_str = "".join(new_state)
                if (
                    is_safe(new_state_str)
                    and (next_elevator, new_state_str) not in visited
                ):
                    heapq.heappush(queue, (steps + 1, next_elevator, new_state_str))
                    visited.add((next_elevator, new_state_str))
            for element_1, element_2 in combinations(movable, 2):
                new_state = copy(state_list)
                new_state[element_1] = "0"
                new_state[element_2] = "0"
                new_state[element_1 + value * number_elements] = "1"
                new_state[element_2 + value * number_elements] = "1"
                if new_state == end_state:
                    return steps + 1
                new_state_str = "".join(new_state)
                if (
                    is_safe(new_state_str)
                    and (next_elevator, new_state_str) not in visited
                ):
                    heapq.heappush(queue, (steps + 1, next_elevator, new_state_str))
                    visited.add((next_elevator, new_state_str))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    initial_state = parse(open(file_name).read().strip())
    print(f"The minimum number of steps is {min_steps(initial_state)}")
    with_hidden_components = add_elements(initial_state, 2)
    print(f"With the new found components, it's {min_steps(with_hidden_components)}")
