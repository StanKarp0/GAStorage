import itertools
from unittest import TestCase

from gastorage import algorithm
from gastorage.utils import StorageInput


class AlgorithmStorage(TestCase):

    def test_random(self):
        for storage in itertools.islice(StorageInput.storage_generator(), 1):
            result = algorithm.calculate(storage)
            print(result)