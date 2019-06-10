from io import TextIOWrapper
from typing import Tuple, Optional

import numpy as np
from pathlib import Path


class StorageInput:

    MIN_SHAPE   = 50
    MAX_SHAPE   = 1024
    MAX_N       = 100
    MIN_BOX     = 5
    MAX_BOX     = 100

    def __init__(self, storage_shape: Tuple[int, int], boxes: np.ndarray):
        self._storage_shape = storage_shape
        self._boxes = boxes

    @property
    def storage_shape(self) -> Tuple[int, int]:
        return self._storage_shape

    @storage_shape.setter
    def storage_shape(self, obj):
        raise PermissionError("Not allowed")

    @property
    def boxes(self) -> np.ndarray:
        return self._boxes

    @boxes.setter
    def boxes(self, obj):
        raise PermissionError("Not allowed")

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
