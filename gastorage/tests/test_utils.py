import numpy as np
from unittest import TestCase

from gastorage import algorithm
from gastorage.tests import tests_path
from gastorage.utils import OpenStorage, StorageInput


class TestFileStorage(TestCase):

    def assertValidStorage(self, storage: StorageInput):
        self.assertIsInstance(storage, StorageInput)
        self.assertLess(storage.boxes.max(), StorageInput.MAX_BOX)
        self.assertGreaterEqual(storage.boxes.min(), StorageInput.MIN_BOX)

    def test_from_file(self):

        path = tests_path / "data"
        for file_path in path.rglob("*"):
            with OpenStorage(file_path) as storage:
                self.assertValidStorage(storage)

    def test_from_random(self):
        """
        Zakładamy, że N będzie niewiększe niż 100, Woraz Lmogą się zmieniać między 50 a 1024, natomiast w_ioraz l_i
        mogą się zmieniać między 5 a 100. Pozycje skrzynek, określane przez położenie lewego górnego narożnika,
        mogą przyjmować wyłącznie wartości całkowite. Również długości i szerokości skrzynek mogą być wyłącznie
        całkowite. Lewy górny narożnik ma pozycję (0,0).
        """
        test_num = 1
        shapes = np.random.randint(StorageInput.MIN_SHAPE, StorageInput.MAX_SHAPE, size=(test_num, 2))
        boxes = np.random.randint(StorageInput.MAX_N, size=(test_num,))
        for shape, n in zip(shapes, boxes):
            shape = tuple(shape[:2])
            storage = StorageInput.from_random(shape, n)

            self.assertValidStorage(storage)
            self.assertTupleEqual(shape, storage.storage_shape)
            self.assertTupleEqual(storage.boxes.shape, (n, 2))

