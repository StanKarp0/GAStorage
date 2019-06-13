import itertools
from unittest import TestCase
import numpy as np

from gastorage import operators
from gastorage.utils import StorageInput, visualize


class AlgorithmStorage(TestCase):

    @staticmethod
    def generate_population(individuals: int, storage: StorageInput):
        return (operators.generate_individual(storage) for _ in range(individuals))

    def test_tetris(self):
        storage_cnt = 500
        individuals = 10

        for storage in itertools.islice(StorageInput.storage_generator(), storage_cnt):
            for individual in AlgorithmStorage.generate_population(individuals, storage):
                added, left, rectangles = operators.calculate_positions(individual, storage)
                no_overlaps = operators.no_overlaps_ratio(np.array(rectangles))
                self.assertAlmostEqual(no_overlaps, 1.)

    def test_eval(self):
        storage_cnt = 500
        individuals = 10

        for storage in itertools.islice(StorageInput.storage_generator(), storage_cnt):
            for individual in AlgorithmStorage.generate_population(individuals, storage):
                fitness = operators.eval_individual(individual, storage)
                self.assertIsInstance(fitness, tuple)
                self.assertEqual(len(fitness), 2)
                self.assertGreaterEqual(fitness[0], 0)
                self.assertGreaterEqual(fitness[1], 0)

    def test_cx(self):
        storage_cnt = 500
        individuals = 10
        generator = itertools.combinations(range(individuals), 2)

        for storage in itertools.islice(StorageInput.storage_generator(), storage_cnt):
            population = list(AlgorithmStorage.generate_population(individuals, storage))
            generator, local_gen = itertools.tee(generator, 2)

            for a, b in local_gen:
                old_a_arr, old_b_arr = np.array(population[a]), np.array(population[b])
                operators.cx_individual(population[a], population[b])
                new_a_arr, new_b_arr = np.array(population[a]), np.array(population[b])

                if len(population[a]) > 0:
                    self.assertEqual(np.unique(new_a_arr[:, 1]).shape[0], np.unique(old_a_arr[:, 1]).shape[0])
                    self.assertEqual(np.unique(new_b_arr[:, 1]).shape[0], np.unique(old_b_arr[:, 1]).shape[0])

    def test_mut(self):
        storage_cnt = 500
        individuals = 10
        indpb = 0.01

        for storage in itertools.islice(StorageInput.storage_generator(), storage_cnt):
            for individual in AlgorithmStorage.generate_population(individuals, storage):
                mutated = operators.mut_individual(individual, indpb)
