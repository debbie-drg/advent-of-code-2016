import sys
from hashlib import md5


def md5_hash(input_string: str) -> str:
    return md5(input_string.encode("utf-8")).hexdigest()


def three_in_a_row(input_string: str) -> str:
    for index in range(len(input_string) - 2):
        if len(set(input_string[index : index + 3])) == 1:
            return input_string[index]
    return ""


def key_index(salt: str, stretching: bool = False) -> int:
    candidates = []
    found = []
    index = 0
    wait = 1000
    while True:
        if len(found) >= 64:
            wait -= 1
        if wait == 0:
            break
        current_hash = md5_hash(f"{salt}{str(index)}")
        if stretching:
            for _ in range(2016):
                current_hash = md5_hash(current_hash)
        candidates = [
            candidate for candidate in candidates if index - candidate[0] < 1000
        ]
        for candidate in candidates:
            if (5 * candidate[1]) in current_hash:
                found.append(candidate[0])
        possible = three_in_a_row(current_hash)
        if possible:
            candidates.append([index, possible])
        index += 1
    return sorted(found)[63]


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    salt = open(file_name).read().strip()
    index = key_index(salt)
    print(f"The index at which the 64th key is obtained is {index}")
    index = key_index(salt, stretching=True)
    print(f"With stretching, it's {index}")
