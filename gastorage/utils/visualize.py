import random
from typing import List, Optional

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from deap.tools import Logbook

from ..utils import StorageInput, Rectangle

__all__ = ('plot_rectangles', 'plot_evolution', 'get_colors')


def get_colors():
    shift, scale = 0.25, 0.5
    while True:
        base_color = [1 - random.random() * scale,
                      1 - random.random() * scale,
                      1 - random.random() * scale]
        edge_color = [c - shift for c in base_color]
        yield base_color, edge_color


def plot_rectangles(rectangles: List[Rectangle], storage: StorageInput, colors=get_colors()):
    fig, ax = plt.subplots(1, 1)
    ax.set_xlim(0, storage.width)
    ax.set_ylim(0, storage.height)
    ax.set_title('Rozkład skrzyń')
    ax.set_xlabel('w')
    ax.set_ylabel('h')

    for r in rectangles:
        base_color, edge_color = next(colors)
        rect = patches.Rectangle((r.x, r.y), r.w, r.h, linewidth=1, edgecolor=edge_color, facecolor=base_color)
        ax.add_patch(rect)

    plt.tight_layout()

    return fig


def plot_evolution(evolution: Logbook):
    args = ['gen', 'max', 'mean', 'surface', 'count']
    ev_it, ev_max, ev_mean, ev_surface, ev_count = evolution.select(*args)

    ev_online = np.array(ev_mean).cumsum() / np.arange(1, len(ev_mean) + 1)
    ev_offline = np.array(ev_max).cumsum() / np.arange(1, len(ev_max) + 1)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex='all', figsize=(12, 4))

    # zbieznosc
    ax1.plot(ev_it, ev_max, label='max')
    ax1.plot(ev_it, ev_mean, label='mean')
    ax1.plot(ev_it, ev_offline, label='offline')
    ax1.plot(ev_it, ev_online, label='online')
    ax1.set_title('Zbieżność algorytmu')
    ax1.set_xlabel('Iteracja')
    ax1.set_ylabel('Przystosowanie')
    ax1.grid()
    ax1.legend()

    # surface
    ax2.plot(ev_it, np.array(ev_surface))
    ax2.set_title('Suma powierchni najlepszego osobnika')
    ax2.set_xlabel('Iteracja')
    ax2.set_ylabel('Powierzchnia')
    ax2.grid()

    # count
    ax3.plot(ev_it, ev_count)
    ax3.set_title('Liczba skrzyń najlepszego osobnika')
    ax3.set_xlabel('Iteracja')
    ax3.set_ylabel('Liczba skrzyń')
    ax3.grid()

    plt.tight_layout()

    return fig