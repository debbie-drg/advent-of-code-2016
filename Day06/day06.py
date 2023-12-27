import sys
from collections import defaultdict

def decode(codes: list[str]) -> str:
    counts = [defaultdict(int) for _ in range(len(codes[0]))]
    for code in codes:
        for index, char in enumerate(code):
            counts[index][char] += 1
    decoded_1 = decoded_2 = ""
    for count in counts:
        letters = list(count.keys())
        letters.sort(key=lambda letter: count[letter])
        decoded_1 += letters[-1]
        decoded_2 += letters[0]
    return decoded_1, decoded_2


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    codes = open(file_name).read().strip().splitlines()
    decoded_1, decoded_2 = decode(codes)
    print(f"The decoded word is {decoded_1}")
    print(f"With modified repetitions, it's {decoded_2}")