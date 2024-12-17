import sys


# Works because modulos are prime
def modulo_inverse(number, modulo) -> int:
    return number ** (modulo - 2) % modulo


def chinese_remainder_solution(remainders: list[int], modulos: list[int]):
    M = 1
    for modulo in modulos:
        M *= modulo
    Mi = [M // modulo for modulo in modulos]
    xi = [
        modulo_inverse(Mi[index] % modulos[index], modulos[index])
        for index in range(len(modulos))
    ]
    solution = (
        sum(
            [remainders[index] * Mi[index] * xi[index] for index in range(len(modulos))]
        )
        % M
    )
    return solution


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip().split("\n")
    modulos = [int(line.split()[3]) for line in input_data]

    remainders = [
        -int(input_data[index].split()[-1].removesuffix("."))
        - (index + 1) % modulos[index]
        for index in range(len(input_data))
    ]
    solution = chinese_remainder_solution(remainders, modulos)
    print(f"You would have to press the button at time {solution}")
    modulos.append(11)
    remainders.append(-len(input_data) - 1 % 11)
    solution = chinese_remainder_solution(remainders, modulos)
    print(f"With the added disk, you need to wait until {solution}")
