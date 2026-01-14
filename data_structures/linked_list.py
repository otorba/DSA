from typing import Generic, Iterator, Self, TypeVar

T = TypeVar("T")


class LinkedList(Generic[T]):
    # noinspection PyTypeHints
    class __Node(Generic[T]):
        __slots__ = ("value", "next")
        value: T
        next: Self | None

        def __init__(self, value: T):
            self.value = value
            self.next = None

    __head: __Node[T] | None
    __tail: __Node[T] | None
    __length: int

    def __init__(self):
        self.__head = self.__tail = None
        self.__length = 0

    def __len__(self) -> int:
        return self.__length

    def __iter__(self) -> Iterator[T]:
        current = self.__head
        while current is not None:
            yield current.value
            current = current.next

    def append(self, value: T) -> None:
        new_node = self.__Node(value)
        if self.__head is None:
            self.__head = self.__tail = new_node
        else:
            self.__tail.next = new_node
            self.__tail = new_node
        self.__length += 1

    def prepend(self, value: T) -> None:
        new_node = self.__Node(value)
        if self.__length == 0:
            self.__head = self.__tail = new_node
        else:
            current_value = self.__head
            new_node.next = current_value
            self.__head = new_node

        self.__length += 1

    def extend(self, values: Iterator[T]) -> None:
        for i in values:
            self.append(i)

    def insert(self, index: int, value: T) -> None:
        if (
                index < 0
                or index > self.__length
                or (self.__length == 0 and index > 0)
        ):
            raise IndexError("Index out of bounds")

        new_node = self.__Node(value)
        if self.__head is None:
            self.__head = self.__tail = new_node
            self.__length += 1
            return

        if index == 0:
            new_node.next = self.__head
            self.__head = new_node
            self.__length += 1
            return

        prev_node = self.__head
        for _ in range(index - 1):
            prev_node = prev_node.next

        new_node.next = prev_node.next
        prev_node.next = new_node
        if new_node.next is None:
            self.__tail = new_node

        self.__length += 1

    def remove(self, value: T) -> bool:
        if self.__length == 0 or (
                self.__head is None and self.__tail is None
        ):
            return False

        prev_node = None
        current = self.__head
        while current is not None:
            if current.value == value:
                if prev_node is not None:
                    prev_node.next = current.next  # remove a node from a list
                else:
                    self.__head = current.next
                if current == self.__tail:
                    self.__tail = prev_node
                self.__length -= 1
                return True

            prev_node = current
            current = current.next

        return False

    def pop_front(self) -> T:
        if self.__length == 0:
            raise IndexError("Pop from empty list")

        if self.__head == self.__tail:
            value_to_return = self.__head.value
            self.__head = self.__tail = None
            self.__length = 0
            return value_to_return

        node_to_remove = self.__head
        self.__head = node_to_remove.next
        self.__length -= 1
        return node_to_remove.value

    def pop_back(self) -> T:
        if self.__length == 0:
            raise IndexError("Pop from empty list")

        if self.__head == self.__tail:
            value_to_return = self.__head.value
            self.__head = self.__tail = None
            self.__length = 0
            return value_to_return

        # we don't have a reference to the previous node, so we need to iterate
        prev_node = self.__head
        while prev_node.next is not self.__tail:
            prev_node = prev_node.next

        value_to_return = self.__tail.value
        prev_node.next = None
        self.__tail = prev_node
        self.__length -= 1
        return value_to_return

    def index_of(self, value: T) -> int | None:
        index = 0
        for i in self:
            if i == value:
                return index
            index += 1

        return None

    def get(self, index: int) -> T | None:
        if index < 0 or index >= self.__length:
            raise IndexError("Index out of bounds")

        i = 0
        for value in self:
            if i == index:
                return value
            i += 1

        return None
