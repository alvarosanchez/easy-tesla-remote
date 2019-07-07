"""
Tests for etr.controllers.util.tesla_api
"""
import json
import pytest
import requests_mock
from etr.engine.util.thread_safe_counter import ThreadSafeCounter


def test_context_manager():
    counter = ThreadSafeCounter()
    with counter:
        assert counter.get_value() == 1
    assert counter.get_value() == 0


def test_decorator():
    counter = ThreadSafeCounter()

    @counter.count
    def some_function():
        assert counter.get_value() == 1

    some_function()

    assert counter.get_value() == 0
