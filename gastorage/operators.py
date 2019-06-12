import random
import numpy as np
import pandas as pd
from deap import tools

from .utils import StorageInput, Box


def init_box(storage: StorageInput) -> Box:
    """
    Function generates random box using storage config info.
    :param storage:
    :return:
    """
    return Box(random.randint(0, 1),
               random.randint(0, 1),
               random.randint(0, storage.height),
               random.randint(0, storage.width))


def no_overlaps_ratio(df: pd.DataFrame) -> float:
    """
    Function calculates ratio of overlapping boxes over all boxes.
    :param df:
    :return:
    """
    assert all([key in df for key in ['yA', 'yB', 'xA', 'xB']])

    df = df.copy()
    df['join'] = 1
    df = df.reset_index()
    pairs = pd.merge(df, df, on='join', suffixes=('_1', '_2'))
    pairs = pairs[pairs.index_1 != pairs.index_2]
    # series = pd.Series((pairs.yA_2 >= pairs.yB_1) |
    #                  (pairs.yA_1 >= pairs.yB_2) |
    #                  (pairs.xA_2 >= pairs.xB_1) |
    #                  (pairs.xA_1 >= pairs.xB_2))
    series = pd.Series((pairs.yA_2 >= pairs.yB_1) | (pairs.xA_2 >= pairs.xB_1))
    return series.mean()


def eval_individual(individual, storage: StorageInput):
    """

    :param individual:
    :param storage:
    :return:
    """
    inv_arr = np.array(individual)
    exist = inv_arr[:, 1] == 1

    # filer existing boxes
    boxes = storage.boxes[exist]
    inv_arr = inv_arr[exist]

    # rotate boxes
    storage_range = np.arange(boxes.shape[0])
    rotated = np.array((boxes[storage_range, inv_arr[:, 0]], boxes[storage_range, ~inv_arr[:, 0]])).T
    stacked = np.column_stack((inv_arr[:, 2:], inv_arr[:, 2:] + rotated))
    df = pd.DataFrame(stacked, columns=['xA', 'yA', 'xB', 'yB'])

    # no overlaps
    no_overlaps = no_overlaps_ratio(df)

    # results
    surface = (rotated[:, 0] * rotated[:, 1]).sum() * no_overlaps
    count = df.shape[0]

    # database like join
    return surface, count


def cx_individual(ind1, ind2, alpha: float, indpb: float):
    """

    :param ind1:
    :param ind2:
    :param alpha:
    :param indpb:
    :return:
    """
    rotate, exist, x, y = [[list(b) for b in a] for a in zip(zip(*ind1), zip(*ind2))]

    tools.cxUniform(*rotate, indpb)
    tools.cxUniform(*exist, indpb)

    tools.cxBlend(*x, alpha)
    tools.cxBlend(*y, alpha)

    x, y = [[int(v + 0.5) for v in ind] for ind in x], [[int(v + 0.5) for v in ind] for ind in y]
    ind1[:] = [Box(*args) for args in zip(rotate[0], exist[0], x[0], y[0])]
    ind2[:] = [Box(*args) for args in zip(rotate[1], exist[1], x[1], y[1])]

    return ind1, ind2


def mut_individual(individual, indpb: float, eta: float, storage: StorageInput):
    """

    :param individual:
    :param indpb:
    :param eta:
    :param storage:
    :return:
    """
    rotate, exist, x, y = [list(var) for var in zip(*individual)]

    tools.mutFlipBit(rotate, indpb)
    tools.mutFlipBit(exist, indpb)

    tools.mutPolynomialBounded(x, eta, 0, storage.width, indpb)
    tools.mutPolynomialBounded(y, eta, 0, storage.height, indpb)

    # print(any([np.isnan(a) for a in x]), any([np.isnan(a) for a in y]), storage.storage_shape)
    # print(x)
    # print(y)
    x = [int(v + 0.5) if not np.isnan(v) else storage.height for v in x]
    y = [int(v + 0.5) if not np.isnan(v) else storage.width for v in y]
    individual[:] = [Box(*args) for args in zip(rotate, exist, x, y)]

    return individual,
