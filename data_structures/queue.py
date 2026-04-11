from typing import Generic, Iterator, TypeVar

from data_structures.linked_list import LinkedList

T = TypeVar("T")


class Queue(Generic[T]):
    def __init__(self):
        self._ll = LinkedList()

    def __len__(self) -> int:
        return len(self._ll)

    def enqueue(self, value: T) -> None:
        self._ll.append(value)

    def dequeue(self) -> T:
        if not self._ll:
            raise IndexError("Queue is empty")
        return self._ll.pop_front()

    def peek(self) -> T:
        if not self._ll:
            raise IndexError("Queue is empty")
        return self._ll.get(0)

    def __iter__(self) -> Iterator[T]:
        return iter(self._ll)
