import sys


def generate_string(in_data: str) -> str:
    more_data = in_data[::-1]
    out_data = in_data + "0"
    for data in more_data:
        out_data += "1" if data == "0" else "0"
    return out_data


def fill_disk(in_data: str, target_length: int) -> str:
    while len(in_data) < target_length:
        in_data = generate_string(in_data)
    return in_data[:target_length]


def dragon_checksum(in_data: str) -> str:
    checksum = ""
    for index in range(0, len(in_data), 2):
        if in_data[index : index + 2] in {"00", "11"}:
            checksum += "1"
        else:
            checksum += "0"
    return checksum


def fill_disk_get_checksum(in_data: str, target_length: int) -> str:
    data = fill_disk(in_data, target_length)
    while len(data) % 2 == 0:
        data = dragon_checksum(data)
    return data


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    in_data, length = open(file_name).read().strip().split()
    length = int(length)
    checksum = fill_disk_get_checksum(in_data, length)
    print(f"The final checksum is {checksum}")
