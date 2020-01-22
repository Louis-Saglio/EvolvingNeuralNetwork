from unittest import TestCase
from unittest.mock import MagicMock

from neural_network import Perceptron, NetworkInput


class TestPerceptron(TestCase):
    def test_run(self):
        perceptron = Perceptron(lambda x: 2 * x, [MagicMock(output_value=7), MagicMock(output_value=-2)], [3, 0.3])
        perceptron.run()
        self.assertEqual(perceptron.current_value, 2 * (7 * 3 + -2 * 0.3))

    def test_update(self):
        # noinspection PyTypeChecker
        perceptron = Perceptron(None, None, None)
        perceptron.current_value = 42
        perceptron.update()
        self.assertEqual(perceptron.old_value, 42)

    def test_id(self):
        # noinspection PyTypeChecker
        perceptron = Perceptron(None, None, None)
        # noinspection PyTypeChecker
        other_perceptron = Perceptron(None, None, None)
        self.assertEqual(perceptron.id, perceptron.id)
        self.assertNotEqual(perceptron.id, other_perceptron.id)

    def test_add_as_input(self):
        # noinspection PyTypeChecker
        perceptron = Perceptron(None, [0], ["a"])
        # noinspection PyTypeChecker
        perceptron.add_as_input(1, "b")
        self.assertListEqual(perceptron.inputs, [0, 1])
        self.assertListEqual(perceptron.weights, ["a", "b"])

    def test_output_value(self):
        # noinspection PyTypeChecker
        perceptron = Perceptron(None, None, None)
        perceptron.old_value = 42
        self.assertEqual(perceptron.output_value, 42)


class TestNetworkInput(TestCase):
    def test_run(self):
        perceptron = NetworkInput(lambda x: 2 * x, [MagicMock(output_value=7)], [3])
        perceptron.current_value = 42
        perceptron.run()
        self.assertEqual(perceptron.current_value, 42)

    def test_read(self):
        perceptron = NetworkInput(lambda x: 2 * x, [MagicMock(output_value=7)], [3])
        perceptron.read(42)
        self.assertEqual(perceptron.current_value, 42)
