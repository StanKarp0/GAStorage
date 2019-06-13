import random

from .utils import StorageInput, Rect, Rectangle
from .utils.visualize import plot_rectangles, Box


def init_box(position: int):
    return Rect(rotated=random.randint(0, 1),
                exist=random.randint(0, 1),
                position=position)


def generate_individual(storage: StorageInput):
    return [init_box(i) for i in random.sample(range(storage.count), storage.count)]


def calculate_positions(individual, storage: StorageInput):
    rects = sorted(zip(individual, storage.boxes), key=lambda r: r[0].position)
    shapes = [arr[::-1 if rect.rotated else 1] for rect, arr in rects]

    points = [(0, 0, storage.width, storage.height)]
    boxes = []
    for shape_ind, shape in enumerate(shapes):
        # print(shape_ind, 'Shape:', shape)
        points_ind = 0
        point_to_remove = None
        points_to_add = []

        while points_ind < len(points) and point_to_remove is None:
            x, y, width, height = points[points_ind]
            # print('Try: ', 'x:', x, ', y:', y, ', w:', width, ', h:', height)
            if shape[0] <= width and shape[1] <= height:
                box = Rectangle(x, y, shape[0], shape[1])
                boxes.append(box)
                plot_rectangles(boxes, storage, filename=f'shapes_{shape_ind}.png')

                new_x = x + shape[0]
                new_y = y + shape[1]

                point_to_remove = points_ind
                # print(box)

                for i, (px, py, pw, ph) in enumerate(points):
                    if y < py < new_y and px < x < px + pw:
                        points[i] = (px, py, x - px, ph)

                for i, (px, py, pw, ph) in enumerate(points):
                    if x < px < new_x and py < y < py + ph:
                        points[i] = (px, py, pw, y - py)

                if shape[0] < width:
                    points_to_add.append((new_x, y, width - shape[0], height))

                if shape[1] < height:
                    points_to_add.append((x, new_y, width, height - shape[1]))

            points_ind += 1

        if point_to_remove is not None:
            del points[point_to_remove]
        # print('add: ', points_to_add)
        # print('points:', points)

        points += points_to_add

        # print(boxes)
        # print(points)

    return boxes


def eval_individual(individual, storage: StorageInput):
    positions = calculate_positions(individual, storage)
    return None


def cx_individual():
    return None