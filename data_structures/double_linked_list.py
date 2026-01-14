from typing import Generic, Iterator, Self, TypeVar

T = TypeVar("T")


class DoubleLinkedList(Generic[T]):
    # noinspection PyTypeHints
    class __Node(Generic[T]):
        __slots__ = ("value", "next", "prev")
        value: T
        next: Self | None
        prev: Self | None

        def __init__(self, value: T):
            self.value = value
            self.next = self.prev = None

    __head: __Node[T] | None
    __tail: __Node[T] | None
    __length: int

    def __init__(self):
        self.__head = self.__tail = None
        self.__length = 0

    def __len__(self) -> int:
        return self.__length

    def __iter__(self) -> Iterator[T]:
        current_node = self.__head
        while current_node is not None:
            yield current_node.value
            current_node = current_node.next

    def append(self, value: T) -> None:
        node = self.__Node(value)
        if self.__length == 0:
            self.__head = self.__tail = node
        elif self.__length == 1:
            node.prev = self.__head
            self.__head.next = node
            self.__tail = node
        else:
            self.__tail.next = node
            node.prev = self.__tail
            self.__tail = node

        self.__length += 1

    def prepend(self, value: T) -> None:
        node = self.__Node(value)
        if self.__length == 0:
            self.__head = self.__tail = node
        else:
            node.next = self.__head
            self.__head.prev = node
            self.__head = node

        self.__length += 1

    def extend(self, values: Iterator[T]) -> None:
        for i in values:
            self.append(i)

    def insert(self, index: int, value: T) -> None:
        if index < 0 or index > self.__length:
            raise IndexError("Index out of bounds")

        new_node = self.__Node(value)
        if self.__length == 0:
            self.__head = self.__tail = new_node
            self.__length += 1
            return

        if index == 0:
            new_node.next = self.__head
            self.__head.prev = new_node
            self.__head = new_node
            self.__length += 1
            return

        if index == self.__length:
            new_node.prev = self.__tail
            self.__tail.next = new_node
            self.__tail = new_node
            self.__length += 1
            return

        if self.__length / 2 < index:
            i = 0
            node = self.__head
            while i != index - 1:
                node = node.next
                i += 1
            next_node = node.next
            new_node.prev = node
            node.next = new_node
            new_node.next = next_node
        else:
            i = self.__length
            node = self.__tail
            next_node = node
            while i != index + 1:
                next_node = node.prev
                i -= 1
            node = next_node.prev
            new_node.prev = node
            node.next = new_node
            new_node.next = next_node
            next_node.prev = new_node
        self.__length += 1

    def remove(self, value: T) -> bool:
        if self.__length == 0 or (
                self.__head is None and self.__tail is None
        ):
            return False

        if self.__length == 1 and value == self.__tail.value:
            self.__head = self.__tail = None
            self.__length = 0
            return True

        node = self.__head
        node_to_remove = None
        while node is not None:
            if node.value == value:
                node_to_remove = node
                break
            node = node.next

        if node_to_remove is None:
            return False

        if node_to_remove is self.__head:
            next_node = node_to_remove.next
            next_node.prev = None
            self.__head = next_node
        elif node_to_remove is self.__tail:
            prev_node = node_to_remove.prev
            prev_node.next = None
            self.__tail = prev_node
        else:
            prev_node = node.prev
            next_node = node.next
            prev_node.next = next_node
            next_node.prev = prev_node

        self.__length -= 1
        return True

    def pop_front(self) -> T:
        if self.__length == 0:
            raise IndexError("Pop from empty list")

        if self.__length == 1:
            value = self.__head.value
            self.__head = self.__tail = None
        else:
            value = self.__head.value
            self.__head = self.__head.next
            self.__head.prev.next = None

        self.__length -= 1
        return value

    def pop_back(self) -> T:
        if self.__length == 0:
            raise IndexError("Pop from empty list")

        if self.__length == 1:
            value = self.__tail.value
            self.__head = self.__tail = None
        else:
            value = self.__tail.value
            prev_node = self.__tail.prev
            prev_node.next = None
            self.__tail = prev_node

        self.__length -= 1
        return value

    def index_of(self, value: T) -> int | None:
        i = 0
        for v in self:
            if v == value:
                return i
            i += 1
        return None

    def get(self, index: int) -> T | None:
        if index < 0 or index >= self.__length:
            raise IndexError("Index out of bounds")

        if self.__length == 0:
            raise IndexError("List is empty")

        if index == 0:
            return self.__head.value

        if index == self.__length - 1:
            return self.__tail.value

        if self.__length / 2 < index:
            i = 0
            for value in self:
                if i == index:
                    return value
                i += 1
        else:
            i = self.__length
            node = self.__tail
            while i != index:
                node = node.prev
                i -= 1
            return node.value

        return None
