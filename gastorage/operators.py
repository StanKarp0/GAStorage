import random

from gastorage.utils import StorageInput, Box


def init_box(storage: StorageInput):
    return Box(random.randint(0, 1),
               random.randint(0, 1),
               random.randint(0, storage.height),
               random.randint(0, storage.width))


def eval_individual(individual):
    return sum(individual),


def cx_individual(individual1, individual2):
    return individual1


def mut_individual(individual, indpb):
    return individual
