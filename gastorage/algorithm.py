from functools import partial

import numpy as np
from deap import creator, base, tools, algorithms

from . import operators
from .utils import StorageInput


def initialize_toolbox(storage: StorageInput, *, tournsize, mutpb):
    # creator
    creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

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


def calculate(storage_input: StorageInput, *, ngen: int = 100, pop: int = 100,
              cxpb: float = 0.2, mutpb: float = 0.01, tournsize: int = 3):

    toolbox = initialize_toolbox(storage_input, tournsize=tournsize, mutpb=mutpb)

    # population
    pop = toolbox.population(n=pop)

    statistic = tools.Statistics()
    statistic.register("mean", np.mean)
    statistic.register("max", np.max)
    statistic.register("min", np.min)

    results, log = algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen, statistic)

    individual = max(results, key=lambda ind: sum(ind.fitness.wvalues))

    return individual, log
