import sys


def supports_tls(code: str) -> bool:
    in_brackets = False
    found_pair = False
    for index in range(len(code) - 3):
        if code[index] == "[":
            in_brackets = True
            continue
        if code[index] == "]":
            in_brackets = False
            continue
        if (
            code[index] != code[index + 1]
            and code[index] == code[index + 3]
            and code[index + 1] == code[index + 2]
        ):
            if in_brackets:
                return False
            found_pair = True
    return found_pair


def supports_ssl(code: str) -> bool:
    in_brackets = False
    found_aba = set()
    found_bab = set()
    for index in range(len(code) - 2):
        if code[index] == "[":
            in_brackets = True
            continue
        if code[index] == "]":
            in_brackets = False
            continue
        if "[" in code[index : index + 3] or "]" in code[index : index + 3]:
            continue
        if code[index] != code[index + 1] and code[index] == code[index + 2]:
            if in_brackets:
                found_bab.add(f"{code[index + 1]}{code[index]}")
            else:
                found_aba.add(f"{code[index]}{code[index + 1]}")
    return len(found_aba.intersection(found_bab)) > 0


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    codes = open(file_name).read().strip().splitlines()
    print(f"{sum(map(supports_tls, codes))} IPs support TLS.")
    print(f"{sum(map(supports_ssl, codes))} IPs support SSL.")
