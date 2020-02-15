from logging import getLogger
import gokart
import luigi

logger = getLogger(__name__)


class TaskBase(gokart.TaskOnKart):
    task_namespace = 'sample'


class TaskA(TaskBase):
    sample = luigi.Parameter()

    def run(self):
        results = {'param_a': 1, 'param_b': self.sample}
        self.dump(results)


class TaskB(TaskBase):
    task = gokart.TaskInstanceParameter()

    def requires(self):
        return self.task

    def run(self):
        params = self.load()
        params.update({'trained': True})  # training model
        self.dump(params)


class TaskC(TaskBase):
    def requires(self):
        return TaskB(task=self.clone(TaskA, sample='hoge'))

    def run(self):
        model = self.load()
        model.update({'task_name': 'task_c'})
        self.dump(model)
