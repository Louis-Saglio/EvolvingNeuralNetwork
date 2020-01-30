from __future__ import annotations

import os
from random import randint, choices, random
from statistics import mean

from encoding import build_neural_network_from_binary_string


class Problem:
    def get_answer_accuracy(self, individual: Individual) -> float:
        raise NotImplementedError


class Individual:
    def __init__(self, genome: str):
        self.genome = genome
        self.network = build_neural_network_from_binary_string(genome, 2, 1)

    def score(self, problem, precision: int = 10) -> float:
        score = 0
        for _ in range(precision):
            score += problem.get_answer_accuracy(self)
        return score / (precision * len(self.genome))

    def mate(self, partner: Individual) -> Individual:
        return Individual(
            "".join(
                str(int(int(gene_self) + int(gene_other) == 1))
                for gene_self, gene_other in zip(self.genome, partner.genome)
            )
        )

    def mutate(self) -> Individual:
        seed = random()
        if seed < 0.8:
            new_genome = list(self.genome)
            index_of_mutated_gene = randint(0, len(new_genome) - 1)
            new_genome[index_of_mutated_gene] = str(int(not bool(int(new_genome[index_of_mutated_gene]))))
            self.genome = "".join(new_genome)
        elif seed < 0.9:
            self.genome += str(randint(0, 1))
        else:
            self.genome = self.genome[:-1]
        self.network = build_neural_network_from_binary_string(self.genome, 2, 1)
        return self


def main():
    population_size = 100
    population = [
        Individual(
            # "000001"
            # "000010"
            # "000000"
            # "000010"
            # "000010"
            # "000001"
            # # Perceptron 0
            # "000010"
            # "0000"
            # # Weights
            # "000000"
            # "00000011111111111111111100"
            # "000000"
            # "00000000000000000000000000"
            # # Perceptron 1
            # "000000"
            # "0000"
            # # Weights
            # "000000"
            # "000000000000000000"
            "01010101010101010101"
        )
        for _ in range(population_size)
    ]

    class Sum(Problem):
        def get_answer_accuracy(self, individual: Individual) -> float:
            numbers = [randint(1, 20), randint(1, 20)]
            return int(round(individual.network.feedforward(numbers)[0], 0) == sum(numbers))

    problem = Sum()

    while True:
        try:
            best: Individual = max(population, key=lambda x: x.score(problem))
            with open("nn.dot", "w") as f:
                f.write(best.network.write_as_graphviz())
            os.system("dot -Tpng nn.dot -o neural_network.png")
            biased_scores = [individual.score(problem) ** 10 for individual in population]
            population = [
                father.mate(mother)
                for father, mother in zip(
                    choices(population, weights=biased_scores, k=population_size),
                    choices(population, weights=biased_scores, k=population_size),
                )
            ]
            [mutant.mutate() for mutant in choices(population, k=population_size // 20)]
            print(
                max([individual.score(problem) for individual in population]),
                round(mean([individual.score(problem) for individual in population]), 2),
            )
        except KeyboardInterrupt:
            # breakpoint()
            break


if __name__ == "__main__":
    main()
