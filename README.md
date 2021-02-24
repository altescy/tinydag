TinyDAG
=======

[![Actions Status](https://github.com/altescy/tinydag/workflows/CI/badge.svg)](https://github.com/altescy/tinydag/actions?query=workflow%3ACI)

TinyDAG is a simple library to execute multi-threaded DAG-tree workflows.


## Installation

```
$ pip install git+https://github.com/altescy/tinydag.git
```


## Example

```python
# main.py

import logging
import time

from tinydag import TinyDAG

logging.basicConfig(
    format="[ %(asctime)s ] %(message)s",
    level=logging.INFO,
)

dag = TinyDAG()


@dag.add_node("generate_number")
def generate_number():
    return 3


@dag.add_node("double", depends=["generate_number"])
def double(num):
    time.sleep(1)
    return 2 * num


@dag.add_node("square", depends=["generate_number"])
def square(num):
    time.sleep(2)
    return num * num


@dag.add_node("sum", depends=["double", "square"])
def sumup(doubled_num, squared_num):
    return doubled_num + squared_num


dag.run(max_workers=2)
result = dag.get_output("sum")

logging.info("output: %s", result)
```

```
$ python main.py
[ 2021-02-25 04:05:14,292 ] Start node: generate_number
[ 2021-02-25 04:05:14,292 ] Finish node: generate_number
[ 2021-02-25 04:05:14,293 ] Start node: double
[ 2021-02-25 04:05:14,293 ] Start node: square
[ 2021-02-25 04:05:15,293 ] Finish node: double
[ 2021-02-25 04:05:16,295 ] Finish node: square
[ 2021-02-25 04:05:16,295 ] Start node: sum
[ 2021-02-25 04:05:16,296 ] Finish node: sum
[ 2021-02-25 04:05:16,296 ] output: 15
```
