from typing import Iterator, Protocol, TypeVar

T = TypeVar("T")


class StackProtocol(Protocol[T]):
    def push(self, value: T) -> None:
        """
        Push *value* onto the top of the stack.
        """
        ...

    def pop(self) -> T:
        """
        Remove and return the top element.
        Raises IndexError when the stack is empty.
        """
        ...

    def peek(self) -> T:
        """
        Return the top element without removing it.
        Raises IndexError when the stack is empty.
        """
        ...

    def __len__(self) -> int:
        """
        Return the number of elements in the stack.
        """
        ...

    def __iter__(self) -> Iterator[T]:
        """
        Iterate over elements from top to bottom (LIFO order).
        Must not modify the stack.
        """
        ...
