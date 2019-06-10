import numpy as np
from unittest import TestCase

from gastorage import algorithm
from gastorage.utils import StorageInput


class AlgorithmStorage(TestCase):

    def test_random(self):
        test_num = 1
        shapes = np.random.randint(StorageInput.MIN_SHAPE, StorageInput.MAX_SHAPE, size=(test_num, 2))
        boxes = np.random.randint(StorageInput.MAX_N, size=(test_num,))
        for shape, n in zip(shapes, boxes):
            shape = tuple(shape[:2])
            storage = StorageInput.from_random(shape, n)
            result = algorithm.calculate(storage)