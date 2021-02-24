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
