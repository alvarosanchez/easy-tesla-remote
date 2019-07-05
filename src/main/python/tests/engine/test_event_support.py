"""
Tests for etr.controllers.util.events
"""
import pytest
from etr.engine.util.event_support import (
    EventSupportError,
    EventSupport,
)


@pytest.fixture
def class_with_events():
    return EventSupport(['event_1', 'event_2', 'event_3'])


@pytest.fixture
def invocation_test_class():
    class raise_event_checker:
        def __init__(self, test_class):
            self.handler_01_invoked = 0
            self.handler_01_args = None
            self.handler_01_kwargs = None
            self.handler_02_invoked = 0
            self.handler_02_args = None
            self.handler_02_kwargs = None
            self.handler_03_invoked = 0
            self.handler_03_args = None
            self.handler_03_kwargs = None
    
        def handler_function_01(self, *args, **kwargs):
            self.handler_01_invoked += 1
            self.handler_01_args = args
            self.handler_01_kwargs = kwargs

        def handler_function_02(self, *args, **kwargs):
            self.handler_02_invoked += 1
            self.handler_02_args = args
            self.handler_02_kwargs = kwargs
        
        def handler_function_03(self, *args, **kwargs):
            self.handler_03_invoked += 1
            self.handler_03_args = args
            self.handler_03_kwargs = kwargs
    
    return raise_event_checker


def test_constructor(class_with_events):
    assert len(class_with_events._event_handlers.keys()) == 0
    assert 'event_1' in class_with_events.supported_events
    assert 'event_2' in class_with_events.supported_events
    assert 'event_3' in class_with_events.supported_events


def test_register_handler_not_supported(class_with_events):
    with pytest.raises(EventSupportError):
        class_with_events.register_handler('unsupported', lambda: True)


def test_register_handler_supported(class_with_events):
    def handler_function():
        pass
    
    class_with_events.register_handler('event_2', handler_function)

    assert handler_function in class_with_events._event_handlers['event_2']


def test_register_handler_duplicated(class_with_events):
    def handler_function():
        pass
    
    class_with_events.register_handler('event_2', handler_function)
    class_with_events.register_handler('event_2', handler_function)

    assert len(class_with_events._event_handlers['event_2']) == 1


def test_unregister_handler_not_supported(class_with_events):
    with pytest.raises(EventSupportError):
        class_with_events.unregister_handler('unsupported', lambda: True)


def test_unregister_handler(class_with_events):
    def handler_function():
        pass
    
    class_with_events.register_handler('event_2', handler_function)
    class_with_events.unregister_handler('event_2', handler_function)

    assert handler_function not in class_with_events._event_handlers['event_2']


def test_unregister_non_registered_handler(class_with_events):
    def handler_function():
        pass
    
    class_with_events.register_handler('event_2', lambda: True)
    
    class_with_events.unregister_handler('event_2', handler_function)
    class_with_events.unregister_handler('event_1', lambda: True)

    assert handler_function not in class_with_events._event_handlers['event_2']


def test_handles_decorator(class_with_events):
    @class_with_events.handles('event_2')
    def test_function():
        pass
    
    assert test_function in class_with_events._event_handlers['event_2']


def test_raise_event(class_with_events, invocation_test_class):
    test_class = invocation_test_class(class_with_events)
    class_with_events.register_handler('event_2', test_class.handler_function_01)
    class_with_events.register_handler('event_2', test_class.handler_function_02)
    class_with_events.register_handler('event_3', test_class.handler_function_03)

    class_with_events.raise_event('event_2')

    assert test_class.handler_01_invoked == 1
    assert test_class.handler_02_invoked == 1
    assert test_class.handler_03_invoked == 0


def test_raise_event_args(class_with_events, invocation_test_class):
    test_class = invocation_test_class(class_with_events)
    class_with_events.register_handler('event_2', test_class.handler_function_01)
    class_with_events.register_handler('event_2', test_class.handler_function_02)

    class_with_events.raise_event('event_2', 'arg_01', 'arg_02')

    assert len(test_class.handler_01_args) == 2
    assert 'arg_01' in test_class.handler_01_args
    assert 'arg_02' in test_class.handler_01_args

    assert len(test_class.handler_02_args) == 2
    assert 'arg_01' in test_class.handler_02_args
    assert 'arg_02' in test_class.handler_02_args


def test_raise_event_kwargs(class_with_events, invocation_test_class):
    test_class = invocation_test_class(class_with_events)
    class_with_events.register_handler('event_2', test_class.handler_function_01)
    class_with_events.register_handler('event_2', test_class.handler_function_02)

    class_with_events.raise_event('event_2', kwarg01='kwarg_01', kwarg02='kwarg_02')

    assert len(test_class.handler_01_kwargs.keys()) == 2
    assert 'kwarg01' in test_class.handler_01_kwargs
    assert test_class.handler_01_kwargs['kwarg01'] == 'kwarg_01'
    assert 'kwarg02' in test_class.handler_01_kwargs
    assert test_class.handler_01_kwargs['kwarg02'] == 'kwarg_02'

    assert len(test_class.handler_02_kwargs.keys()) == 2
    assert 'kwarg01' in test_class.handler_02_kwargs
    assert test_class.handler_02_kwargs['kwarg01'] == 'kwarg_01'
    assert 'kwarg02' in test_class.handler_02_kwargs
    assert test_class.handler_02_kwargs['kwarg02'] == 'kwarg_02'
