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

    def insert(self, value: T) -> bool:
        if self._root is None:
            self._root = BinarySearchTreeNode(value)
            return True

        next_node = self._root
        while True:
            if next_node.value == value:
                return False

            if value > next_node.value:
                if next_node.right is None:
                    next_node.right = BinarySearchTreeNode(value)
                    return True
                next_node = next_node.right

            if value < next_node.value:
                if next_node.left is None:
                    next_node.left = BinarySearchTreeNode(value)
                    return True
                next_node = next_node.left

    def contains(self, value: T) -> bool:
        next_node = self._root
        while True:
            if next_node is None:
                return False
            if next_node.value == value:
                return True
            elif value > next_node.value:
                next_node = next_node.right
            else:
                next_node = next_node.left


if __name__ == "__main__":
    try:
        from data_structures.binary_search_tree_printer import BinarySearchTreePrinter
    except ModuleNotFoundError:
        from binary_search_tree_printer import BinarySearchTreePrinter

    print("\nUsing insert method:")
    bst = BinarySearchTree()
    bst.insert(15)
    bst.insert(10)
    bst.insert(20)
    bst.insert(8)
    bst.insert(12)
    bst.insert(18)
    bst.insert(25)

    BinarySearchTreePrinter().print(bst)

    print("\nUsing contains method:")
    print(f"contains(15): {bst.contains(15)}")
    print(f"contains(20): {bst.contains(20)}")
    print(f"contains(25): {bst.contains(25)}")
    print(f"contains(99): {bst.contains(99)}")
