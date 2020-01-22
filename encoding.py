from typing import Tuple, List, Callable

from activation_functions import identity, sigmoid, relu
from neural_network import Network, Perceptron, NetworkInput


def parse_input_and_weight(input_and_weight_data: str) -> Tuple[str, str]:
    return input_and_weight_data[0:6], input_and_weight_data[6:32]


def parse_perceptron_data(data: str) -> Tuple[str, List[str], List[str]]:
    inputs_and_weights_data = data[10:]
    inputs_data, weights_data = [], []
    for i in range(0, len(inputs_and_weights_data), 32):
        input_data, weight_data = parse_input_and_weight(inputs_and_weights_data[i : i + 32])
        inputs_data.append(input_data)
        weights_data.append(weight_data)
    return data[6:10], inputs_data, weights_data


def parse(
    data: str, input_nbr: int, output_nbr: int
) -> Tuple[List[str], List[str], List[Tuple[str, List[str], List[str]]]]:
    cursor = input_nbr * 6 + output_nbr * 6
    perceptrons_data = []
    while True:
        perceptron_data_size = int(data[cursor : cursor + 6], base=2) * 32 + 4 + 6
        perceptrons_data.append(
            parse_perceptron_data(data[cursor : cursor + perceptron_data_size].ljust(perceptron_data_size, "0"))
        )
        cursor += perceptron_data_size
        if cursor >= len(data) - 1:
            break
    return (
        [data[0 : input_nbr * 6][i * 6 : (i + 1) * 6] for i in range(input_nbr)],
        [data[input_nbr * 6 : input_nbr * 6 + output_nbr * 6][i * 6 : (i + 1) * 6] for i in range(output_nbr)],
        perceptrons_data,
    )


def read(
    inputs_indexes_data: List[str],
    outputs_indexes_data: List[str],
    perceptrons_data: List[Tuple[str, List[str], List[str]]],
) -> Tuple[List[int], List[int], List[Tuple[Callable, List[int], List[float]]]]:
    return (
        [int(input_index_data, base=2) for input_index_data in inputs_indexes_data],
        [int(output_index_data, base=2) for output_index_data in outputs_indexes_data],
        [
            (
                {"0000": identity, "0001": sigmoid, "0010": relu}[perceptron_data[0]],
                [int(i, base=2) for i in perceptron_data[1]],
                [int(i, base=2) / 10 ** 6 for i in perceptron_data[2]],
            )
            for perceptron_data in perceptrons_data
        ],
    )


def build_neural_network(
    network_input_perceptrons_indexes: List[int],
    network_output_perceptrons_indexes: List[int],
    perceptrons_details: List[Tuple[Callable, List[int], List[float]]],
) -> Network:
    perceptrons = [
        (NetworkInput if index in network_input_perceptrons_indexes else Perceptron)(activation_function, [])
        for index, (activation_function, input_perceptrons_indexes, weight) in enumerate(perceptrons_details)
    ]
    for (activation_function, input_perceptrons_indexes, weights), perceptron in zip(perceptrons_details, perceptrons):
        for index, weight in zip(input_perceptrons_indexes, weights):
            perceptron.add_as_input(perceptrons[index], weight)
    network_input_perceptrons, network_output_perceptrons, computing_perceptrons = [], [], []
    for i, perceptron in enumerate(perceptrons):
        if i in network_input_perceptrons_indexes:
            network_input_perceptrons.append(perceptron)
        elif i in network_output_perceptrons_indexes:
            network_output_perceptrons.append(perceptron)
        else:
            computing_perceptrons.append(perceptron)
    return Network(network_input_perceptrons, computing_perceptrons, network_output_perceptrons)


if __name__ == "__main__":
    scope = build_neural_network(
        *read(
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
    )
