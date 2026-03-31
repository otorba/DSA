from typing import Generic, Iterator, TypeVar

from data_structures.double_linked_list import DoubleLinkedList

T = TypeVar("T")


class Queue(Generic[T]):
    def __init__(self):
        self.dll = DoubleLinkedList()

    def __len__(self) -> int:
        return len(self.dll)

    def enqueue(self, value: T) -> None:
        self.dll.append(value)

    def dequeue(self) -> T:
        if not self.dll:
            raise IndexError("Queue is empty")
        return self.dll.pop_front()

    def peek(self) -> T:
        if not self.dll:
            raise IndexError("Queue is empty")
        return self.dll.get(0)

    def __iter__(self) -> Iterator[T]:
        return iter(self.dll)
