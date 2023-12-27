import sys
import re


def decompress(string: str, count_instructions_within: bool = False):
    parentheses = re.search(r"\((\d+)x(\d+)\)", string)
    if not parentheses:
        return len(string)
    length, times = int(parentheses.group(1)), int(parentheses.group(2))
    start_point = parentheses.start() + len(parentheses.group())
    count = (
        decompress(string[start_point : start_point + length], True)
        if count_instructions_within
        else length
    )
    return (
        len(string[: parentheses.start()])
        + times * count
        + decompress(string[start_point + length :], count_instructions_within)
    )


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    compressed = open(file_name).read().strip()
    print(f"The length of the decompressed file is {decompress(compressed)}")
    print(
        f"If instructions within a decompressed fragment are not ignored, it's {decompress(compressed, True)}"
    )
