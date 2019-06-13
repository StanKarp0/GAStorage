from deap import creator, base, tools, algorithms
import numpy as np

from . import operators
from .utils import StorageInput


def initialize_toolbox(storage: StorageInput, *, indpb_mutate: float = 0.05, tournsize: int = 3, eta: float = 4,
                       alpha: float = 0.1, indpb_mate=0.25):
    # The creator is a class factory that can build new classes at run-time.
    # It will be called with first the desired name of the new class,
    # second the base class it will inherit, and in addition any subsequent
    # arguments you want to become attributes of your class. This allows us to
    # build new and complex structures of any type of container from lists to n-ary trees.
    creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # All the objects we will use on our way, an individual, the population,
    # as well as all functions, operators, and arguments will be
    # stored in a DEAP container called Toolbox.
    toolbox = base.Toolbox()

    # Attribute generator
    toolbox.register("attr_box", operators.init_box, storage)

    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_box, n=storage.count)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # parameters
    toolbox.register("evaluate", operators.eval_individual, storage=storage)
    toolbox.register("mate", operators.cx_individual, alpha=alpha, indpb=indpb_mate)
    toolbox.register("mutate", operators.mut_individual, indpb=indpb_mutate, eta=eta, storage=storage)
    toolbox.register("select", tools.selTournament, tournsize=tournsize)

    return toolbox


def calculate(storage_input: StorageInput, *, cxpb: float = 0.2, mutpb: float = 0.02, ngen: int = 100,
              eta: float = 0.2, pop: int = 100):

    toolbox = initialize_toolbox(storage_input, eta=eta)

    # population
    pop = toolbox.population(n=pop)

    statistic = tools.Statistics()
    statistic.register("mean", np.mean)
    statistic.register("max", np.max)
    statistic.register("min", np.min)

    results, log = algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen, statistic)

    individual = max(results, key=lambda ind: sum(ind.fitness.wvalues))

    return individual, log
