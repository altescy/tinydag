from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
import threading

from tinydag.exceptions import NodeUnexecutedError


class Node:
    def __init__(
        self,
        name: str,
        func: Callable,
        depends: Optional[List[str]] = None,
    ) -> None:
        self._name = name
        self._depends = depends or []
        self._func = func
        self._next_nodes: List[Node] = []
        self._inputs: Dict[str, Any] = {}
        self._output: Optional[Any] = None
        self._is_executed = False
        self._lock = threading.RLock()

    @property
    def name(self) -> str:
        return self._name

    @property
    def depends(self) -> List[str]:
        return self._depends

    @property
    def next_nodes(self) -> List[Node]:
        return self._next_nodes

    @property
    def is_ready(self) -> bool:
        with self._lock:
            return len(self._depends) == len(self._inputs)

    @property
    def is_executed(self) -> bool:
        return self._is_executed

    @property
    def output(self) -> Any:
        if not self.is_executed:
            raise NodeUnexecutedError(f"Node <{self.name}> is not executed.")
        return self._output

    def add_next_node(self, next_node: Node) -> None:
        self._next_nodes.append(next_node)

    def set_input(self, depname: str, data: Any):
        with self._lock:
            self._inputs[depname] = data

    def run(self) -> Any:
        inputs: List[Any] = [
            self._inputs[depname] for depname in self._depends
            if depname in self._inputs
        ]
        if len(self._inputs) != len(self._depends):
            raise RuntimeError("numbers of required and given "
                               "inputs is not matched")

        self._output = self._func(*inputs)
        self._is_executed = True
        return self._output

    def __repr__(self) -> str:
        return f"<Node: name={self.name}, depends={self.depends}, next_nodes={self.next_nodes}>"
