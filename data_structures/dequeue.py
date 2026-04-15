from typing import TypeVar, Generic, Iterator

T = TypeVar("T")


class Dequeue(Generic[T]):
    def __init__(self):
        self._capacity = 4
        self._data = [None] * self._capacity  # circular array
        self._length = 0
        self._head = 0
        self._tail = 0

    def __len__(self) -> int:
        return self._length

    def enqueue(self, value: T) -> None:
        if self._length == self._capacity:
            self._grow()

        self._data[self._tail] = value
        self._tail = (self._tail + 1) % self._capacity
        self._length += 1

    def _grow(self):
        new_capacity = self._capacity * 2
        new_data = [None] * new_capacity
        for i in range(0, self._length):
            old_index = (self._head + i) % self._capacity
            new_data[i] = self._data[old_index]

        self._capacity = new_capacity
        self._data = new_data
        self._head = 0
        self._tail = self._length

    def dequeue(self) -> T:
        if self._length == 0:
            raise IndexError("Dequeue is empty")

        self._length -= 1
        value = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._capacity
        return value

    def peek(self) -> T:
        if self._length == 0:
            raise IndexError("Dequeue is empty")

        return self._data[self._head]

    def __iter__(self) -> Iterator[T]:
        for i in range(0, self._length):
            index = (self._head + i) % self._capacity
            yield self._data[index]
