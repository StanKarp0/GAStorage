import itertools
import random
from typing import Tuple, List

import numpy as np

from .utils import StorageInput, Package, Rectangle


def init_box(position: int, index: int):
    return Package(rotated=random.randint(0, 1),
                   position=position,
                   index=index)


def generate_individual(storage: StorageInput):
    args = zip(range(storage.count), random.sample(range(storage.count), storage.count))
    return [init_box(position, index) for position, index in args]


def no_overlaps_ratio(rectangles: np.ndarray) -> float:
    if rectangles.shape[0] in [0, 1]:
        return 1.

    left, right = zip(*itertools.combinations(range(rectangles.shape[0]), 2))
    rectangles[:, 2:] += rectangles[:, :2]
    # columns: 0:xA_1, 1:yA_1, 2:xB_1, 3:yB_1, 4:xA_2, 5:yA_2, 6:xB_2, 7:yB_2
    pairs = np.concatenate((rectangles[left, :], rectangles[right, :]), axis=1)
    no_overlaps = np.array((pairs[:, 5] >= pairs[:, 3]) |
                           (pairs[:, 1] >= pairs[:, 7]) |
                           (pairs[:, 4] >= pairs[:, 2]) |
                           (pairs[:, 0] >= pairs[:, 6]))
    return no_overlaps.mean()


def calculate_positions(individual, storage: StorageInput) -> Tuple[List[Package], List[Package], List[Rectangle]]:
    recs = sorted(zip(individual, storage.boxes), key=lambda r: r[0].position)
    shapes = [(arr[::-1 if rect.rotated else 1], rect) for rect, arr in recs]

    points = [(0, 0, storage.width, storage.height)]
    added_recs, not_added_recs, rectangles = [], [], []

    # iterating over packages
    for shape_ind, (shape, rect) in enumerate(shapes):
        points_ind = 0
        point_to_remove = None
        points_to_add = []

        while points_ind < len(points) and point_to_remove is None:
            x, y, width, height = points[points_ind]

            if shape[0] <= width and shape[1] <= height:
                box = Rectangle(x, y, shape[0], shape[1])
                rectangles.append(box)
                point_to_remove = points_ind

            points_ind += 1

        if point_to_remove is None:
            not_added_recs.append(rect)

        else:

            x, y, width, height = points[point_to_remove]

            new_x = x + shape[0]
            new_y = y + shape[1]
            for i, (px, py, pw, ph) in enumerate(points):
                if y <= py <= new_y and px <= x <= px + pw:
                    points[i] = (px, py, x - px, ph)

            for i, (px, py, pw, ph) in enumerate(points):
                if x <= px <= new_x and py <= y <= py + ph:
                    points[i] = (px, py, pw, y - py)

            if shape[0] < width:
                points_to_add.append((new_x, y, width - shape[0], height))

            if shape[1] < height:
                points_to_add.append((x, new_y, width, height - shape[1]))

            del points[point_to_remove]
            added_recs.append(rect)

        points += points_to_add

    return added_recs, not_added_recs, rectangles


def eval_individual(individual, storage: StorageInput):
    added_recs, not_added_recs, rectangles = calculate_positions(individual, storage)
    return None


def cx_individual():
    return None