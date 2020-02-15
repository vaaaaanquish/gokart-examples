from logging import getLogger
import unittest
from unittest.mock import MagicMock
import gokart
from sample.model.sample import TaskA, TaskB, TaskC

logger = getLogger(__name__)


class TestTaskA(unittest.TestCase):
    def setUp(self):
        self.task = TaskA(sample=None)
        self.output_data = None

    def test_run(self):
        source = 'hoge'
        target = {'param_a': 1, 'param_b': 'hoge'}

        self.task.sample = source
        self.task.dump = MagicMock(side_effect=self._dump)

        self.task.run()
        self.assertDictEqual(self.output_data, target)

    def _dump(self, data):
        self.output_data = data


class TestTaskB(unittest.TestCase):
    def setUp(self):
        self.task = TaskB(task=gokart.TaskOnKart())
        self.output_data = None

    def test_run(self):
        source = {'test': 'hoge'}
        target = {'test': 'hoge', 'trained': True}

        self.task.load = MagicMock(side_effect=lambda: source)
        self.task.dump = MagicMock(side_effect=self._dump)

        self.task.run()
        self.assertDictEqual(self.output_data, target)

    def _dump(self, data):
        self.output_data = data


class TestTaskC(unittest.TestCase):
    def setUp(self):
        self.task = TaskC()
        self.output_data = None

    def test_run(self):
        source = {'test': 'hoge'}
        target = {'test': 'hoge', 'task_name': 'task_c'}

        self.task.load = MagicMock(side_effect=lambda: source)
        self.task.dump = MagicMock(side_effect=self._dump)

        self.task.run()
        self.assertDictEqual(self.output_data, target)

    def _dump(self, data):
        self.output_data = data
