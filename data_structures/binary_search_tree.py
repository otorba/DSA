from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class BinarySearchTreeNode(Generic[T]):
    value: T
    left: BinarySearchTreeNode[T] | None = None
    right: BinarySearchTreeNode[T] | None = None


class BinarySearchTree(Generic[T]):
    _root: BinarySearchTreeNode[T] | None

    def __init__(self) -> None:
        self._root = None

    @property
    def root(self) -> BinarySearchTreeNode[T] | None:
        return self._root

    def insert(self, value: T) -> None:
        self._root = self._set_next(self._root, value)

    def _set_next(
            self, next_node: BinarySearchTreeNode[T] | None, value: T
    ) -> BinarySearchTreeNode[T]:
        if next_node is None:
            return BinarySearchTreeNode(value)

        if value > next_node.value:
            next_node.right = self._set_next(next_node.right, value)

        if value <= next_node.value:
            next_node.left = self._set_next(next_node.left, value)

        return next_node


if __name__ == "__main__":
    try:
        from data_structures.binary_search_tree_printer import BinarySearchTreePrinter
    except ModuleNotFoundError:
        from binary_search_tree_printer import BinarySearchTreePrinter

    bst = BinarySearchTree()
    bst.insert(12)
    bst.insert(25)
    bst.insert(27)
    bst.insert(6)
    bst.insert(7)

    BinarySearchTreePrinter().print(bst)
