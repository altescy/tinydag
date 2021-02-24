TinyDAG
=======

[![Actions Status](https://github.com/altescy/tinydag/workflows/CI/badge.svg)](https://github.com/altescy/tinydag/actions?query=workflow%3ACI)

TinyDAG is a simple library to execute multi-threaded DAG-tree workflows.


```python
$ cat main.py
import logging
import time

from tinydag import TinyDAG

logging.basicConfig(
    format="[ %(asctime)s ] %(message)s",
    level=logging.INFO,
)

dag = TinyDAG(max_workers=2)


@dag.add_node("generate_sequence")
def generate_sequence():
    return list(range(10))


@dag.add_node("double", depends=["generate_sequence"])
def double(seq):
    time.sleep(1)
    return [2 * x for x in seq]


@dag.add_node("square", depends=["generate_sequence"])
def square(seq):
    time.sleep(2)
    return [2 * x for x in seq]


@dag.add_node("sum", depends=["double", "square"])
def seqsum(doubled_seq, squared_seq):
    return [x + y for x, y in zip(doubled_seq, squared_seq)]


dag.run()
result = dag.get_output("sum")

logging.info("output: %s", result)

$ python main.py
[ 2021-02-25 01:16:48,717 ] start generate_sequence
[ 2021-02-25 01:16:48,717 ] end generate_sequence
[ 2021-02-25 01:16:48,717 ] start double
[ 2021-02-25 01:16:48,718 ] start square
[ 2021-02-25 01:16:49,719 ] end double
[ 2021-02-25 01:16:50,719 ] end square
[ 2021-02-25 01:16:50,720 ] start sum
[ 2021-02-25 01:16:50,720 ] end sum
[ 2021-02-25 01:16:50,721 ] output: [0, 4, 8, 12, 16, 20, 24, 28, 32, 36]
```
