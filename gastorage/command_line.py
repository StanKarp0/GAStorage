import argparse
from pathlib import Path

from . import algorithm
from .utils import OpenStorage


__all__ = ()


def main():
    parser = argparse.ArgumentParser(description='Problem Magazynowy. \nImplementacja: Wojciech Malarski')
    parser.add_argument('path', type=str, help='path to input file')
    args = parser.parse_args()

    path = Path(args.path)
    with OpenStorage(path) as storage:
        algorithm.initialize_creator()
        individual, log = algorithm.calculate(storage, verbose=False)
        output = algorithm.to_output_format(individual, storage)

    output_path = Path('output.txt')
    with output_path.open("w") as file:
        file.write(output)