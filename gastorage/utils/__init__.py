from io import TextIOWrapper
from typing import Tuple, Optional

import numpy as np
from pathlib import Path


class StorageInput:

    def __init__(self, box_shape: Tuple[int, int], boxes: np.ndarray):
        self._box_shape = box_shape
        self._boxes = boxes

    @property
    def box_shape(self) -> Tuple[int, int]:
        return self._box_shape

    @box_shape.setter
    def box_shape(self, obj):
        raise PermissionError("Not allowed")

    @property
    def boxes(self) -> np.ndarray:
        return self._boxes

    @boxes.setter
    def boxes(self, obj):
        raise PermissionError("Not allowed")

    def __str__(self):
        return f"Shape: {self._box_shape}\nBoxes:\n{self._boxes}"


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
