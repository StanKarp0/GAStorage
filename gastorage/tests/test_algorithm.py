import itertools
import pickle
import random
from unittest import TestCase

import matplotlib.pyplot as plt

from gastorage import algorithm, operators
from gastorage.tests import tests_path
from gastorage.utils import StorageInput, visualize, OpenStorage


class AlgorithmStorage(TestCase):

    def test_random(self):
        algorithm.initialize_creator()
        generator = (storage for storage in StorageInput.storage_generator()
                     if storage.packages_surface > storage.height * storage.width and abs(storage.width - storage.height) < 50)

        data_path = tests_path / 'data'
        name = 'param_%d.txt'
        max_file = 10000

        for storage in itertools.islice(generator, 1):
            individual, evolution = algorithm.calculate(storage, ngen=5000, pop=20, mutpb=0.2, best=3, cxpb=0.5)
            algorithm.to_output_format(individual, storage)
            added_recs, not_added_recs, rectangles = operators.calculate_positions(individual, storage)

            with (data_path / (name % random.randint(0, max_file))).open('w') as file:
                file.write(storage.as_input())

            fig = visualize.plot_rectangles(rectangles, storage)
            plt.show()
            plt.close(fig)
            fig = visualize.plot_evolution(evolution)
            plt.show()
            plt.close(fig)

    # def test_algorithm_from_file(self):
    #     algorithm.initialize_creator()
    #
    #     file_path = tests_path / "data" / "param_5121.txt"
    #     results = {}
    #     with OpenStorage(file_path) as storage:
    #         for mutpb in [0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.025, 0.01]:
    #             for cxpb in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]:
    #                 for t in range(10):
    #                     print((mutpb, cxpb, t))
    #                     individual, evolution = algorithm.calculate(storage, ngen=500, pop=20, mutpb=mutpb, best=5,
    #                                                                 cxpb=cxpb)
    #                     results[(mutpb, cxpb, t)] = evolution[-1]
    #
    #     result_pickle = tests_path / "data" / "result.pickle"
    #     with result_pickle.open('wb') as file:
    #         pickle.dump(results, file)