import sys
from collections import defaultdict


def isnumeric(string: str):
    if string[0] == "-":
        return True
    return string.isnumeric()


class AssembunnyMachine:
    def __init__(self, instructions: list[str]) -> None:
        self.registers = defaultdict(int)
        self.instructions = [instruction.split() for instruction in instructions]

    def run_instruction(self, index: int) -> int:
        instruction = self.instructions[index]
        match instruction[0]:
            case "cpy":
                if isnumeric(instruction[2]):
                    return 1
                if isnumeric(instruction[1]):
                    self.registers[instruction[2]] = int(instruction[1])
                else:
                    self.registers[instruction[2]] = self.registers[instruction[1]]
            case "inc":
                if self.detect_and_do_mul(index):
                    return 4
                if isnumeric(instruction[1]):
                    return 1
                self.registers[instruction[1]] += 1
            case "dec":
                if isnumeric(instruction[1]):
                    return 1
                self.registers[instruction[1]] -= 1
            case "jnz":
                if isnumeric(instruction[1]):
                    value = instruction[1]
                else:
                    value = self.registers[instruction[1]]
                if value != 0:
                    if isnumeric(instruction[2]):
                        steps = int(instruction[2])
                    else:
                        steps = self.registers[instruction[2]]
                    return steps
            case "tgl":
                value = self.registers[instruction[1]]
                try:
                    to_change = self.instructions[index + value]
                except IndexError:
                    return 1
                if len(to_change) == 2:
                    to_change[0] = "dec" if to_change[0] == "inc" else "inc"
                else:
                    to_change[0] = "cpy" if to_change[0] == "jnz" else "jnz"
                self.instructions[index + value] = to_change
        return 1

    def detect_and_do_mul(self, index: int) -> bool:
        if not [
            instruction[0] for instruction in self.instructions[index : index + 5]
        ] == ["inc", "dec", "jnz", "dec", "jnz"]:
            return False
        if not self.instructions[index + 2][2] == "-2":
            return False
        if not self.instructions[index + 4][2] == "-5":
            return False
        initial_value = int(self.registers[self.instructions[index][1]])
        initial_reg = self.instructions[index][1]
        mul_1 = int(self.registers[self.instructions[index + 1][1]])
        mul_1_reg = self.instructions[index + 1][1]
        mul_2 = int(self.registers[self.instructions[index + 3][1]])
        mul_2_reg = self.instructions[index + 3][1]
        if len({initial_reg, mul_1_reg, mul_2_reg}) != 3:
            return False
        if mul_1_reg != self.instructions[index + 2][1]:
            return False
        if mul_2_reg != self.instructions[index + 4][1]:
            return False
        self.registers[initial_reg] = initial_value + mul_1 * mul_2
        self.registers[mul_1_reg] = 0
        self.registers[mul_2_reg] = 0
        return True

    def run(self):
        counter = 0
        while counter < len(self.instructions):
            counter += self.run_instruction(counter)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    instructions = open(file_name).read().strip().split("\n")
    assembuny_machine = AssembunnyMachine(instructions)
    if not "example" in file_name:
        assembuny_machine.registers["a"] = 7
    assembuny_machine.run()
    print(f"The final value of register a is {assembuny_machine.registers["a"]}")
    if not "example" in file_name:
        assembuny_machine = AssembunnyMachine(instructions)
        assembuny_machine.registers["a"] = 12
        assembuny_machine.run()
        print(f"With the new value, it's {assembuny_machine.registers["a"]}")
