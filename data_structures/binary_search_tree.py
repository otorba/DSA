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

    def insert_recursively(self, value: T) -> None:
        self._root = self._set_next(self._root, value)

    def _set_next(
            self, next_node: BinarySearchTreeNode[T] | None, value: T
    ) -> BinarySearchTreeNode[T]:
        if next_node is None:
            return BinarySearchTreeNode(value)

        if value > next_node.value:
            next_node.right = self._set_next(next_node.right, value)

        if value < next_node.value:
            next_node.left = self._set_next(next_node.left, value)

        if value == next_node.value:
            return next_node

        return next_node

    def insert(self, value: T) -> bool:
        temp = BinarySearchTreeNode(value)
        if self._root is None:
            self._root = temp
            return True

        next_node = self._root
        while True:
            if next_node.value == value:
                return False

            if value > next_node.value:
                if next_node.right is None:
                    next_node.right = temp
                    return True
                next_node = next_node.right

            if value < next_node.value:
                if next_node.left is None:
                    next_node.left = temp
                    return True
                next_node = next_node.left


if __name__ == "__main__":
    try:
        from data_structures.binary_search_tree_printer import BinarySearchTreePrinter
    except ModuleNotFoundError:
        from binary_search_tree_printer import BinarySearchTreePrinter

    bst = BinarySearchTree()
    bst.insert_recursively(12)
    bst.insert_recursively(25)
    bst.insert_recursively(25)
    bst.insert_recursively(27)
    bst.insert_recursively(6)
    bst.insert_recursively(6)
    bst.insert_recursively(7)
    bst.insert_recursively(7)

    BinarySearchTreePrinter().print(bst)

    print("\nUsing insert method:")
    bst2 = BinarySearchTree()
    bst2.insert(15)
    bst2.insert(10)
    bst2.insert(20)
    bst2.insert(8)
    bst2.insert(12)
    bst2.insert(18)
    bst2.insert(25)

    BinarySearchTreePrinter().print(bst2)
