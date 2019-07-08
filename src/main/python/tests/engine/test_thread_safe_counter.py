"""
Tests for etr.controllers.util.thread_safe_counter
"""
import pytest

from etr.engine.util.thread_safe_counter import ThreadSafeCounter


def test_init_updates_event():
    counter01 = ThreadSafeCounter(0)
    counter02 = ThreadSafeCounter(1)

    assert counter01.counter_is_zero.is_set()
    assert not counter02.counter_is_zero.is_set()


def test_increment_updates_event():
    counter = ThreadSafeCounter(0)
    counter.increment()

    assert not counter.counter_is_zero.is_set()


def test_decrement_updates_event():
    counter = ThreadSafeCounter(1)
    counter.decrement()

    assert counter.counter_is_zero.is_set()


def test_increment():
    counter = ThreadSafeCounter(0)
    counter.increment()
    counter.increment()
    counter.increment()

    assert counter._value == 3


def test_decrement():
    counter = ThreadSafeCounter(3)
    counter.decrement()
    counter.decrement()
    counter.decrement()

    assert counter._value == 0


def test_decrement_negative_allowed():
    counter = ThreadSafeCounter(1, True)
    counter.decrement()
    counter.decrement()
    counter.decrement()

    assert counter._value == -2


def test_decrement_negative_not_allowed():
    counter = ThreadSafeCounter(1, False)
    counter.decrement()
    counter.decrement()
    counter.decrement()

    assert counter._value == 0


def test_get_value():
    counter = ThreadSafeCounter(0)
    counter.increment()
    counter.increment()
    counter.increment()

    assert counter._value == counter.get_value()


def test_context_manager():
    counter = ThreadSafeCounter()
    with counter:
        assert counter.get_value() == 1
    assert counter.get_value() == 0


def test_decorator():
    counter = ThreadSafeCounter()

    @counter.count_access
    def some_function():
        assert counter.get_value() == 1

    some_function()

    assert counter.get_value() == 0
