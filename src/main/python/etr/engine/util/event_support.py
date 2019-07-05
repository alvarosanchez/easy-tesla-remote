import logging


logger = logging.getLogger(__name__)


class EventSupportError(Exception):
    pass


class EventSupport:
    """
    Base class for classes that need to raise events
    """

    def __init__(self, supported_events=[]):
        """
        :param supported_events: names of the class supported events
        """
        self._event_handlers = {}
        self.supported_events = supported_events
        self.intercept_exceptions = True

    def _validate_event_name(self, event_name):
        if event_name not in self.supported_events:
            raise EventSupportError(f'Event {event_name} not supported')

    def register_handler(self, event_name, handler_function):
        """
        Register a handler function for an event

        :param event_name: name of the event. It must exist in the supported
        events list
        :param handler_function: function that will be invoked when the event ocurs
        """
        self._validate_event_name(event_name)

        if event_name in self._event_handlers\
           and handler_function not in self._event_handlers[event_name]:
            self._event_handlers[event_name].append(handler_function)
        else:
            self._event_handlers[event_name] = [handler_function]

    def unregister_handler(self, event_name, handler_function):
        """
        Unregister an event's handler function

        :param event_name: name of the event. It must exist in the supported
        events list
        :param handler_function: function that will be unregistered
        """
        self._validate_event_name(event_name)

        if event_name in self._event_handlers\
           and handler_function in self._event_handlers[event_name]:
            self._event_handlers[event_name].remove(handler_function)

    def handles(self, event_name):
        """
        Register by decorating a handler function for an event

        :param event_name: name of the event. It must exist in the supported
        events list
        """
        def decorator(f):
            self.register_handler(event_name, f)
            return f
        return decorator

    def raise_event(self, event_name, *args, **kwargs):
        """
        Invoke all the event handlers for an event

        :param event_name: name of the event. It must exist in the supported
        events list 
        """
        self._validate_event_name(event_name)

        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                try:
                    handler(*args, **kwargs)
                except Exception as error:
                    if self.intercept_exceptions:
                        logger.error(error)
                    else:
                        raise
