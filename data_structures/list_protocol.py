from typing import Iterator, Protocol, TypeVar

T = TypeVar("T")


class ListProtocol(Protocol[T]):
    def __iter__(self) -> Iterator[T]:
        """
        <summary>
        Returns an iterator that iterates through the list.
        </summary>
        """
        ...

    def __len__(self) -> int:
        """
        <summary>
        Returns the number of elements in the list.
        </summary>
        """

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
