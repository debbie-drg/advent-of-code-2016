import sys


class Robot:
    def __init__(self, idx, low_to: int, high_to: int) -> None:
        self.idx = idx
        self.low_to = low_to
        self.high_to = high_to
        self.low = None
        self.high = None
        self.unasigned = None

    def __hash__(self) -> int:
        return self.idx.__hash__()

    def in_value(self, value: int) -> bool:
        if self.unasigned is not None:
            self.low = min(self.unasigned, value)
            self.high = max(self.unasigned, value)
            self.unasigned = None
            return True
        self.unasigned = value
        return False

    def reset(self) -> tuple[int, int, int, int]:
        low = self.low
        high = self.high
        self.low = None
        self.high = None
        return low, high, self.low_to, self.high_to


class RobotGroup:
    def __init__(self, instructions: str, low_to_seek: int, high_to_seek: int) -> None:
        self.bots = {}
        split_instructions = instructions.split("\n")
        initial_values = []
        full_robots = []
        self.output_prod = 1
        while split_instructions:
            instruction = split_instructions.pop().split()
            if instruction[0] == "value":
                initial_values.append((int(instruction[1]), int(instruction[5])))
                continue
            idx = int(instruction[1])
            if instruction[5] == "output":
                low_to = -int(instruction[6]) - 1
            else:
                low_to = int(instruction[6])
            if instruction[10] == "output":
                high_to = -int(instruction[11]) - 1
            else:
                high_to = int(instruction[11])
            self.bots[idx] = Robot(idx, low_to, high_to)
        for value, robot in initial_values:
            if self.bots[robot].in_value(value):
                full_robots.append(robot)
        while full_robots:
            robot = full_robots.pop(0)
            low, high, low_to, high_to = self.bots[robot].reset()
            if low == low_to_seek and high == high_to_seek:
                self.responsible_bot = robot
            if low_to >= 0:
                if self.bots[low_to].in_value(low):
                    full_robots.append(low_to)
            elif low_to in [-1, -2, -3]:
                self.output_prod *= low
            if high_to >= 0:
                if self.bots[high_to].in_value(high):
                    full_robots.append(high_to)
            elif high_to in [-1, -2, -3]:
                self.output_prod *= high


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    if "example" in file_name:
        low_to_seek = 2
        high_to_seek = 5
    else:
        low_to_seek = 17
        high_to_seek = 61
    instructions = open(file_name).read().strip()
    robot_group = RobotGroup(instructions, low_to_seek, high_to_seek)
    print(f"The robot responsible for the comparison is {robot_group.responsible_bot}")
    print(f"The product of chips in outputs 0, 1 and 2 is {robot_group.output_prod}")
