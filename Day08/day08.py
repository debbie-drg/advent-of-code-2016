import sys

FILLED_CHARACTER = "██"
EMPTY_CHARACTER = "░░"


class Pixel:
    def __init__(self, location: tuple[int, int]):
        self.location = location

    def rotate_row(self, num_rows: int, width: int):
        self.location = (self.location[0], (self.location[1] + num_rows) % width)

    def rotate_col(self, num_cols: int, height: int):
        self.location = ((self.location[0] + num_cols) % height, self.location[1])


class Display:
    def __init__(self, instructions: list[str], width: int, height: int):
        self.width = width
        self.height = height
        self.pixels = []
        for instruction in instructions:
            self.perform(instruction)

    def perform(self, instruction: str):
        instruction = instruction.split(" ")
        if len(instruction) == 2:  # rectangle
            width, depth = [int(number) for number in instruction[1].split("x")]
            for row_index in range(depth):
                for col_index in range(width):
                    self.pixels.append(Pixel((row_index, col_index)))
            return
        if instruction[1] == "row":
            num_row = int(instruction[2].split("=")[1])
            number_rows = int(instruction[-1])
            for pixel in self.pixels:
                if pixel.location[0] == num_row:
                    pixel.rotate_row(number_rows, self.width)
            return
        if instruction[1] == "column":
            num_col = int(instruction[2].split("=")[1])
            number_cols = int(instruction[-1])
            for pixel in self.pixels:
                if pixel.location[1] == num_col:
                    pixel.rotate_col(number_cols, self.height)
            return
        raise ValueError

    def num_pixels_on(self):
        return len(set(pixel.location for pixel in self.pixels))

    def __repr__(self) -> str:
        display = ""
        locations = set(pixel.location for pixel in self.pixels)
        for row_index in range(self.height):
            for col_index in range(self.width):
                if (row_index, col_index) in locations:
                    display += FILLED_CHARACTER
                else:
                    display += EMPTY_CHARACTER
            display += "\n"
        return display.removesuffix("\n")


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    width, height = (7, 3) if "example" in file_name else (50, 6)
    instructions = open(file_name).read().strip().splitlines()
    display = Display(instructions, width, height)
    print(f"The number of pixels on is {display.num_pixels_on()}")
    print(display)
