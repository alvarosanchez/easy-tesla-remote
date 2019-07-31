from threading import (
    Lock,
    Event,
)


class ThreadSafeCounter:
    """
    Thread safe counter to keep track of the number of threads ussing a
    resource.

    Can be used as context manager or function decorator to ensure that
    the counter is always updated.

    Attributes:
        - counter_is_zero: Event that is set when the counter reaches zero.
            It can be used to sync threads that require that no one is using
            the resource.
    """

    def __init__(self, initial_value=0, allow_below_zero=False):
        """
        Args:
            - initial_value (int=0): Initial value of the counter.
            - allow_below_zero (bool=False): Sets wether the counter will go
                below zero or not.
        """
        self._value = initial_value
        self._allow_below_zero = allow_below_zero
        self._lock = Lock()
        self.counter_is_zero = Event()
        self._set_is_zero_event()

    def increment(self):
        """
        Increment the counter by one.

        Thread safe.
        """
        with self._lock:
            self._value += 1
            self._set_is_zero_event()

    def decrement(self):
        """
        Decrement the counter by one.

        Thread safe.
        """
        with self._lock:
            self._value -= 1
            if not self._allow_below_zero and self._value < 0:
                self._value = 0
            self._set_is_zero_event()

    def _set_is_zero_event(self):
        if self._value == 0:
            self.counter_is_zero.set()
        else:
            self.counter_is_zero.clear()

    def get_value(self):
        """
        Get the current value of the counter.

        Thread safe.
        """
        with self._lock:
            return self._value

    def __enter__(self):
        self.increment()
        return self

    def __exit__(self, type, value, traceback):
        self.decrement()
        return False

    def count_access(self, func):
        """
        Function decorator. Increase the counter on function invocation and
        decrease it when the function exits.
        """
        def decorator():
            with self:
                return func
        return decorator
