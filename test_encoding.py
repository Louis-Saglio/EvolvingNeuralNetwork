import random
from unittest import TestCase

from encoding import parse, read, build_neural_network
from activation_functions import identity, sigmoid, relu
from neural_network import NetworkInput, Perceptron


class TestParse(TestCase):
    def test_parse(self):
        input_data, output_data, perceptrons_data = parse(
            "000000" "000010"
            # Perceptron 0
            # Input nbr
            "000010"
            # Activation function
            "0000"
            # Weights
            # Perceptron
            "000000"
            # Weight
            "00000000000000000000000000"
            # Perceptron
            "000000"
            # Weight
            "00000000000000000000111111"
            # Perceptron 1
            # Input nbr
            "000001"
            # Activation function
            "0000"
            # Weights
            # Perceptron
            "000000"
            # Weight
            "00000000000000000000000000"
            # Perceptron 2
            # Input nbr
            "000001"
            # Activation function
            "0110"
            # Weights
            # Perceptron
            "000001"
            # Weight
            "01000000001000010000000111",
            1,
            1,
        )
        self.assertListEqual(input_data, ["000000"])
        self.assertListEqual(output_data, ["000010"])
        self.assertListEqual(
            perceptrons_data,
            [
                ("0000", ["000000", "000000"], ["00000000000000000000000000", "00000000000000000000111111"]),
                ("0000", ["000000"], ["00000000000000000000000000"]),
                ("0110", ["000001"], ["01000000001000010000000111"]),
            ],
        )


class TestRead(TestCase):
    def test_read(self):
        input_indexes, output_indexes, perceptrons_details = read(
            ["000000"],
            ["000010"],
            [
                ("0000", ["000000", "000000"], ["00000000000000000000000000", "00000000000000000000111111"]),
                ("0001", ["000000"], ["00000000000000000000000000"]),
                ("0010", ["000001"], ["01000000001000010000000111"]),
            ],
        )
        self.assertListEqual(input_indexes, [0])
        self.assertListEqual(output_indexes, [2])
        self.assertListEqual(
            perceptrons_details, [(identity, [0, 0], [0, 0.000063]), (sigmoid, [0], [0]), (relu, [1], [16.811015])]
        )


class TestBuildNeuralNetwork(TestCase):
    def test_build_neural_network_input(self):
        network = build_neural_network(
            [0], [2], [(identity, [0, 0], [0, 0.000063]), (sigmoid, [0], [0]), (relu, [1], [16.811015])]
        )
        self.assertIsInstance(network.input_perceptrons[0], NetworkInput)
        self.assertIs(network.input_perceptrons[0].activation_function, identity)
        self.assertListEqual(network.input_perceptrons[0].weights, [0, 0.000063])

    def test_build_neural_network_output(self):
        network = build_neural_network(
            [0], [2], [(identity, [0, 0], [0, 0.000063]), (sigmoid, [0], [0]), (relu, [1], [16.811015])]
        )
        self.assertIsInstance(network.output_perceptrons[0], Perceptron)
        self.assertIs(network.output_perceptrons[0].activation_function, relu)
        self.assertListEqual(network.output_perceptrons[0].weights, [16.811015])

    def test_build_neural_network_hidden_perceptrons(self):
        network = build_neural_network(
            [0],
            [3],
            [(identity, [0, 0], [0, 0.000063]), (sigmoid, [0], [0]), (relu, [1], [0.42]), (relu, [1], [16.811015])],
        )
        self.assertIsInstance(network.hidden_perceptrons[0], Perceptron)
        self.assertIs(network.hidden_perceptrons[0].activation_function, sigmoid)
        self.assertListEqual(network.hidden_perceptrons[0].weights, [0])

        self.assertIsInstance(network.hidden_perceptrons[1], Perceptron)
        self.assertIs(network.hidden_perceptrons[1].activation_function, relu)
        self.assertListEqual(network.hidden_perceptrons[1].weights, [0.42])

    def test_build_neural_network_input_number(self):
        network = build_neural_network(
            *read(*parse("".join([str(random.randint(0, 1)) for _ in range(random.randint(49, 5000))]), 5, 1))
        )
        self.assertEqual(len(network.input_perceptrons), 5)
