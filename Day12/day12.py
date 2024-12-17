import sys
from collections import defaultdict

class AssembunnyMachine:
    def __init__(self) -> None:
        self.registers = defaultdict(int)

    def run_instruction(self, instruction: str) -> int:
        split_instruction = instruction.split()
        match split_instruction[0]:
            case "cpy":
                if split_instruction[1].isnumeric():
                    self.registers[split_instruction[2]] = int(split_instruction[1])
                else:
                    self.registers[split_instruction[2]] = self.registers[split_instruction[1]]
            case "inc":
                self.registers[split_instruction[1]] += 1
            case "dec":
                self.registers[split_instruction[1]] -= 1
            case "jnz":
                if split_instruction[1].isnumeric():
                    value = split_instruction[1]
                else:
                    value = self.registers[split_instruction[1]]
                if value != 0:
                    return int(split_instruction[2])
        return 1
    
    def run_list(self, instructions: list[str]):
        counter = 0
        while counter < len(instructions):
            counter += self.run_instruction(instructions[counter])

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    assembuny_machine = AssembunnyMachine()
    instructions = open(file_name).read().strip().split("\n")
    assembuny_machine.run_list(instructions)
    print(f"The final value of register a is {assembuny_machine.registers["a"]}")
    assembuny_machine = AssembunnyMachine()
    assembuny_machine.registers["c"] = 1
    assembuny_machine.run_list(instructions)
    print(f"With register c started as 1, it's {assembuny_machine.registers["a"]}")