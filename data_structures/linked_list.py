from typing import Iterator, Protocol, Self, TypeVar

T = TypeVar("T")


class LinkedListProtocol(Protocol[T]):
    def append(self, value: T) -> None: ...

    def insert(self, index: int, value: T) -> None: ...

    def pop(self) -> T: ...

    def remove(self, value: T) -> bool: ...

    def __iter__(self) -> Iterator[T]: ...

    def extend(self, values: Iterator[T]) -> None: ...

    def index_of(self, value: T) -> int: ...


class LinkedList:
    class _Node:
        def __init__(self, value: T):
            self._value = value
            self._next = None

        @property
        def value(self) -> T:
            return self._value

        @property
        def next(self) -> Self | None:
            return self._next

    _head: _Node | None
    _tail: _Node | None
    _itemsCount: int

    def __init__(self):
        self._tail = self._head = None
        self._itemsCount = 0

    def append(self, value: T) -> None:
        if self._tail is None and self._head is None:
            self._tail = self._head = self._Node(value)
            return

        new_node = self._Node(value)
        self._head._next = new_node  # set a previous head's next to new node
        self._head = new_node
        self._itemsCount += 1

    def insert(self, index: int, value: T) -> None:
        if index < 0 or index > self._itemsCount + 1 or (self._itemsCount == 0 and index > 0):
            raise IndexError("Index out of bounds")

        if self._tail is None:
            self._tail = self._head = self._Node(value)
        else:
            i = 0
            prev_node: LinkedList._Node | None = None
            current_node = self._tail
            while True:
                if i >= index:
                    if prev_node is None:  # insert before the first node
                        new_node = self._Node(value)
                        new_node._next = current_node
                        self._tail = new_node
                    else:
                        new_node = self._Node(value)
                        prev_node._next = new_node
                        new_node._next = current_node
                    break

                prev_node = current_node
                current_node = getattr(current_node, "next", None)
                i += 1

        self._itemsCount += 1

    def pop(self) -> T:
        if self._itemsCount is 0:
            raise IndexError("Pop from empty list")

        # we don't have a reference to the previous node, so we need to iterate
        prev_node = self._tail
        while prev_node.next != self._head:
            prev_node = prev_node.next

        prev_node._next = None
        value_to_return = self._head.value
        self._head = prev_node
        return value_to_return

    def __iter__(self) -> Iterator[T]:
        current = self._tail
        while current is not None:
            yield current.value
            current = current.next
