# gokart-examples
gokart examples for m3 techbook 2


# 1, Make project by cookiecutter-gokart

We can use project templete by [cookiecutter](https://github.com/cookiecutter/cookiecutter).

```
$ cookiecutter https://github.com/m3dev/cookiecutter-gokart
project_name [project_name]: GokartSample
package_name [package_name]: sample
python_version [3.6]:
author [your name]: vaaaaanquish
package_description [What's this project?]: gokart task example
license [MIT License]:
```

```
$ tree .
.
├── GokartSample
│   ├── README.md
│   ├── conf
│   │   ├── logging.ini
│   │   └── param.ini
│   ├── main.py
│   ├── sample
│   │   ├── __init__.py
│   │   └── model
│   │       ├── __init__.py
│   │       └── sample.py
│   ├── setup.py
│   └── test
│       └── unit_test
│           ├── __init__.py
│           └── test_sample.py
└── README.md
```


Unittest has already been added :)


```
$ cd GokartSample/
$ python -m unittest discover -s ./test/unit_test
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```
start test-driven development!



# 2, Development gokart task

example: GokartSample/sample/model/sample.py
 - TaskA: dump dict
 - TaskB: update dict
 - TaskC: TasA -> TaskB and update dict


TDD. It is a correspondence table between task and test.

<table>
<tr>
<th>sample/model/sample.py</th>
<th>test/unit_test/test_sample.py</th>
</tr>
<tr>
<td><pre>
class TaskA(gokart.TaskOnKart):
    sample = luigi.Parameter()

    def run(self):
        results = {'param_a': 1, 'param_b': self.sample}
        self.dump(results)
</pre></td>
<td><pre>class TestTaskA(unittest.TestCase):
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
</pre></td></tr>
<tr><td><pre>class TaskB(gokart.TaskOnKart):
    task = gokart.TaskInstanceParameter()

    def requires(self):
        return self.task

    def run(self):
        params = self.load()
        params.update({'trained': True})  # training model
        self.dump(params)
</pre></td>
<td><pre>class TestTaskB(unittest.TestCase):
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
</pre></td></tr>
<tr><td><pre>class TaskC(gokart.TaskOnKart):
    def requires(self):
        return TaskB(task=self.clone(TaskA, sample='hoge'))

    def run(self):
        model = self.load()
        model.update({'task_name': 'task_c'})
        self.dump(model)
</pre></td>
<td><pre>class TestTaskC(unittest.TestCase):
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
</pre></td></tr>
</table>

 

# 3 running gokart

Let's running gokart task.
```
# add new parameter info GokartSample/conf/param.ini
[sample.TaskA]
sample='sample param'
```

run.
```
$ python main.py sample.TaskC --local-scheduler

...
===== Luigi Execution Summary =====
Scheduled 3 tasks of which:
* 3 ran successfully:
    - 1 sample.TaskA(...)
    - 1 sample.TaskB(...)
    - 1 sample.TaskC(...)

This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====
```
↓
check output files
↓
```
$ tree resource

resource/
├── log
│   ├── module_versions
│   │   ├── TaskA_74416d6e12945172d2ae8a4eaa6bc9de.txt
│   │   ├── TaskB_cb786f70051e31e9f4fcdf2aac06b533.txt
│   │   └── TaskC_e49eb8498c2ad327e1ca4ead88cea1ad.txt
│   ├── processing_time
│   │   ├── TaskA_74416d6e12945172d2ae8a4eaa6bc9de.pkl
│   │   ├── TaskB_cb786f70051e31e9f4fcdf2aac06b533.pkl
│   │   └── TaskC_e49eb8498c2ad327e1ca4ead88cea1ad.pkl
│   ├── task_log
│   │   ├── TaskA_74416d6e12945172d2ae8a4eaa6bc9de.pkl
│   │   ├── TaskB_cb786f70051e31e9f4fcdf2aac06b533.pkl
│   │   └── TaskC_e49eb8498c2ad327e1ca4ead88cea1ad.pkl
│   └── task_params
│       ├── TaskA_74416d6e12945172d2ae8a4eaa6bc9de.pkl
│       ├── TaskB_cb786f70051e31e9f4fcdf2aac06b533.pkl
│       └── TaskC_e49eb8498c2ad327e1ca4ead88cea1ad.pkl
└── sample
    └── model
        └── sample
            ├── TaskA_74416d6e12945172d2ae8a4eaa6bc9de.pkl
            ├── TaskB_cb786f70051e31e9f4fcdf2aac06b533.pkl
            └── TaskC_e49eb8498c2ad327e1ca4ead88cea1ad.pkl

8 directories, 15 files
```



# 3, Check data by thunderbolt

Please see './ExampleThunderbolt.ipynb'

```
from thunderbolt import Thunderbolt
tb = Thunderbolt('./resource')
print(tb.get_data(’TaskC’)) # outout TaskC's result
print(tb.get_task_df()) # get all task parameter's
```

# 4, Make Machine Learning Task using redshells

Please see redshells examples.

https://github.com/m3dev/redshells/tree/master/examples


# Thanks.

 - luigi: https://github.com/spotify/luigi
 - cookiecutter-gokart: https://github.com/m3dev/cookiecutter-gokart
 - gokart: https://github.com/m3dev/gokart
 - thunderbolt: https://github.com/m3dev/thunderbolt
 - redshells: https://github.com/m3dev/redshells

Thanks :)
