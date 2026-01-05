from typing import Iterator, Protocol, Self, TypeVar

T = TypeVar("T")


class LinkedListProtocol(Protocol[T]):
    def append(self, value: T) -> bool: ...

    def insert(self, index: int, value: T) -> bool: ...

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

    def __init__(self):
        self._tail = self._head = None

    def append(self, value: T) -> None:
        if self._tail is None and self._head is None:
            self._tail = self._head = self._Node(value)
            return

        new_node = self._Node(value)
        self._head._next = new_node  # set a previous head's next to new node
        self._head = new_node

    def insert(self, index: int, value: T) -> None:
        if self._tail is None and self._head is None:
            if index != 0:
                raise IndexError("Index out of bounds")
            self._tail = self._head = self._Node(value)
            return

        i = 0
        while i != index:
            i += 1

    def __iter__(self) -> Iterator[T]:
        current = self._tail
        while current is not None:
            yield current.value
            current = current.next
