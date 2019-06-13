import itertools
from unittest import TestCase

import numpy as np

from gastorage import algorithm, operators
from gastorage.utils import StorageInput, visualize


class AlgorithmStorage(TestCase):

    def test_random(self):
        for storage in itertools.islice(StorageInput.storage_generator(), 10):
            result, evolution = algorithm.calculate(storage, ngen=50, pop=20, mutpb=0.01)
            added_recs, not_added_recs, rectangles = operators.calculate_positions(result, storage)
            print(len(added_recs), len(not_added_recs), storage.count)
            visualize.plot_rectangles(rectangles, storage)

    def test_vis(self):
        storage = next(StorageInput.storage_generator())
        toolbox = algorithm.initialize_toolbox(storage, tournsize=3, mutpb=0.01)
        pop = toolbox.population(n=1)[0]
        visualize.plot_rectangles(pop, storage)