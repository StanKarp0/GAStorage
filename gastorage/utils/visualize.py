from typing import List, Optional

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from ..utils import Box, StorageInput, Rectangle

__all__ = ('plot_boxes', 'plot_rectangles')


def plot_boxes(boxes: List[Box], storage: StorageInput):

    fig, ax = plt.subplots(1, 1)
    ax.set_xlim(0, storage.width)
    ax.set_ylim(0, storage.height)

    for box, (width, height) in zip(boxes, storage.boxes):
        rect = patches.Rectangle((box.x, box.y), width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    plt.show()


def plot_rectangles(rectangles: List[Rectangle], storage: StorageInput, *, filename: Optional[str]=None):

    fig, ax = plt.subplots(1, 1)
    ax.set_xlim(0, storage.width)
    ax.set_ylim(0, storage.height)

    for r in rectangles:
        rect = patches.Rectangle((r.x, r.y), r.w, r.h, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    if filename is not None:
        plt.savefig(filename)
    # else:
    plt.show()