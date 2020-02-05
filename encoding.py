import os
import random
from typing import Tuple, List, Callable

from activation_functions import identity, sigmoid, relu
from neural_network import Network, Perceptron, NetworkInput

NETWORK_INPUT_INDEX_SIZE = 6
NETWORK_OUTPUT_INDEX_SIZE = 6
PERCEPTRON_INPUT_INDEX_SIZE = 4
WEIGHT_SIZE = 26
WEIGHTED_PERCEPTRON_INDEX_SIZE = 6
ACTIVATION_FUNCTION_KEY_SIZE = 4
PERCEPTRON_INPUT_NUMBER_SIZE = 6


def parse_input_and_weight(input_and_weight_data: str) -> Tuple[str, str]:
    return (
        input_and_weight_data[0:PERCEPTRON_INPUT_INDEX_SIZE],
        input_and_weight_data[PERCEPTRON_INPUT_INDEX_SIZE : WEIGHT_SIZE + WEIGHTED_PERCEPTRON_INDEX_SIZE],
    )


def parse_perceptron_data(data: str) -> Tuple[str, List[str], List[str]]:
    inputs_and_weights_data = data[ACTIVATION_FUNCTION_KEY_SIZE + PERCEPTRON_INPUT_NUMBER_SIZE :]
    inputs_data, weights_data = [], []
    for i in range(0, len(inputs_and_weights_data), WEIGHT_SIZE + WEIGHTED_PERCEPTRON_INDEX_SIZE):
        input_data, weight_data = parse_input_and_weight(
            inputs_and_weights_data[i : i + WEIGHT_SIZE + WEIGHTED_PERCEPTRON_INDEX_SIZE]
        )
        inputs_data.append(input_data)
        weights_data.append(weight_data)
    return (
        data[PERCEPTRON_INPUT_NUMBER_SIZE : PERCEPTRON_INPUT_NUMBER_SIZE + ACTIVATION_FUNCTION_KEY_SIZE],
        inputs_data,
        weights_data,
    )


def parse(
    data: str, input_nbr: int, output_nbr: int
) -> Tuple[List[str], List[str], List[Tuple[str, List[str], List[str]]]]:
    """
    Takes a binary string as input and splits it into logical parts.
    Returns three things.
    The first one is the list of the indexes of the input perceptrons.
    The second one is the list of the indexes of the output perceptrons.
    Finally, the third one is the data describing all the perceptrons.
    See the file 'design' to know the rules used to split the data.
    """
    cursor = input_nbr * NETWORK_INPUT_INDEX_SIZE + output_nbr * NETWORK_OUTPUT_INDEX_SIZE
    if cursor >= len(data):
        raise RuntimeError(f"data is too short : size is {len(data)} whereas {cursor + 1} or more is required")
    perceptrons_data = []
    while True:
        perceptron_data_size = (
            int(data[cursor : cursor + PERCEPTRON_INPUT_NUMBER_SIZE], base=2)
            * (WEIGHTED_PERCEPTRON_INDEX_SIZE + WEIGHTED_PERCEPTRON_INDEX_SIZE)
            + ACTIVATION_FUNCTION_KEY_SIZE
            + PERCEPTRON_INPUT_NUMBER_SIZE
        )
        perceptrons_data.append(
            parse_perceptron_data(data[cursor : cursor + perceptron_data_size].ljust(perceptron_data_size, "0"))
        )
        cursor += perceptron_data_size
        if cursor >= len(data) - 1:
            break
    return (
        [
            data[0 : input_nbr * NETWORK_INPUT_INDEX_SIZE][
                i * NETWORK_INPUT_INDEX_SIZE : (i + 1) * NETWORK_INPUT_INDEX_SIZE
            ]
            for i in range(input_nbr)
        ],
        [
            data[
                input_nbr * NETWORK_INPUT_INDEX_SIZE : input_nbr * NETWORK_INPUT_INDEX_SIZE
                + output_nbr * NETWORK_OUTPUT_INDEX_SIZE
            ][i * NETWORK_OUTPUT_INDEX_SIZE : (i + 1) * NETWORK_OUTPUT_INDEX_SIZE]
            for i in range(output_nbr)
        ],
        perceptrons_data,
    )


def read(
    inputs_indexes_data: List[str],
    outputs_indexes_data: List[str],
    perceptrons_data: List[Tuple[str, List[str], List[str]]],
) -> Tuple[List[int], List[int], List[Tuple[Callable[[float], float], List[int], List[float]]]]:
    """
    Takes the output of parse as input and transform it from binary strings to actual value (int, float, function ...).
    The output is the same as in parse except that the content of the data structure is no longer binary strings
    """
    return (
        [int(input_index_data, base=2) for input_index_data in inputs_indexes_data],
        [int(output_index_data, base=2) for output_index_data in outputs_indexes_data],
        [
            (
                {"0000": identity, "0001": sigmoid, "0010": relu}.get(perceptron_data[0], sigmoid),
                [int(i, base=2) for i in perceptron_data[1]],
                [int(i, base=2) / 2 ** 26 for i in perceptron_data[2]],
            )
            for perceptron_data in perceptrons_data
        ],
    )


def build_neural_network(
    network_input_perceptrons_indexes: List[int],
    network_output_perceptrons_indexes: List[int],
    perceptrons_details: List[Tuple[Callable[[float], float], List[int], List[float]]],
) -> Network:
    """
    Takes the output of read as input and build a Network object with it.
    """
    perceptron_nbr = len(perceptrons_details)
    network_input_perceptrons_indexes = [index % perceptron_nbr for index in network_input_perceptrons_indexes]
    network_output_perceptrons_indexes = [index % perceptron_nbr for index in network_output_perceptrons_indexes]
    perceptrons = [
        (NetworkInput if index in network_input_perceptrons_indexes else Perceptron)(activation_function, [], [])
        for index, (activation_function, _, _) in enumerate(perceptrons_details)
    ]
    for (_, input_perceptrons_indexes, weights), perceptron in zip(perceptrons_details, perceptrons):
        for index, weight in zip(input_perceptrons_indexes, weights):
            perceptron.add_as_input(perceptrons[index % len(perceptrons)], weight)
    network_input_perceptrons, network_output_perceptrons, hidden_perceptrons = [], [], []
    for index, perceptron in enumerate(perceptrons):
        index = index % perceptron_nbr
        if index not in network_input_perceptrons_indexes and index not in network_output_perceptrons_indexes:
            hidden_perceptrons.append(perceptron)
    for index in network_input_perceptrons_indexes:
        network_input_perceptrons.append(perceptrons[index % perceptron_nbr])
    for index in network_output_perceptrons_indexes:
        network_output_perceptrons.append(perceptrons[index % perceptron_nbr])
    return Network(network_input_perceptrons, hidden_perceptrons, network_output_perceptrons)


def build_neural_network_from_binary_string(data: str, input_nbr: int, output_nbr: int) -> Network:
    """"
    Shortcut for build_neural_network(*read(*parse(data, input_nbr, output_nbr)))
    """
    # todo test
    return build_neural_network(*read(*parse(data, input_nbr, output_nbr)))


def main():
    input_nbr = 1
    network = build_neural_network_from_binary_string(
        # "000001" "000010" "000000" "000010" "000010" "000001"
        # # Perceptron 0
        # "000010" "0000"
        # # Weights
        # "000000" "00000011111111111111111100" "000000" "00000000000000000000000000"
        # # Perceptron 1
        # "000000" "0000"
        # # Weights
        # "000000" "000000000000000000",
        "".join([str(random.randint(0, 1)) for _ in range(random.randint(49, 5000))]),
        input_nbr,
        3,
    )
    while True:
        input(">>>")
        with open("nn.dot", "w") as f:
            f.write(network.write_as_graphviz())
        os.system("dot -Tpng nn.dot -o neural_network.png")
        network.feedforward([random.random() for _ in range(input_nbr)])


if __name__ == "__main__":
    main()
