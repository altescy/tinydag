from typing import Any, List
from concurrent.futures import ThreadPoolExecutor, Executor, as_completed
import logging

from tinydag.node import Node

logger = logging.getLogger()


class TinyDAG:
    def __init__(self, *nodes: Node) -> None:
        self._nodes = {node.name: node for node in nodes}

    def _build_dag(self):
        for node in self._nodes.values():
            for depnode_name in node.depends:
                depnode = self._nodes[depnode_name]
                depnode.add_next_node(node)

    def add_node(self, name: str, depends: List[str] = None):
        def decorator(func):
            self._nodes[name] = Node(name, func, depends)
            return func

        return decorator

    def get_output(self, name: str) -> Any:
        if name not in self._nodes:
            raise KeyError(f"Node name '{name}' is not found.")
        node = self._nodes[name]
        return node.output

    def _run(self, executor: Executor, nodes: List[Node]) -> None:
        def _run_node_with_logging(node):
            logger.info("Start node: %s", node.name)
            result = node.run()
            logger.info("Finish node: %s", node.name)
            return result

        future_to_node = {
            executor.submit(_run_node_with_logging, node): node
            for node in nodes if node.is_ready
        }

        for future in as_completed(future_to_node):
            node = future_to_node[future]
            result = future.result()
            for next_node in node.next_nodes:
                next_node.set_input(node.name, result)

            self._run(executor, node.next_nodes)

    def run(self, max_workers: int = 1):
        self._build_dag()

        nodes = list(self._nodes.values())
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            self._run(executor, nodes)
