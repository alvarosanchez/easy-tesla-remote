from threading import (
    Lock,
    Event,
)


class ThreadSafeCounter:

    def __init__(self, initial_value=0, allow_below_zero=False):
        self._value = initial_value
        self._allow_below_zero = allow_below_zero
        self._lock = Lock()
        self.counter_is_zero = Event()
        self.counter_is_zero.set()

    def increment(self, ammount=1):
        with self._lock:
            self._value += ammount

    def decrement(self, ammount=1):
        with self._lock:
            self._value -= ammount
            
            if not self._allow_below_zero and self._value < 0:
                self._value = 0
            
            if self._value == 0:
                self.counter_is_zero.set()
            else:
                self.counter_is_zero.clear()

    def get_value(self):
        with self._lock:
            return self._value

    def __enter__(self):
        self.increment()
        return self

    def __exit__(self, type, value, traceback):
        self.decrement()
        return False

    def count(self, func):
        def decorator():
            with self:
                return func
        return decorator
