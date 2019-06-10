from unittest import TestCase

from gastorage.tests import tests_path
from gastorage.utils import OpenStorage, StorageInput


class TestFileStorage(TestCase):

    def test_loading(self):

        path = tests_path / "data"
        for file_path in path.rglob("*"):
            with OpenStorage(file_path) as storage:
                self.assertIsInstance(storage, StorageInput)