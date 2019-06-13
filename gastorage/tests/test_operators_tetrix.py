from unittest import TestCase

from gastorage import algorithm, operators_tetris
from gastorage.utils import StorageInput, visualize


class AlgorithmStorage(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        generator = StorageInput.storage_generator()
        cls._storage = next(generator)
        cls._toolbox = algorithm.initialize_toolbox_tetris(cls._storage)

    def test_eval(self):
        pop = self._toolbox.population(n=1)
        boxes = operators_tetris.calculate_positions(pop[0], self._storage)
        visualize.plot_rectangles(boxes, self._storage)
