from itertools import islice

import pytest
from assertpy import assert_that

from data_structures.dequeue import Dequeue
from data_structures.queue import Queue
from data_structures.queue_protocol import QueueProtocol


@pytest.fixture(params=[Queue, Dequeue], ids=["queue", "dequeue"])
def queue(request: pytest.FixtureRequest) -> QueueProtocol[int]:
    """
    System-under-test factory.

    These tests target the behavioral contract implied by `QueueProtocol`.
    Implement `Queue` in `data_structures/queue.py` to make them pass.

    A Queue is a FIFO (First-In, First-Out) collection:
      - enqueue → adds to the back
      - dequeue → removes & returns from the front
      - peek    → inspects the front without removing it
    """
    queue_cls = request.param
    return queue_cls[int]()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def drain(q: QueueProtocol[int], *, max_items: int = 1_000) -> list[int]:
    """Dequeue every element and return them in dequeue order."""
    result: list[int] = []
    while len(q) and len(result) < max_items:
        result.append(q.dequeue())
    return result


def to_list(q: QueueProtocol[int], *, max_items: int = 1_000) -> list[int]:
    """Snapshot via __iter__ (front → back), capped to catch infinite loops."""
    items = list(islice(iter(q), max_items + 1))
    assert_that(len(items)).described_as(
        "Queue iteration did not terminate; possible cycle."
    ).is_less_than_or_equal_to(max_items)
    return items


# ---------------------------------------------------------------------------
# __len__ / __bool__
# ---------------------------------------------------------------------------

def test_empty_queue_has_len_zero(queue: QueueProtocol[int]):
    # Arrange / Act / Assert
    assert_that(len(queue)).is_equal_to(0)


def test_empty_queue_is_falsy(queue: QueueProtocol[int]):
    # Arrange / Act / Assert
    assert_that(bool(queue)).is_false()


def test_nonempty_queue_is_truthy(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)

    # Act / Assert
    assert_that(bool(queue)).is_true()


def test_len_tracks_enqueues(queue: QueueProtocol[int]):
    # Arrange / Act
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)

    # Assert
    assert_that(len(queue)).is_equal_to(3)


def test_len_decrements_on_dequeue(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)
    queue.enqueue(2)

    # Act
    queue.dequeue()

    # Assert
    assert_that(len(queue)).is_equal_to(1)


def test_len_back_to_zero_after_all_dequeues(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)
    queue.enqueue(2)

    # Act
    queue.dequeue()
    queue.dequeue()

    # Assert
    assert_that(len(queue)).is_equal_to(0)


# ---------------------------------------------------------------------------
# enqueue / dequeue — FIFO semantics
# ---------------------------------------------------------------------------

def test_enqueue_then_dequeue_returns_same_value(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(42)

    # Act
    value = queue.dequeue()

    # Assert
    assert_that(value).is_equal_to(42)


def test_dequeue_returns_fifo_order(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)

    # Act
    order = drain(queue)

    # Assert — first enqueued comes out first
    assert_that(order).is_equal_to([1, 2, 3])


def test_dequeue_on_empty_raises_index_error(queue: QueueProtocol[int]):
    # Arrange / Act / Assert
    assert_that(queue.dequeue).raises(IndexError).when_called_with()


def test_dequeue_on_empty_after_draining_raises_index_error(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)
    queue.dequeue()

    # Act / Assert
    assert_that(queue.dequeue).raises(IndexError).when_called_with()


def test_interleaved_enqueue_dequeue_preserves_fifo(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)
    queue.enqueue(2)

    # Act
    first = queue.dequeue()  # should be 1
    queue.enqueue(3)
    second = queue.dequeue()  # should be 2
    third = queue.dequeue()  # should be 3

    # Assert
    assert_that(first).is_equal_to(1)
    assert_that(second).is_equal_to(2)
    assert_that(third).is_equal_to(3)


# ---------------------------------------------------------------------------
# peek
# ---------------------------------------------------------------------------

def test_peek_returns_front_element(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(7)

    # Act
    front = queue.peek()

    # Assert
    assert_that(front).is_equal_to(7)


def test_peek_does_not_remove_element(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(7)

    # Act
    queue.peek()

    # Assert
    assert_that(len(queue)).is_equal_to(1)
    assert_that(queue.dequeue()).is_equal_to(7)


def test_peek_always_shows_the_oldest_element(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)
    queue.enqueue(2)

    # Act / Assert — front stays 1 even after a second enqueue
    assert_that(queue.peek()).is_equal_to(1)

    queue.enqueue(3)
    assert_that(queue.peek()).is_equal_to(1)


def test_peek_on_empty_raises_index_error(queue: QueueProtocol[int]):
    # Arrange / Act / Assert
    assert_that(queue.peek).raises(IndexError).when_called_with()


def test_peek_after_dequeue_reflects_new_front(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)
    queue.enqueue(2)

    # Act
    queue.dequeue()
    front = queue.peek()

    # Assert
    assert_that(front).is_equal_to(2)


# ---------------------------------------------------------------------------
# __iter__ — snapshot, front to back, non-destructive
# ---------------------------------------------------------------------------

def test_iter_on_empty_yields_nothing(queue: QueueProtocol[int]):
    # Arrange / Act
    items = to_list(queue)

    # Assert
    assert_that(items).is_empty()


def test_iter_yields_front_to_back(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)

    # Act
    items = to_list(queue)

    # Assert — 1 was enqueued first, so it is at the front
    assert_that(items).is_equal_to([1, 2, 3])


def test_iter_does_not_modify_queue(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)

    # Act
    _ = to_list(queue)

    # Assert
    assert_that(len(queue)).is_equal_to(3)
    assert_that(queue.dequeue()).is_equal_to(1)


def test_iter_after_dequeue_reflects_current_state(queue: QueueProtocol[int]):
    # Arrange
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    queue.dequeue()

    # Act
    items = to_list(queue)

    # Assert
    assert_that(items).is_equal_to([2, 3])


# ---------------------------------------------------------------------------
# Capacity / Resizing
# ---------------------------------------------------------------------------

def test_enqueue_beyond_initial_capacity_triggers_resize(queue: QueueProtocol[int]):
    # Arrange
    for i in range(10):
        queue.enqueue(i)

    # Act
    items = to_list(queue)

    # Assert
    assert_that(len(queue)).is_equal_to(10)
    assert_that(items).is_equal_to(list(range(10)))


def test_interleaved_operations_forcing_wrap_around_and_resize(queue: QueueProtocol[int]):
    # Arrange
    for i in range(4):
        queue.enqueue(i)

    queue.dequeue()
    queue.dequeue()

    # Enqueue more to force a resize while head > 0 (testing circular array growth)
    for i in range(4, 10):
        queue.enqueue(i)

    # Act
    items = to_list(queue)

    # Assert
    assert_that(len(queue)).is_equal_to(8)
    assert_that(items).is_equal_to(list(range(2, 10)))
