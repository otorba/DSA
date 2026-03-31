from itertools import islice

import pytest
from assertpy import assert_that

from data_structures.stack import Stack
from data_structures.stack_protocol import StackProtocol


@pytest.fixture
def stack() -> StackProtocol[int]:
    """
    System-under-test factory.

    These tests target the behavioural contract implied by `StackProtocol`.
    Implement `Stack` in `data_structures/stack.py` to make them pass.

    A Stack is a LIFO (Last-In, First-Out) collection:
      - push  → adds to the top
      - pop   → removes & returns from the top
      - peek  → inspects the top without removing it
    """
    return Stack[int]()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def drain(s: StackProtocol[int], *, max_items: int = 1_000) -> list[int]:
    """Pop every element and return them in pop order."""
    result: list[int] = []
    while len(s):
        result.append(s.pop())
    return result


def to_list(s: StackProtocol[int], *, max_items: int = 1_000) -> list[int]:
    """Snapshot via __iter__ (top → bottom), capped to catch infinite loops."""
    items = list(islice(iter(s), max_items + 1))
    assert_that(len(items)).described_as(
        "Stack iteration did not terminate; possible cycle."
    ).is_less_than_or_equal_to(max_items)
    return items


# ---------------------------------------------------------------------------
# __len__ / __bool__
# ---------------------------------------------------------------------------

def test_empty_stack_has_len_zero(stack: StackProtocol[int]):
    # Arrange / Act / Assert
    assert_that(len(stack)).is_equal_to(0)


def test_empty_stack_is_falsy(stack: StackProtocol[int]):
    # Arrange / Act / Assert
    assert_that(bool(stack)).is_false()


def test_nonempty_stack_is_truthy(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)

    # Act / Assert
    assert_that(bool(stack)).is_true()


def test_len_tracks_pushes(stack: StackProtocol[int]):
    # Arrange / Act
    stack.push(10)
    stack.push(20)
    stack.push(30)

    # Assert
    assert_that(len(stack)).is_equal_to(3)


def test_len_decrements_on_pop(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)
    stack.push(2)

    # Act
    stack.pop()

    # Assert
    assert_that(len(stack)).is_equal_to(1)


def test_len_back_to_zero_after_all_pops(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)
    stack.push(2)

    # Act
    stack.pop()
    stack.pop()

    # Assert
    assert_that(len(stack)).is_equal_to(0)


# ---------------------------------------------------------------------------
# push / pop — LIFO semantics
# ---------------------------------------------------------------------------

def test_push_then_pop_returns_same_value(stack: StackProtocol[int]):
    # Arrange
    stack.push(42)

    # Act
    value = stack.pop()

    # Assert
    assert_that(value).is_equal_to(42)


def test_pop_returns_lifo_order(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)
    stack.push(2)
    stack.push(3)

    # Act
    order = drain(stack)

    # Assert — last pushed comes out first
    assert_that(order).is_equal_to([3, 2, 1])


def test_pop_on_empty_raises_index_error(stack: StackProtocol[int]):
    # Arrange / Act / Assert
    assert_that(stack.pop).raises(IndexError).when_called_with()


def test_pop_on_empty_after_draining_raises_index_error(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)
    stack.pop()

    # Act / Assert
    assert_that(stack.pop).raises(IndexError).when_called_with()


def test_interleaved_push_pop_preserves_lifo(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)
    stack.push(2)

    # Act
    first_pop = stack.pop()  # should be 2
    stack.push(3)
    second_pop = stack.pop()  # should be 3
    third_pop = stack.pop()  # should be 1

    # Assert
    assert_that(first_pop).is_equal_to(2)
    assert_that(second_pop).is_equal_to(3)
    assert_that(third_pop).is_equal_to(1)


# ---------------------------------------------------------------------------
# peek
# ---------------------------------------------------------------------------

def test_peek_returns_top_element(stack: StackProtocol[int]):
    # Arrange
    stack.push(7)

    # Act
    top = stack.peek()

    # Assert
    assert_that(top).is_equal_to(7)


def test_peek_does_not_remove_element(stack: StackProtocol[int]):
    # Arrange
    stack.push(7)

    # Act
    stack.peek()

    # Assert
    assert_that(len(stack)).is_equal_to(1)
    assert_that(stack.pop()).is_equal_to(7)


def test_peek_always_shows_the_latest_push(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)
    stack.push(2)

    # Act / Assert
    assert_that(stack.peek()).is_equal_to(2)

    stack.push(3)
    assert_that(stack.peek()).is_equal_to(3)


def test_peek_on_empty_raises_index_error(stack: StackProtocol[int]):
    # Arrange / Act / Assert
    assert_that(stack.peek).raises(IndexError).when_called_with()


def test_peek_after_pop_reflects_new_top(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)
    stack.push(2)

    # Act
    stack.pop()
    top = stack.peek()

    # Assert
    assert_that(top).is_equal_to(1)


# ---------------------------------------------------------------------------
# __iter__ — snapshot, top to bottom, non-destructive
# ---------------------------------------------------------------------------

def test_iter_on_empty_yields_nothing(stack: StackProtocol[int]):
    # Arrange / Act
    items = to_list(stack)

    # Assert
    assert_that(items).is_empty()


def test_iter_yields_top_to_bottom(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)
    stack.push(2)
    stack.push(3)

    # Act
    items = to_list(stack)

    # Assert — 3 was pushed last, so it sits on top
    assert_that(items).is_equal_to([3, 2, 1])


def test_iter_does_not_modify_stack(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)
    stack.push(2)
    stack.push(3)

    # Act
    _ = to_list(stack)

    # Assert
    assert_that(len(stack)).is_equal_to(3)
    assert_that(stack.pop()).is_equal_to(3)


def test_iter_after_pop_reflects_current_state(stack: StackProtocol[int]):
    # Arrange
    stack.push(1)
    stack.push(2)
    stack.push(3)
    stack.pop()

    # Act
    items = to_list(stack)

    # Assert
    assert_that(items).is_equal_to([2, 1])
