from pprint import pprint
from typing import Tuple, List


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


def parse(data: str, input_nbr: int, output_nbr: int):
    assert len(data) == 144, len(data)
    cursor = 0
    inputs_indexes = [data[cursor : cursor + input_nbr * 6][i * 6 : (i + 1) * 6] for i in range(input_nbr)]
    cursor += input_nbr * 6
    # assert inputs_indexes == ['101101', '011111', '101111', '111100']
    inputs_indexes = [int(binary, base=2) for binary in inputs_indexes]
    outputs_indexes = [data[cursor : cursor + output_nbr * 6][i * 6 : (i + 1) * 6] for i in range(output_nbr)]
    cursor += output_nbr * 6
    # assert outputs_indexes == ['111010', '111100']
    outputs_indexes = [int(binary, base=2) for binary in outputs_indexes]
    perceptrons_data = []
    while True:
        perceptron_data_size = int(data[cursor : cursor + 6], base=2) * 32 + 4 + 6
        current_perceptron_data = data[cursor : cursor + perceptron_data_size].ljust(perceptron_data_size, "0")
        activation_function_data, inputs_data, weights_data = parse_perceptron_data(current_perceptron_data)
        perceptrons_data.append(
            {
                "activation_function_data": activation_function_data,
                "inputs_data": inputs_data,
                "weights_data": weights_data,
            }
        )
        cursor += perceptron_data_size
        if cursor >= len(data) - 1:
            break
    return inputs_indexes, outputs_indexes, perceptrons_data


if __name__ == "__main__":
    parse(
        "000001" "000010" "000000" "000010" "000010" "000001"
        # Perceptron 0
        "000010" "0000"
        # Weights
        "000000" "00000000000000000000000000" "000000" "00000000000000000000000000"
        # Perceptron 1
        "000000" "0000"
        # Weights
        "000000" "000000000000000000".replace(" ", ""),
        2,
        4,
    )
