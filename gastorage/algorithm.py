from deap import creator, base, tools, algorithms

from . import operators
from .utils import StorageInput


def initialize_toolbox(storage: StorageInput, *, indpb: float=0.05, tournsize: int=3):
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
    toolbox.register("mate", operators.cx_individual, alpha=0.1, indpb=0.25)
    toolbox.register("mutate", operators.mut_individual, indpb=indpb)
    toolbox.register("select", tools.selTournament, tournsize=tournsize)

    return toolbox


def calculate(storage_input: StorageInput, *, cxpb: float = 0.2, mutpb: float = 0.02, ngen: int = 100):

    toolbox = initialize_toolbox(storage_input)

    # population
    pop = toolbox.population(n=50)

    log = algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen)

    #
    #     length = len(pop)
    #     mean = sum(fits) / length
    #     sum2 = sum(x * x for x in fits)
    #     std = abs(sum2 / length - mean ** 2) ** 0.5
    #
    #     print("  Min %s" % min(fits))
    #     print("  Max %s" % max(fits))
    #     print("  Avg %s" % mean)
    #     print("  Std %s" % std)


    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
            u'Beiherhund das Oder die Flipperwaldt gersput.')