from __future__ import annotations

import math
import os
from random import choices, random
from typing import Union, Callable, List

Number = Union[int, float]


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class Perceptron:
    def __init__(self, activation_function: Callable[[Number], Number], inputs: List[Perceptron]):
        self.inputs = inputs
        self.activation_function = activation_function
        self.current_value: Number = 0
        self.old_value: Number = 0
        self.weights: List[Number] = [random() for _ in self.inputs]
        self.formula = "0"

    def run(self):
        self.current_value = self.activation_function(
            sum([i.output_value * weight for i, weight in zip(self.inputs, self.weights)])
        )

    def update(self):
        self.old_value = self.current_value

    @property
    def id(self):
        return str(id(self))[-5:]

    def add_as_input(self, perceptron: Perceptron, weight: Number):
        self.weights.append(weight)
        self.inputs.append(perceptron)

    def __repr__(self):
        return (
            f"P(id={self.id}, current_value={self.current_value}, old_value={self.old_value},"
            f" weights={[round(w, 2) for w in self.weights]}, {[i.id for i in self.inputs]})"
        )

    @property
    def output_value(self) -> Number:
        return self.old_value


class NetworkInput(Perceptron):
    def run(self):
        pass

    def read(self, value: Number):
        self.current_value = value


class Network:
    def __init__(self, input_perceptrons: List[NetworkInput], computing_perceptrons: List[Perceptron]):
        self.input_perceptrons = input_perceptrons
        self.computing_perceptrons = computing_perceptrons

    @property
    def perceptrons(self) -> List[Perceptron]:
        self.input_perceptrons: List[Perceptron]
        return self.input_perceptrons + self.computing_perceptrons

    @classmethod
    def build_random(cls, nbr: int, nbr_inputs: int, initial_input_nbr: int) -> Network:
        computing_perceptrons = [Perceptron(lambda x: x, []) for _ in range(nbr)]
        input_perceptrons = [NetworkInput(lambda x: x, []) for _ in range(nbr_inputs)]
        perceptrons = computing_perceptrons + input_perceptrons
        for perceptron in computing_perceptrons:
            for new_input in [p for p in choices(perceptrons, k=initial_input_nbr) if p is not perceptron]:
                perceptron.add_as_input(new_input, random())
        return cls(input_perceptrons, computing_perceptrons)

    def feedforward(self, inputs: List[Number]):
        for i, input_value in enumerate(inputs):
            self.input_perceptrons[i].read(input_value)
        for perceptron in self.perceptrons:
            perceptron.run()
        for perceptron in self.perceptrons:
            perceptron.update()

    def write_as_graphviz(self) -> str:
        text = ["digraph {"]
        for perceptron in self.perceptrons:
            text.append(f'"{perceptron.id}" [label="{round(perceptron.current_value, 2)}"]')
            for input_, weight in zip(perceptron.inputs, perceptron.weights):
                text.append(f'"{input_.id}" -> "{perceptron.id}" [label="{round(weight, 2)}"]')
        text.append("}")
        return "\n".join(text)


if __name__ == "__main__":
    network = Network.build_random(5, 2, 2)
    while True:
        network.feedforward([random(), random()])
        with open("nn.dot", "w") as f:
            f.write(network.write_as_graphviz())
        os.system("dot -Tpng nn.dot -o neural_network.png")
        input(">>>")
