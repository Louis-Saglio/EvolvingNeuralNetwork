from __future__ import annotations

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
        return score / precision

    def mate(self, partner: Individual) -> Individual:
        return Individual(
            "".join(
                str(int(int(gene_self) + int(gene_other) == 1))
                for gene_self, gene_other in zip(self.genome, partner.genome)
            )
        )

    def mutate(self) -> Individual:
        new_genome = list(self.genome)
        index_of_mutated_gene = randint(0, len(new_genome) - 1)
        new_genome[index_of_mutated_gene] = str(int(not bool(int(new_genome[index_of_mutated_gene]))))
        self.genome = "".join(new_genome)
        return self


def main():
    population_size = 100
    population = [
        Individual(
            "000001"
            "000010"
            "000000"
            "000010"
            "000010"
            "000001"
            # Perceptron 0
            "000010"
            "0000"
            # Weights
            "000000"
            "00000011111111111111111100"
            "000000"
            "00000000000000000000000000"
            # Perceptron 1
            "000000"
            "0000"
            # Weights
            "000000"
            "000000000000000000"
        )
        for _ in range(population_size)
    ]

    class Sum(Problem):
        def get_answer_accuracy(self, individual: Individual) -> float:
            numbers = [randint(1, 20), randint(1, 20)]
            return int(round(individual.network.feedforward(numbers)[0], 2) == sum(numbers))

    problem = Sum()

    while True:
        try:
            biased_scores = [individual.score(problem) ** 10 for individual in population]
            population = [
                father.mate(mother).mutate() if random() < 0.1 else father.mate(mother)
                for father, mother in zip(
                    choices(population, weights=biased_scores, k=population_size),
                    choices(population, weights=biased_scores, k=population_size),
                )
            ]
            print(
                max([individual.score(problem) for individual in population]),
                round(mean([individual.score(problem) for individual in population]), 2),
            )
        except KeyboardInterrupt:
            breakpoint()
            break


if __name__ == "__main__":
    main()
