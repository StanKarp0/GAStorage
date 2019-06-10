import argparse
from pathlib import Path

from . import algorithm
from .utils import OpenStorage


def main():
    parser = argparse.ArgumentParser(description='Problem Magazynowy. \nImplementacja: Wojciech Malarski')
    parser.add_argument('path', type=str, help='path to input file')
    args = parser.parse_args()

    path = Path(args.path)
    with OpenStorage(path) as storage:
        result = algorithm.calculate(storage)
        print(result)