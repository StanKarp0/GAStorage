import itertools
from unittest import TestCase
import numpy as np

from gastorage import algorithm, operators_tetris
from gastorage.utils import StorageInput, visualize


class AlgorithmStorage(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        generator = StorageInput.storage_generator()
        cls._storage = next(generator)
        cls._toolbox = algorithm.initialize_toolbox_tetris(cls._storage)

    def test_eval(self):
        storage_cnt = 5000
        individuals = 10

        for storage_ind, storage in enumerate(itertools.islice(StorageInput.storage_generator(), storage_cnt)):
            print(storage_ind)
            pop = [operators_tetris.generate_individual(storage) for _ in range(individuals)]
            for i, individual in enumerate(pop):
                added, left, rectangles = operators_tetris.calculate_positions(individual, storage)
                no_overlaps = operators_tetris.no_overlaps_ratio(np.array(rectangles))
                self.assertAlmostEqual(no_overlaps, 1.)
