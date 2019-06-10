from deap import creator, base, tools

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


def calculate(storage_input: StorageInput):

    toolbox = initialize_toolbox(storage_input)

    # population
    pop = toolbox.population(n=300)
    print(pop)

    # Evaluate the entire population
    # fitnesses = list(map(toolbox.evaluate, pop))
    # for ind, fit in zip(pop, fitnesses):
    #     ind.fitness.values = fit
    #
    # # CXPB  is the probability with which two individuals
    # #       are crossed
    # #
    # # MUTPB is the probability for mutating an individual
    # CXPB, MUTPB = 0.5, 0.2
    #
    # # Extracting all the fitnesses of
    # fits = [ind.fitness.values[0] for ind in pop]
    #
    # # Variable keeping track of the number of generations
    # g = 0
    #
    # # Begin the evolution
    # while max(fits) < 100 and g < 1000:
    #     # A new generation
    #     g = g + 1
    #     print("-- Generation %i --" % g)
    #
    #     # Select the next generation individuals
    #     offspring = toolbox.select(pop, len(pop))
    #     # Clone the selected individuals
    #     offspring = list(map(toolbox.clone, offspring))
    #
    #     # Apply crossover and mutation on the offspring
    #     for child1, child2 in zip(offspring[::2], offspring[1::2]):
    #         if random.random() < CXPB:
    #             toolbox.mate(child1, child2)
    #             del child1.fitness.values
    #             del child2.fitness.values
    #
    #     for mutant in offspring:
    #         if random.random() < MUTPB:
    #             toolbox.mutate(mutant)
    #             del mutant.fitness.values
    #
    #     # Evaluate the individuals with an invalid fitness
    #     invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    #     fitnesses = map(toolbox.evaluate, invalid_ind)
    #     for ind, fit in zip(invalid_ind, fitnesses):
    #         ind.fitness.values = fit
    #
    #     pop[:] = offspring
    #
    #     # Gather all the fitnesses in one list and print the stats
    #     fits = [ind.fitness.values[0] for ind in pop]
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
    #
    # print(storage_input)

    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
            u'Beiherhund das Oder die Flipperwaldt gersput.')