from collections.abc import Iterable
from itertools import islice
from typing import TypeVar

import pytest
from assertpy import assert_that

from data_structures.linked_list import LinkedListProtocol

T = TypeVar("T")


@pytest.fixture()
def linked_list() -> LinkedListProtocol[int]:
    """
    System-under-test factory.

    These tests target the behavioral contract implied by `LinkedListProtocol`.
    Implement `LinkedList` in `data_structures/linked_list.py` to make them
    pass.
    """
    from data_structures.linked_list import LinkedList

    return LinkedList[int]()


def to_py_list(
        ll: LinkedListProtocol[T], *, max_nodes: int = 1_000
) -> list[T]:
    values = list(islice(iter(ll), max_nodes + 1))
    assert_that(len(values)).described_as(
        "LinkedList iteration did not terminate; possible cycle in links."
    ).is_less_than_or_equal_to(max_nodes)
    return values


def fill(ll: LinkedListProtocol[T], values: Iterable[T]) -> None:
    for value in values:
        ll.append(value)


def test_iter_empty_is_empty(linked_list: LinkedListProtocol[int]):
    # Arrange

    # Act
    actual = to_py_list(linked_list)

    # Assert
    assert_that(actual).is_empty()


def test_append_adds_to_end(linked_list: LinkedListProtocol[int]):
    # Arrange

    # Act
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    actual = to_py_list(linked_list)

    # Assert
    assert_that(actual).is_equal_to([1, 2, 3])


def test_insert_at_head(linked_list: LinkedListProtocol[int]):
    # Arrange
    fill(linked_list, [2, 3])

    # Act
    linked_list.insert(0, 1)
    actual = to_py_list(linked_list)

    # Assert
    assert_that(actual).is_equal_to([1, 2, 3])


def test_insert_at_tail_uses_len_index(linked_list: LinkedListProtocol[int]):
    # Arrange
    fill(linked_list, [1, 2])

    # Act
    linked_list.insert(2, 3)
    actual = to_py_list(linked_list)

    # Assert
    assert_that(actual).is_equal_to([1, 2, 3])


def test_insert_in_middle(linked_list: LinkedListProtocol[int]):
    # Arrange
    fill(linked_list, [1, 3])

    # Act
    linked_list.insert(1, 2)
    actual = to_py_list(linked_list)

    # Assert
    assert_that(actual).is_equal_to([1, 2, 3])


def test_insert_into_empty_at_zero(linked_list: LinkedListProtocol[int]):
    # Arrange

    # Act
    linked_list.insert(0, 1)
    actual = to_py_list(linked_list)

    # Assert
    assert_that(actual).is_equal_to([1])


def test_insert_into_empty_out_of_bounds_raises_and_does_not_modify(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    before = to_py_list(linked_list)

    # Act / Assert
    assert_that(linked_list.insert).raises(IndexError).when_called_with(1, 999)
    after = to_py_list(linked_list)

    # Assert
    assert_that(after).is_equal_to(before)


def test_insert_at_tail_updates_last_element_for_pop_back(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])

    # Act
    linked_list.insert(3, 4)
    popped = linked_list.pop_back()
    after = to_py_list(linked_list)

    # Assert
    assert_that(popped).is_equal_to(4)
    assert_that(after).is_equal_to([1, 2, 3])


@pytest.mark.parametrize("index", [-1, -999, 4, 999])
def test_insert_out_of_bounds_raises_and_does_not_modify(
        linked_list: LinkedListProtocol[int], index: int
):
    # Arrange
    fill(linked_list, [1, 2, 3])
    before = to_py_list(linked_list)

    # Act / Assert
    assert_that(linked_list.insert).raises(IndexError).when_called_with(
        index, 999
    )
    after = to_py_list(linked_list)

    # Assert
    assert_that(after).is_equal_to(before)


def test_pop_back_removes_and_returns_last(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])

    # Act
    first = linked_list.pop_back()
    after_first = to_py_list(linked_list)
    second = linked_list.pop_back()
    after_second = to_py_list(linked_list)

    # Assert
    assert_that(first).is_equal_to(3)
    assert_that(after_first).is_equal_to([1, 2])
    assert_that(second).is_equal_to(2)
    assert_that(after_second).is_equal_to([1])


def test_pop_back_on_empty_raises_index_error(
        linked_list: LinkedListProtocol[int],
):
    # Arrange

    # Act / Assert
    assert_that(linked_list.pop_back).raises(IndexError).when_called_with()


def test_pop_front_removes_and_returns_first(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])

    # Act
    first = linked_list.pop_front()
    after = to_py_list(linked_list)

    # Assert
    assert_that(first).is_equal_to(1)
    assert_that(after).is_equal_to([2, 3])


def test_pop_front_single_element_empties_list(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1])

    # Act
    first = linked_list.pop_front()
    after = to_py_list(linked_list)

    # Assert
    assert_that(first).is_equal_to(1)
    assert_that(after).is_empty()


def test_pop_front_on_empty_raises_index_error(
        linked_list: LinkedListProtocol[int],
):
    # Arrange

    # Act / Assert
    assert_that(linked_list.pop_front).raises(IndexError).when_called_with()


def test_remove_from_empty_returns_false(
        linked_list: LinkedListProtocol[int],
):
    # Arrange

    # Act
    result = linked_list.remove(1)
    after = to_py_list(linked_list)

    # Assert
    assert_that(result).is_false()
    assert_that(after).is_empty()


def test_remove_head_updates_list(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])

    # Act
    result = linked_list.remove(1)
    after = to_py_list(linked_list)

    # Assert
    assert_that(result).is_true()
    assert_that(after).is_equal_to([2, 3])


def test_remove_tail_updates_list(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])

    # Act
    result = linked_list.remove(3)
    after = to_py_list(linked_list)

    # Assert
    assert_that(result).is_true()
    assert_that(after).is_equal_to([1, 2])


def test_remove_only_element_empties_list(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1])

    # Act
    result = linked_list.remove(1)
    after = to_py_list(linked_list)

    # Assert
    assert_that(result).is_true()
    assert_that(after).is_empty()


def test_remove_existing_returns_true_and_removes_first_occurrence(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3, 2, 4])

    # Act
    result = linked_list.remove(2)
    actual = to_py_list(linked_list)

    # Assert
    assert_that(result).is_true()
    assert_that(actual).is_equal_to([1, 3, 2, 4])


def test_remove_missing_returns_false_and_does_not_modify(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])
    before = to_py_list(linked_list)

    # Act
    result = linked_list.remove(999)
    after = to_py_list(linked_list)

    # Assert
    assert_that(result).is_false()
    assert_that(after).is_equal_to(before)


def test_extend_appends_all_values_in_order(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1])

    # Act
    linked_list.extend(iter([2, 3, 4]))
    actual = to_py_list(linked_list)

    # Assert
    assert_that(actual).is_equal_to([1, 2, 3, 4])


def test_extend_with_empty_iterator_is_noop(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2])

    # Act
    linked_list.extend(iter([]))
    actual = to_py_list(linked_list)

    # Assert
    assert_that(actual).is_equal_to([1, 2])


def test_index_of_existing_returns_first_index(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [10, 20, 30, 20])

    # Act
    index_10 = linked_list.index_of(10)
    index_20 = linked_list.index_of(20)
    index_30 = linked_list.index_of(30)

    # Assert
    assert_that(index_10).is_equal_to(0)
    assert_that(index_20).is_equal_to(1)
    assert_that(index_30).is_equal_to(2)


def test_index_of_missing_returns_none_on_non_empty(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])

    # Act
    actual = linked_list.index_of(999)

    # Assert
    assert_that(actual).is_none()


def test_index_of_missing_returns_none_on_empty(
        linked_list: LinkedListProtocol[int],
):
    # Arrange

    # Act
    actual = linked_list.index_of(999)

    # Assert
    assert_that(actual).is_none()


def test_index_of_missing_returns_none(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])

    # Act
    index = linked_list.index_of(999)

    # Assert
    assert_that(index).is_equal_to(None)


def test_insert_into_empty_at_zero_adds_value(
        linked_list: LinkedListProtocol[int],
):
    # Arrange

    # Act
    linked_list.insert(0, 42)
    actual = to_py_list(linked_list)

    # Assert
    assert_that(actual).is_equal_to([42])


def test_pop_back_single_element_returns_value_and_leaves_empty(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    linked_list.append(7)

    # Act
    value = linked_list.pop_back()
    actual = to_py_list(linked_list)

    # Assert
    assert_that(value).is_equal_to(7)
    assert_that(actual).is_empty()


def test_remove_on_empty_returns_false(
        linked_list: LinkedListProtocol[int],
):
    # Arrange

    # Act
    result = linked_list.remove(10)

    # Assert
    assert_that(result).is_false()


def test_remove_head_removes_first_node(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])

    # Act
    result = linked_list.remove(1)
    actual = to_py_list(linked_list)

    # Assert
    assert_that(result).is_true()
    assert_that(actual).is_equal_to([2, 3])


def test_remove_tail_removes_last_node(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])

    # Act
    result = linked_list.remove(3)
    actual = to_py_list(linked_list)

    # Assert
    assert_that(result).is_true()
    assert_that(actual).is_equal_to([1, 2])


def test_index_of_empty_returns_none(
        linked_list: LinkedListProtocol[int],
):
    # Arrange

    # Act
    index = linked_list.index_of(1)

    # Assert
    assert_that(index).is_equal_to(None)


def test_mutations_preserve_indices(
        linked_list: LinkedListProtocol[int],
):
    # Arrange
    fill(linked_list, [1, 2, 3])

    # Act
    linked_list.insert(1, 9)
    linked_list.remove(2)
    list_after = to_py_list(linked_list)
    index_of_3 = linked_list.index_of(3)
    index_of_2 = linked_list.index_of(2)

    # Assert
    assert_that(list_after).is_equal_to([1, 9, 3])
    assert_that(index_of_3).is_equal_to(2)
    assert_that(index_of_2).is_equal_to(None)
