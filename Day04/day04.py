import sys

MIN_ORDER = ord("a")
MODULO = ord("z") - ord("a") + 1


def parse_input(room_data: str) -> tuple[dict[str, int], int, str]:
    room, checksum = room_data.split("[")
    checksum = checksum.removesuffix("]")
    room = room.split("-")
    number = int(room[-1])
    room = "".join(room[:-1])
    letters = list(set(room))
    counts = {letter: room.count(letter) for letter in letters}
    return (counts, number, checksum)


def is_room_real(room_data: str) -> int:
    counts, number, checksum = parse_input(room_data)
    for letter in checksum:
        if letter not in counts:
            return 0
    last_count = counts[checksum[0]]
    last_letter = checksum[0]
    for letter in checksum:
        if counts[letter] > last_count:
            return 0
        if counts[letter] == last_count:
            if letter < last_letter:
                return 0
        last_count = counts[letter]
        last_letter = letter
    return number


def shift_cipher(word: str, shift: int):
    return "".join(
        chr((ord(letter) - MIN_ORDER + shift) % MODULO + MIN_ORDER) for letter in word
    )


def decrypt(room_data: str) -> tuple[str, int]:
    useful_data = room_data.split("[")[0].split("-")
    number = int(useful_data[-1])
    words = useful_data[:-1]
    words = " ".join(shift_cipher(word, number) for word in words).strip()
    return words, number


def find_north_pole(rooms: list[str]) -> int:
    for room in rooms:
        name, sector = decrypt(room)
        if name == "northpole object storage":
            return sector


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    rooms = open(file_name).read().strip().splitlines()

    print(f"The sum of sectors of real rooms is {sum(map(is_room_real, rooms))}")
    print(f"The northpole object storage sector is {find_north_pole(rooms)}")
