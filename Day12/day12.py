import sys
from collections import defaultdict

class AssembunnyMachine:
    def __init__(self, instructions: list[str]) -> None:
        self.registers = defaultdict(int)
        self.instructions = [instruction.split() for instruction in instructions]

    def run_instruction(self, index: int) -> int:
        instruction = self.instructions[index]
        match instruction[0]:
            case "cpy":
                if instruction[1].isnumeric():
                    self.registers[instruction[2]] = int(instruction[1])
                else:
                    self.registers[instruction[2]] = self.registers[instruction[1]]
            case "inc":
                self.registers[instruction[1]] += 1
            case "dec":
                self.registers[instruction[1]] -= 1
            case "jnz":
                if instruction[1].isnumeric():
                    value = instruction[1]
                else:
                    value = self.registers[instruction[1]]
                if value != 0:
                    return int(instruction[2])
        return 1
    
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
    assembuny_machine.run()
    print(f"The final value of register a is {assembuny_machine.registers["a"]}")
    assembuny_machine = AssembunnyMachine(instructions)
    assembuny_machine.registers["c"] = 1
    assembuny_machine.run()
    print(f"With register c started as 1, it's {assembuny_machine.registers["a"]}")