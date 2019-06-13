import itertools
import random
from typing import Tuple, List

import numpy as np
from deap import tools

from .utils import StorageInput, Package, Rectangle, visualize


def init_box(position: int, index: int):
    return Package(rotated=random.randint(0, 1),
                   position=position,
                   index=index)


def generate_individual(storage: StorageInput):
    args = zip(range(storage.count), random.sample(range(storage.count), storage.count))
    return [init_box(position, index) for index, position in args]


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
    if len(individual) < 1:
        return 0, 0

    added_recs, not_added_recs, rectangles = calculate_positions(individual, storage)

    if len(added_recs) < 1:
        return 0, 0

    recs_arr = storage.boxes[np.array(added_recs)[:, 2], :]
    surface = (recs_arr[:, 0] * recs_arr[:, 1]).sum()
    count = len(added_recs)
    return surface, count


def cx_individual(individual1, individual2):
    if len(individual1) < 2:
        return individual1, individual2

    ind_arr1 = np.array(individual1)
    ind_arr2 = np.array(individual2)

    try:
        rotated1, rotated2 = tools.cxTwoPoint(ind_arr1[:, 0].copy(), ind_arr2[:, 0].copy())
        order1, order2 = tools.cxPartialyMatched(ind_arr1[:, 1].copy(), ind_arr2[:, 1].copy())

        for index, position, rotated in zip(ind_arr1[:, 2], order1, rotated1):
            individual1[index] = Package(rotated, position, index)

        for index, position, rotated in zip(ind_arr2[:, 2], order2, rotated2):
            individual2[index] = Package(rotated, position, index)

    except Exception as e:
        raise e

    return individual1, individual2
