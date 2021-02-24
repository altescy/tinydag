TinyDAG
=======

[![Actions Status](https://github.com/altescy/tinydag/workflows/CI/badge.svg)](https://github.com/altescy/tinydag/actions?query=workflow%3ACI)

TinyDAG is a simple library to execute multi-threaded DAG-tree workflows.


```python
# main.py

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
```
```
$ python main.py
[ 2021-02-25 03:47:25,088 ] Start node: generate_sequence
[ 2021-02-25 03:47:25,088 ] Finish node: generate_sequence
[ 2021-02-25 03:47:25,089 ] Start node: double
[ 2021-02-25 03:47:25,089 ] Start node: square
[ 2021-02-25 03:47:26,089 ] Finish node: double
[ 2021-02-25 03:47:27,091 ] Finish node: square
[ 2021-02-25 03:47:27,092 ] Start node: sum
[ 2021-02-25 03:47:27,092 ] Finish node: sum
[ 2021-02-25 03:47:27,093 ] output: [0, 4, 8, 12, 16, 20, 24, 28, 32, 36]
```
