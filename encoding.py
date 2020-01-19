import math
from pprint import pprint
from typing import Tuple, List, Callable


def parse_input_and_weight(input_and_weight_data: str) -> Tuple[str, str]:
    return input_and_weight_data[0:6], input_and_weight_data[6:32]


def parse_perceptron_data(data: str) -> Tuple[str, List[str], List[str]]:
    activation_function_data = data[6:10]
    inputs_and_weights_data = data[10:]
    inputs_data, weights_data = [], []
    for i in range(0, len(inputs_and_weights_data), 32):
        input_data, weight_data = parse_input_and_weight(inputs_and_weights_data[i : i + 32])
        inputs_data.append(input_data)
        weights_data.append(weight_data)
    return activation_function_data, inputs_data, weights_data


def parse(
    data: str, input_nbr: int, output_nbr: int
) -> Tuple[List[str], List[str], List[Tuple[str, List[str], List[str]]]]:
    assert len(data) == 144, len(data)
    cursor = 0
    inputs_indexes_data = [data[cursor : cursor + input_nbr * 6][i * 6 : (i + 1) * 6] for i in range(input_nbr)]
    cursor += input_nbr * 6
    outputs_indexes_data = [data[cursor : cursor + output_nbr * 6][i * 6 : (i + 1) * 6] for i in range(output_nbr)]
    cursor += output_nbr * 6
    perceptrons_data = []
    while True:
        perceptron_data_size = int(data[cursor : cursor + 6], base=2) * 32 + 4 + 6
        perceptrons_data.append(
            parse_perceptron_data(data[cursor : cursor + perceptron_data_size].ljust(perceptron_data_size, "0"))
        )
        cursor += perceptron_data_size
        if cursor >= len(data) - 1:
            break
    return inputs_indexes_data, outputs_indexes_data, perceptrons_data


def read(
    inputs_indexes_data: List[str],
    outputs_indexes_data: List[str],
    perceptrons_data: List[Tuple[str, List[str], List[str]]],
) -> Tuple[List[int], List[int], List[Tuple[Callable, List[int], List[float]]]]:
    inputs_indexes = [int(input_index_data, base=2) for input_index_data in inputs_indexes_data]
    outputs_indexes = [int(output_index_data, base=2) for output_index_data in outputs_indexes_data]
    activation_functions_by_code = {
        "0000": lambda x: x,
        "0001": lambda x: 1 / (1 + math.exp(-x)),
        "0002": lambda x: max(0, x),
    }
    perceptrons_informations = []
    for perceptron_data in perceptrons_data:
        perceptrons_informations.append(
            (
                activation_functions_by_code[perceptron_data[0]],
                [int(i, base=2) for i in perceptron_data[1]],
                [int(i, base=2) / 10 ** 6 for i in perceptron_data[2]],
            )
        )
    pprint(perceptrons_informations)
    return inputs_indexes, outputs_indexes, perceptrons_informations


if __name__ == "__main__":
    read(
        *parse(
            "000001" "000010" "000000" "000010" "000010" "000001"
            # Perceptron 0
            "000010" "0000"
            # Weights
            "000000" "00000011111111111111111100" "000000" "00000000000000000000000000"
            # Perceptron 1
            "000000" "0000"
            # Weights
            "000000" "000000000000000000",
            2,
            4,
        )
    )
