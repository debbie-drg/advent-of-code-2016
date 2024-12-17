import sys

TRAP_PATTERNS = {"^^.", ".^^", "^..", "..^"}


class TrapMap:
    def __init__(self, initial_row: str) -> None:
        self.rows = [initial_row]

    def get_next_row(self):
        current_row = "." + self.rows[-1] + "."
        next_row = ""
        for index in range(len(self.rows[0])):
            if current_row[index : index + 3] in TRAP_PATTERNS:
                next_row += "^"
            else:
                next_row += "."
        self.rows.append(next_row)

    def get_rows_until(self, rows: int):
        for _ in range(rows - 1):
            self.get_next_row()

    def count_safe(self) -> int:
        return sum(row.count(".") for row in self.rows)

    def __repr__(self) -> str:
        return "\n".join(self.rows).strip()


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    first_row = open(file_name).read().strip()
    number_rows = [10] if "example" in file_name else [40, 400000]
    trap_map = TrapMap(first_row)
    for row_number in number_rows:
        trap_map.get_rows_until(row_number)
        number_safe = trap_map.count_safe()
        print(f"In {row_number} rows, the number of safe tiles is {number_safe}")
