import itertools
from unittest import TestCase

import numpy as np
import matplotlib.pyplot as plt

from gastorage import algorithm, operators
from gastorage.utils import StorageInput, visualize


class AlgorithmStorage(TestCase):

    def test_random(self):
        algorithm.initialize_creator()
        generator = (storage for storage in StorageInput.storage_generator()
                     if storage.packages_surface > storage.height * storage.width)

        for storage in itertools.islice(generator, 1):
            individual, evolution = algorithm.calculate(storage, ngen=1000, pop=20, mutpb=0.1, best=5)
            algorithm.to_output_format(individual, storage)
            added_recs, not_added_recs, rectangles = operators.calculate_positions(individual, storage)

            visualize.plot_rectangles(rectangles, storage)
            plt.show()
            visualize.plot_evolution(evolution)
            plt.show()

    def test_vis(self):
        algorithm.initialize_creator()

        storage = next(StorageInput.storage_generator())
        toolbox = algorithm.initialize_toolbox(storage, tournsize=3, mutpb=0.01)

        pop = toolbox.population(n=1)[0]
        visualize.plot_rectangles(pop, storage)