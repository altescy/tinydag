from typing import Any, List
from concurrent.futures import ThreadPoolExecutor
import logging

from tinydag.node import Node

logger = logging.getLogger()


class TinyDAG:
    def __init__(self, *nodes: Node, max_workers: int = 1) -> None:
        self._nodes = {node.name: node for node in nodes}
        self._max_worker = max_workers

    def _build_dag(self):
        for node in self._nodes.values():
            for depnode_name in node.depends:
                depnode = self._nodes[depnode_name]
                depnode.add_next_node(node)

    def _execute_node_recursively(self, node: Node):
        if not node.is_ready:
            return

        logger.info("start %s", node.name)

        result = node.run()

        logger.info("end %s", node.name)

        if not node.next_nodes:
            return

        for next_node in node.next_nodes:
            next_node.set_input(node.name, result)

        with ThreadPoolExecutor(max_workers=self._max_worker) as executor:
            for next_node in node.next_nodes:
                executor.submit(self._execute_node_recursively, next_node)

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

    def run(self):
        self._build_dag()

        start_nodes = [
            node for node in self._nodes.values() if not node.depends
        ]

        with ThreadPoolExecutor(max_workers=self._max_worker) as executor:
            for node in start_nodes:
                executor.submit(self._execute_node_recursively, node)
