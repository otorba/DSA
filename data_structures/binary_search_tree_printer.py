from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from data_structures.binary_search_tree import (
        BinarySearchTree,
        BinarySearchTreeNode,
    )

T = TypeVar("T")

_BRANCH_GAP = 2


class BinarySearchTreePrinter(Generic[T]):
    def print(self, tree: BinarySearchTree[T]) -> None:
        for line in self.to_lines(tree):
            print(line)

    def to_lines(self, tree: BinarySearchTree[T]) -> list[str]:
        root = tree.root
        if root is None:
            return ["<empty>"]

        lines, *_ = self._display_aux(root)
        return [line.rstrip() for line in lines]

    def _display_aux(
            self, node: BinarySearchTreeNode[T]
    ) -> tuple[list[str], int, int, int]:
        value = str(node.value)

        if node.left is None and node.right is None:
            width = len(value)
            height = 1
            middle = width // 2
            return [value], width, height, middle

        if node.right is None:
            assert node.left is not None
            left_lines, left_width, left_height, left_middle = self._display_aux(
                node.left
            )
            gap = len(value) + _BRANCH_GAP
            middle = left_middle + gap + len(value) // 2
            width = left_width + gap + len(value)

            first_line = self._place(value, width, middle)
            second_line = self._place("/", width, (left_middle + middle) // 2)

            shifted_lines = [
                line.ljust(left_width) + " " * (gap + len(value))
                for line in left_lines
            ]

            return (
                [first_line, second_line] + shifted_lines,
                width,
                left_height + 2,
                middle,
            )

        if node.left is None:
            assert node.right is not None
            right_lines, right_width, right_height, right_middle = self._display_aux(
                node.right
            )
            gap = len(value) + _BRANCH_GAP
            right_root = len(value) + gap + right_middle
            width = len(value) + gap + right_width
            middle = len(value) // 2

            first_line = self._place(value, width, middle)
            second_line = self._place("\\", width, (middle + right_root) // 2)

            shifted_lines = [
                " " * (len(value) + gap) + line
                for line in right_lines
            ]

            return (
                [first_line, second_line] + shifted_lines,
                width,
                right_height + 2,
                middle,
            )

        assert node.left is not None
        assert node.right is not None
        left_lines, left_width, left_height, left_middle = self._display_aux(node.left)
        right_lines, right_width, right_height, right_middle = self._display_aux(
            node.right
        )
        gap = len(value) + _BRANCH_GAP
        right_root = left_width + gap + right_middle
        width = left_width + gap + right_width
        middle = (left_middle + right_root) // 2

        first_line = self._place(value, width, middle)
        second_line = self._place("/", width, (left_middle + middle) // 2)
        second_line = self._overlay(
            second_line, "\\", (middle + right_root) // 2
        )

        if left_height < right_height:
            left_lines += [" " * left_width] * (right_height - left_height)
        elif right_height < left_height:
            right_lines += [" " * right_width] * (left_height - right_height)

        zipped_lines = [
            left.ljust(left_width) + " " * gap + right
            for left, right in zip(left_lines, right_lines)
        ]

        return (
            [first_line, second_line] + zipped_lines,
            width,
            max(left_height, right_height) + 2,
            middle,
        )

    def _place(self, text: str, width: int, middle: int) -> str:
        start = max(middle - len(text) // 2, 0)
        return self._overlay(" " * width, text, start)

    def _overlay(self, line: str, text: str, start: int) -> str:
        return line[:start] + text + line[start + len(text):]
