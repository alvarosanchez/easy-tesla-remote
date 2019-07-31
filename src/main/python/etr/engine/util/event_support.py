import logging


logger = logging.getLogger(__name__)


class EventSupportError(Exception):
    pass


class EventSupport:
    """
    Base class for classes that need to raise events.

    Attributes:
        - supported_events (list(string)): names of the class supported events.
        - intercept_exceptions (bool=True): sets whether the exceptions raised
            by the event handlers will be intercepted or let to go up.
    """

    def __init__(self, supported_events=[]):
        """
        Args:
            - supported_events (list(str)): names of the class supported events.
        """
        self._event_handlers = {}
        self.supported_events = supported_events
        self.intercept_exceptions = True

    def _validate_event_name(self, event_name):
        if event_name not in self.supported_events:
            raise EventSupportError(f'Event {event_name} not supported')

    def register_handler(self, event_name, handler_function):
        """
        Register a handler function for an event.

        Args:
            - event_name (str): name of the event. It must exist in the
                supported events list.
            - handler_function (method): function that will be invoked when the
                event ocurs.
        """
        self._validate_event_name(event_name)
        value = self._event_handlers.setdefault(event_name, [])

        if handler_function not in value:
             value.append(handler_function)

    def unregister_handler(self, event_name, handler_function):
        """
        Unregister an event's handler function.

        Args:
            - event_name (str): name of the event. It must exist in the
                supported events list.
            - handler_function (method): function that will be unregistered.
        """
        self._validate_event_name(event_name)
        value = self._event_handlers.setdefault(event_name, [])

        if handler_function in value:
            value.remove(handler_function)

    def handles(self, event_name):
        """
        Register by decorating a handler function for an event.

        Args:
            event_name (str): name of the event. It must exist in the supported
            events list.
        """
        def decorator(f):
            self.register_handler(event_name, f)
            return f
        return decorator

    def raise_event(self, event_name, *args, **kwargs):
        """
        Invoke all the event handlers for an event.

        The intercept_exceptions instance attribute controls if this method
        catches and logs the exceptions raised by the event handlers or lets
        them go up.

        Args:
            event_name (str): name of the event. It must exist in the supported
            events list.
        """
        self._validate_event_name(event_name)
        handlers = self._event_handlers.setdefault(event_name, [])

        for handler in handlers:
            try:
                handler(*args, **kwargs)
            except Exception as error:
                if self.intercept_exceptions:
                    logger.error(error)
                else:
                    raise
