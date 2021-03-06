import math


def identity(x):
    return x


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def relu(x):
    return max(0, x)
