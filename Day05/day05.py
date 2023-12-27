import sys
import hashlib


def decode_password(door_name: str) -> tuple[int, int]:
    counter = 0
    password_1 = ""
    password_2 = [False for _ in range(8)]
    while not all(password_2):
        next_hash = hashlib.md5(f"{door_name}{str(counter)}".encode()).hexdigest()
        counter += 1
        if next_hash[:5] == "00000":
            potential_position = next_hash[5]
            if len(password_1) < 8:
                password_1 += potential_position
            if not potential_position.isnumeric():
                continue
            potential_position = int(potential_position)
            if not 0 <= potential_position < 8:
                continue
            if password_2[potential_position]:
                continue
            password_2[potential_position] = next_hash[6]
    return password_1, "".join(password_2)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    door_name = open(file_name).read().strip()
    password_1, password_2 = decode_password(door_name)
    print(f"The password is {password_1}")
    print(f"Once inside, the password is {password_2}")
