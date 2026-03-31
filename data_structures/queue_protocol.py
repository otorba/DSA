from typing import Iterator, Protocol, TypeVar

T = TypeVar("T")


class QueueProtocol(Protocol[T]):
    def enqueue(self, value: T) -> None:
        """
        Add *value* to the back of the queue.
        """
        ...

    def dequeue(self) -> T:
        """
        Remove and return the front element.
        Raises IndexError when the queue is empty.
        """
        ...

    def peek(self) -> T:
        """
        Return the front element without removing it.
        Raises IndexError when the queue is empty.
        """
        ...

    def __len__(self) -> int:
        """
        Return the number of elements in the queue.
        """
        ...

    def __iter__(self) -> Iterator[T]:
        """
        Iterate over elements from front to back (FIFO order).
        Must not modify the queue.
        """
        ...
