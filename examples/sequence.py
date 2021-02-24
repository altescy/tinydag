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
def sumseq(doubled_seq, squared_seq):
    return [x + y for x, y in zip(doubled_seq, squared_seq)]


dag.run()
result = dag.get_output("sum")

logging.info("output: %s", result)
