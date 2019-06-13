from functools import partial
from typing import List

import numpy as np
from deap import creator, base, tools, algorithms

from . import operators
from .utils import StorageInput, Package


def initialize_creator():
    # creator
    creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)


def initialize_toolbox(storage: StorageInput, *, tournsize, mutpb):
    # toolbox
    toolbox = base.Toolbox()
    toolbox.register("attr_rect", operators.init_box)
    generator = partial(operators.generate_individual, storage)
    toolbox.register("individual", tools.initIterate, creator.Individual, generator)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # operators
    toolbox.register("evaluate", operators.eval_individual, storage=storage)
    toolbox.register("mate", operators.cx_individual)
    toolbox.register("mutate", operators.mut_individual, indpb=mutpb)
    toolbox.register("select", tools.selTournament, tournsize=tournsize)

    return toolbox


def calculate(storage: StorageInput, *, ngen: int = 100, pop: int = 100,
              cxpb: float = 0.2, mutpb: float = 0.01, tournsize: int = 3, best: int = 3):

    toolbox = initialize_toolbox(storage, tournsize=tournsize, mutpb=mutpb)

    # population
    pop = toolbox.population(n=pop)
    hall_of_fame = tools.HallOfFame(best)

    statistic = tools.Statistics()
    statistic.register("mean", lambda p: np.mean([sum(ind.fitness.wvalues) for ind in p]))
    statistic.register("max", lambda p: np.max([sum(ind.fitness.wvalues) for ind in p]))
    statistic.register("min", lambda p: np.min([sum(ind.fitness.wvalues) for ind in p]))
    statistic.register("surface", lambda p: np.max([ind.fitness.values[0] for ind in p]))
    statistic.register("count", lambda p: np.max([ind.fitness.values[1] for ind in p]))

    results, log = algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen, statistic, hall_of_fame)

    individual = max(results, key=lambda ind: sum(ind.fitness.wvalues))

    return individual, log


def to_output_format(individual, storage: StorageInput):
    # TODO test for this method
    added_recs, not_added_recs, rectangles = operators.calculate_positions(individual, storage)
    included = [(1, r.x, r.y, p.rotated, p.index) for p, r in zip(added_recs, rectangles)]
    excluded = [(0, 0, 0, p.rotated, p.index) for p in not_added_recs]
    sort = sorted(included + excluded, key=lambda t: t[-1])
    print(sort)
    lines = [f'{inc} {storage.boxes[index, 0]} {storage.boxes[index, 1]} {x} {y} {rot}'
             for inc, x, y, rot, index in sort]
    return f'{storage.width} {storage.height}\n{storage.count}\n' + '\n'.join(lines)