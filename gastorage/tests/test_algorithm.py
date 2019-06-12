import itertools
from unittest import TestCase

from gastorage import algorithm
from gastorage.utils import StorageInput, visualize


class AlgorithmStorage(TestCase):

    def test_random(self):
        for storage in itertools.islice(StorageInput.storage_generator(), 1):
            result, evolution = algorithm.calculate(storage, eta=1.)
            visualize.plot_boxes(result, storage)

    def test_vis(self):
        storage = next(StorageInput.storage_generator())
        toolbox = algorithm.initialize_toolbox(storage)
        pop = toolbox.population(n=1)[0]
        visualize.plot_boxes(pop, storage)