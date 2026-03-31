from typing import TypeVar, Generic, Self

T = TypeVar("T")


class Stack(Generic[T]):
    # noinspection PyTypeHints
    class __Node(Generic[T]):
        __slots__ = ("value", "next")
        value: T
        next: Self | None

        def __init__(self, value: T):
            self.value = value
            self.next = None

    __top: __Node[T] | None
    __length: int

    def __init__(self):
        self.__top = None
        self.__length = 0

    def __len__(self):
        return self.__length

    def push(self, value: T) -> None:
        node = self.__Node(value)
        if self.__top:
            node.next = self.__top
            self.__top = node
        else:
            self.__top = node

        self.__length += 1

    def pop(self) -> T:
        if self.__length == 0:
            raise IndexError("Pop from empty stack")

        current_top = self.__top
        self.__top = current_top.next
        current_top.next = None

        self.__length -= 1

        return current_top.value

    def peek(self) -> T:
        if self.__length == 0:
            raise IndexError("Peek from empty stack")

        return self.__top.value

    def __iter__(self):
        current = self.__top
        while current:
            yield current.value
            current = current.next
