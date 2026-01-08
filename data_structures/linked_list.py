from typing import Iterator, Protocol, Self, TypeVar

T = TypeVar("T")


class LinkedListProtocol(Protocol[T]):
    def append(self, value: T) -> None:
        """
        <summary>
        Adds an item to the end of the list.
        </summary>
        """
        ...

    def insert(self, index: int, value: T) -> None:
        """
        <summary>
        Inserts an item at the specified index.
        </summary>
        """
        ...

    def pop_back(self) -> T:
        """
        <summary>
        Removes and returns the last item from the list.
        </summary>
        """
        ...

    def remove(self, value: T) -> bool:
        """
        <summary>
        Removes the first occurrence of a specific object from the list.
        </summary>
        """
        ...

    def __iter__(self) -> Iterator[T]:
        """
        <summary>
        Returns an iterator that iterates through the list.
        </summary>
        """
        ...

    def extend(self, values: Iterator[T]) -> None:
        """
        <summary>
        Adds the elements of the specified collection to the end of the list.
        </summary>
        """
        ...

    def index_of(self, value: T) -> int:
        """
        <summary>
        Determines the index of a specific item in the list.
        </summary>
        """
        ...


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
    _items_count: int

    def __init__(self):
        self._tail = self._head = None
        self._items_count = 0

    def append(self, value: T) -> None:
        if self._tail is None and self._head is None:
            self._tail = self._head = self._Node(value)
            return

        new_node = self._Node(value)
        self._head._next = new_node  # set a previous head next to the new node
        self._head = new_node
        self._items_count += 1

    def insert(self, index: int, value: T) -> None:
        if (
                index < 0
                or index > self._items_count + 1
                or (self._items_count == 0 and index > 0)
        ):
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

        self._items_count += 1

    def pop_back(self) -> T:
        if self._items_count == 0:
            raise IndexError("Pop from empty list")

        # we don't have a reference to the previous node, so we need to iterate
        prev_node = self._tail
        while prev_node.next != self._head:
            prev_node = prev_node.next

        prev_node._next = None
        value_to_return = self._head.value
        self._head = prev_node
        return value_to_return

    def remove(self, value: T) -> bool:
        if (self._items_count == 0) or (
                self._tail is None and self._head is None
        ):
            return False

        prev_node = None
        current = self._tail
        while current is not None:
            if current.value == value:
                if prev_node is not None:
                    prev_node._next = current.next  # remove a node from a list
                    self._items_count -= 1
                    return True
                if current == self._tail:
                    # remove the first node from the list
                    # if it was the last node
                    self._tail = current.next
                    self._items_count -= 1
                    return True

            prev_node = current
            current = current.next

        return False

    def extend(self, values: Iterator[T]) -> None:
        for i in values:
            self.append(i)

    def __iter__(self) -> Iterator[T]:
        current = self._tail
        while current is not None:
            yield current.value
            current = current.next
