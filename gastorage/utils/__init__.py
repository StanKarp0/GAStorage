from collections import namedtuple
from io import TextIOWrapper
from typing import Tuple, Optional

import numpy as np
from pathlib import Path


Package = namedtuple('Package', ('rotated', 'position', 'index'))
Rectangle = namedtuple('Rectangle', ('x', 'y', 'w', 'h'))


class StorageInput:

    MIN_SHAPE   = 50
    MAX_SHAPE   = 1024
    MAX_N       = 100
    MIN_BOX     = 5
    MAX_BOX     = 100

    def __init__(self, storage_shape: Tuple[int, int], boxes: np.ndarray):
        self._storage_shape = storage_shape
        self._boxes = boxes
        self._packages_surface = (boxes[:, 0] * boxes[:, 1]).sum()

    @property
    def storage_shape(self) -> Tuple[int, int]:
        return self._storage_shape

    @property
    def height(self) -> int:
        return self._storage_shape[1]

    @property
    def width(self) -> int:
        return self._storage_shape[0]

    @property
    def boxes(self) -> np.ndarray:
        return self._boxes

    @property
    def count(self) -> int:
        return self._boxes.shape[0]

    @property
    def packages_surface(self) -> int:
        return self._packages_surface

    def __str__(self):
        return f"Shape: {self._storage_shape}\nBoxes:\n{self._boxes}"

    @classmethod
    def from_random(cls, storage_shape: Tuple[int, int], boxes: int):
        """
        Zakładamy, że N będzie niewiększe niż 100, Woraz Lmogą się zmieniać między 50 a 1024, natomiast w_ioraz l_i
        mogą się zmieniać między 5 a 100. Pozycje skrzynek, określane przez położenie lewego górnego narożnika,
        mogą przyjmować wyłącznie wartości całkowite. Również długości i szerokości skrzynek mogą być wyłącznie
        całkowite. Lewy górny narożnik ma pozycję (0,0).
        :param storage_shape:
        :param boxes:
        :return:
        """
        boxes = np.random.randint(StorageInput.MIN_BOX, StorageInput.MAX_BOX, size=(boxes, 2))
        return cls(storage_shape, boxes)

    @staticmethod
    def storage_generator():
        while True:
            shape = np.random.randint(StorageInput.MIN_SHAPE, StorageInput.MAX_SHAPE, size=(2,))
            shape = tuple(shape[:2])
            n = np.random.randint(StorageInput.MAX_N)
            yield StorageInput.from_random(shape, n)


class OpenStorage:

    def __init__(self, path: Path):
        self.__path: Path = path
        self.__file: Optional[TextIOWrapper] = None

    def __enter__(self):
        self.__file = self.__path.open('r')
        lines = self.__file.readlines()
        nmbrs = [[int(nmb) for nmb in line.strip().split(' ')] for line in lines]
        shape = tuple(nmbrs[0])[:2]
        boxes = np.array(nmbrs[2:])
        return StorageInput(shape, boxes)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__file and self.__file.close()
