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
        individual, log = algorithm.calculate(storage)
        output = algorithm.to_output_format(individual, storage)
        print(output)