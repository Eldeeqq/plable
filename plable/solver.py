import copy
from typing import Union
import numpy as np

from deap import algorithms, base, creator, tools


def generate(counters):
    vector = []
    for course in counters.keys():
        for cnt in counters[course].values():
            if cnt == 0:
                vector.append(0)
            vector.append(np.random.randint(0, cnt))
    return vector


def decode(sample, parallels):
    vector = []
    index = 0
    for course in parallels.keys():
        for type in parallels[course].values():
            vector.append(type[sample[index]])
            index += 1
    return vector


def mutate(parallel_counters: dict[str, dict[str, int]], sample: list[int], probability=0.5) -> list[int]:
    index = 0
    clone = copy.deepcopy(sample)

    for parallel in parallel_counters.values():
        for count in parallel.values():
            if np.random.randint(0, 1) < probability:
                clone[index] += np.random.randint(0, count) if count > 0 else 0
                clone[index] %= count
            index += 1

    return (clone,)


def crossover(left, right, probability=0.5) -> Union[list[int], list[int]]:
    assert len(left) == len(right)
    for i in range(len(left)):
        if np.random.randint(0, 1) < probability:
            left[i], right[i] = right[i], left[i]
    return left, right


def solve(parallels, counters, fitness, weights):

    creator.create("FitnessMax", base.Fitness, weights=weights)
    creator.create("Individual", list, fitness=creator.FitnessMax)
    tb = base.Toolbox()

    tb.register("create", generate, counters)
    tb.register("individual", tools.initIterate, creator.Individual, tb.create)
    tb.register("population", tools.initRepeat, list, tb.individual)

    tb.register("evaluate", fitness)
    tb.register("mate", tools.cxUniform, indpb=0.2)
    tb.register("mutate", mutate, counters, probability=0.7)
    tb.register("select", tools.selRoulette)

    pop = tb.population(n=100)

    hof = tools.HallOfFame(10)  # hall of fame

    res = algorithms.eaSimple(pop, tb, cxpb=0.3, mutpb=0.5, ngen=20, halloffame=hof)
    return hof
