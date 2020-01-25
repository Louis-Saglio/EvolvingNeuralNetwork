from unittest import TestCase
from unittest.mock import patch

from genetic_algorithm import Individual


class TestIndividual(TestCase):
    def test_score(self):
        self.fail()

    def test_mate(self):
        self.fail()

    def test_mutate(self):
        with patch("genetic_algorithm.build_neural_network_from_binary_string"):
            individual = Individual("000000")
        individual.mutate()
        self.assertIn("1", individual.genome)
