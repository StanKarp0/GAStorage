import pandas as pd
from unittest import TestCase

from gastorage import algorithm, operators
from gastorage.utils import StorageInput


class AlgorithmStorage(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        generator = StorageInput.storage_generator()
        cls._storage = next(generator)
        cls._toolbox = algorithm.initialize_toolbox(cls._storage)

    def test_eval(self):
        pop = self._toolbox.population(n=10)
        values = [self._toolbox.evaluate(individual) for individual in pop]
        for value in values:
            self.assertIsInstance(value, tuple)

    def test_overlaps(self):
        tests = [
            ([{'xA': 10, 'yA': 10, 'xB': 20, 'yB': 20},
              {'xA': 15, 'yA': 15, 'xB': 25, 'yB': 25}], False),

            ([{'xA': 15, 'yA': 10, 'xB': 20, 'yB': 20},
              {'xA': 10, 'yA': 15, 'xB': 25, 'yB': 25}], False),

            ([{'xA': 10, 'yA': 10, 'xB': 25, 'yB': 20},
              {'xA': 15, 'yA': 15, 'xB': 20, 'yB': 25}], False),

            ([{'xA': 10, 'yA': 15, 'xB': 20, 'yB': 20},
              {'xA': 15, 'yA': 10, 'xB': 25, 'yB': 25}], False),

            ([{'xA': 10, 'yA': 10, 'xB': 20, 'yB': 20},
              {'xA': 15, 'yA': 15, 'xB': 30, 'yB': 30}], False),
        ]

        for dicts, result in tests:
            df = pd.DataFrame(dicts)
            ratio = operators.no_overlaps_ratio(df)
            self.assertEqual(ratio >= 1, result)

    def test_cx(self):
        pop = self._toolbox.population(n=1000)
        pairs = zip(pop, pop[1:])

        for ind1, ind2 in pairs:
            self._toolbox.mate(ind1, ind2)

    def test_mut(self):
        pop = self._toolbox.population(n=1000)

        for ind in pop:
            self._toolbox.mutate(ind)