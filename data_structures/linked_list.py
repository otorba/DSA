from typing import Generic, Iterator, Protocol, Self, TypeVar

T = TypeVar("T")


class LinkedListProtocol(Protocol[T]):
    def __iter__(self) -> Iterator[T]:
        """
        <summary>
        Returns an iterator that iterates through the list.
        </summary>
        """
        ...

    def append(self, value: T) -> None:
        """
        <summary>
        Adds an item to the end of the list.
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

    def insert(self, index: int, value: T) -> None:
        """
        <summary>
        Inserts an item at the specified index.
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

    def pop_front(self) -> T:
        """
        Removes and returns the first item from the list.
        :return:
        """

    def pop_back(self) -> T:
        """
        <summary>
        Removes and returns the last item from the list.
        </summary>
        """
        ...

    def index_of(self, value: T) -> int | None:
        """
        <summary>
        Determines the index of a specific item in the list.
        </summary>
        """
        ...


class LinkedList(Generic[T]):
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
        self._head = self._tail = None
        self._items_count = 0

    def __iter__(self) -> Iterator[T]:
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def append(self, value: T) -> None:
        new_node = self._Node(value)
        if self._head is None:
            self._head = self._tail = new_node
            self._items_count += 1
            return

        self._tail._next = new_node
        self._tail = new_node
        self._items_count += 1

    def extend(self, values: Iterator[T]) -> None:
        for i in values:
            self.append(i)

    def insert(self, index: int, value: T) -> None:
        if (
                index < 0
                or index > self._items_count
                or (self._items_count == 0 and index > 0)
        ):
            raise IndexError("Index out of bounds")

        new_node = self._Node(value)
        if self._head is None:
            self._head = self._tail = new_node
            self._items_count += 1
            return

        if index == 0:
            new_node._next = self._head
            self._head = new_node
            self._items_count += 1
            return

        prev_node = self._head
        for _ in range(index - 1):
            prev_node = prev_node.next

        new_node._next = prev_node.next
        prev_node._next = new_node
        if new_node.next is None:
            self._tail = new_node

        self._items_count += 1

    def remove(self, value: T) -> bool:
        if self._items_count == 0 or (
                self._head is None and self._tail is None
        ):
            return False

        prev_node = None
        current = self._head
        while current is not None:
            if current.value == value:
                if prev_node is not None:
                    prev_node._next = current.next  # remove a node from a list
                else:
                    self._head = current.next
                if current == self._tail:
                    self._tail = prev_node
                self._items_count -= 1
                return True

            prev_node = current
            current = current.next

        return False

    def pop_front(self) -> T:
        if self._items_count == 0:
            raise IndexError("Pop from empty list")

        if self._head == self._tail:
            value_to_return = self._head.value
            self._head = self._tail = None
            self._items_count -= 1
            return value_to_return

        node_to_remove = self._head
        self._head = node_to_remove.next
        self._items_count -= 1
        return node_to_remove.value

    def pop_back(self) -> T:
        if self._items_count == 0:
            raise IndexError("Pop from empty list")

        if self._head == self._tail:
            value_to_return = self._head.value
            self._head = self._tail = None
            self._items_count -= 1
            return value_to_return

        # we don't have a reference to the previous node, so we need to iterate
        prev_node = self._head
        while prev_node.next is not None and prev_node.next != self._tail:
            prev_node = prev_node.next

        value_to_return = self._tail.value
        prev_node._next = None
        self._tail = prev_node
        self._items_count -= 1
        return value_to_return

    def index_of(self, value: T) -> int | None:
        index = 0
        for i in self:
            if i == value:
                return index
            index += 1

        return None
