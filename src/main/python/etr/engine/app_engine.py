import concurrent.futures
import logging
import re
import uuid

from threading import Event

from .util.event_support import EventSupport
from .util.option_codes import (
    translate_codes,
    VALID_CHARS,
    SEPARATOR_CHARS,
)
from .util.thread_safe_counter import ThreadSafeCounter
from .tesla.api import TeslaApiError
from .tesla.endpoints import SupportedEndpoints
from . import __version__


logger = logging.getLogger(__name__)


class EngineValidationError(Exception):
    pass


class EngineEvents:
    API_SWITCHED = 'api_switched'
    COMMAND_COMPLETED = 'command_completed'
    CREDENTIALS_REQUIRED = 'credentials_required'
    CREDENTIALS_RESULT = 'credentials_result'
    NEW_FRAMES_READY = 'new_frames_ready'
    POLL_STARTING = 'poll_starting'
    POLL_STOPPED = 'poll_stopped'
    POLL_STOPPING = 'poll_stopping'
    REQUEST_DEMO_API = 'request_demo_api'
    REQUEST_REAL_API = 'request_real_api'

    @classmethod
    def to_array(cls):
        return [
            cls.API_SWITCHED,
            cls.COMMAND_COMPLETED,
            cls.CREDENTIALS_REQUIRED,
            cls.CREDENTIALS_RESULT,
            cls.NEW_FRAMES_READY,
            cls.POLL_STARTING,
            cls.POLL_STOPPED,
            cls.POLL_STOPPING,
            cls.REQUEST_DEMO_API,
            cls.REQUEST_REAL_API
        ]


class AppEngine(EventSupport):

    def __init__(self, tesla_api):
        super().__init__(EngineEvents.to_array())
        self.commands = SupportedEndpoints
        self.events = EngineEvents
        self._terminate_poll = Event()
        self._poll_terminated = Event()
        self._poll_terminated.set()

        self._api_active_accesses = ThreadSafeCounter()
        self._api_not_updating = Event()
        self._api_not_updating.set()

        self._tesla_api = tesla_api
        self.poll_rate = 3
        self._thread_pool = concurrent.futures.ThreadPoolExecutor()

    def _thread_api_poller(self):
        logger.info(f'Poller thread started')
        self.raise_event(self.events.POLL_STARTING)
        first_loop = True
        while first_loop or not self._terminate_poll.wait(self.poll_rate):
            self._api_not_updating.wait()
            with self._api_active_accesses:
                first_loop = False
                logger.info(f'Poll tick started')
                new_frames = []
                future_results = []

                try:
                    cars = self._tesla_api.send_request(self._tesla_api.urls.VEHICLE_LIST)
                except TeslaApiError as error:
                    if error.status_code == 401:
                        self.raise_event(self.events.CREDENTIALS_REQUIRED)
                        self._terminate_poll.set()
                        break
                    else:
                        raise

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    for car in cars:
                        if car['state'] == 'online':
                            future_results.append(
                                executor.submit(
                                    self._tesla_api.send_request,
                                    self._tesla_api.urls.VEHICLE_DATA,
                                    car['id']
                                )
                            )
                        else:
                            if car['state'] != 'asleep' and car['state'] != 'offline':
                                logger.critical(car['state'])
                            new_frames.append(car)

            for future in future_results:
                try:
                    new_frames.insert(0, future.result())
                except Exception as exception:
                    logger.error(exception)

            if len(new_frames) > 0:
                self.raise_event(self.events.NEW_FRAMES_READY, frames=new_frames)

            logger.info(f'Poll tick completed')

        self._poll_terminated.set()
        logger.info(f'Poller terminated')
        self.raise_event(self.events.POLL_STOPPED)

    def _thread_api_command(self, command_id, command_name, *args):
        logger.info(f'Api command thread started')
        try:
            self._api_not_updating.wait()
            with self._api_active_accesses:
                result = self._tesla_api.send_request(command_name, *args)
            self.raise_event(
                self.events.COMMAND_COMPLETED,
                command_id,
                command_name,
                result,
                True,
                ''
            )
        except Exception as error:
            logger.error(error)
            self.raise_event(
                self.events.COMMAND_COMPLETED,
                command_id,
                command_name,
                {},
                False,
                str(error)
            )
        logger.info(f'Api command thread completed')

    def _thread_credentials_load(self, command_id, user_name, password, token):
        logger.info(f'Credentials load started')
        self._api_not_updating.wait()
        self._api_not_updating.clear()
        self._api_active_accesses.counter_is_zero.wait()

        event_args = []

        try:
            if token:
                # Test the token
                self._tesla_api.token = token
                self._tesla_api.send_request(self._tesla_api.urls.VEHICLE_LIST)
                result = { 'access_token': token }
            else:
                # No token so use the user and password to obtain a new one
                result = self._tesla_api.get_token(user_name, password)
                self._tesla_api.token = result['access_token']
            event_args = [self.events.CREDENTIALS_RESULT, command_id, result, True, '']
        except Exception as error:
            logger.error(error)
            event_args = [self.events.CREDENTIALS_RESULT, command_id, {}, False, str(error)]

        self._api_not_updating.set()
        self.raise_event(*event_args)
        logger.info(f'Credentials load completed')

    def poll_start(self):
        if self._poll_terminated.is_set():
            if not self._tesla_api.token:
                logger.debug('poll_start invoked but credentials are required')
                self.raise_event(self.events.CREDENTIALS_REQUIRED)
            else:
                logger.debug('poll_start invoked')
                self._poll_terminated.clear()
                self._terminate_poll.clear()
                self._thread_pool.submit(self._thread_api_poller)
        else:
            logger.debug('poll_start invoked but terminated flag is not set')

    def poll_stop(self):
        self._terminate_poll.set()
        self.raise_event(self.events.POLL_STOPPING)

    def send_car_command(self, command_name, *args):
        command_id = uuid.uuid4().hex

        self._thread_pool.submit(
            self._thread_api_command,
            command_id,
            command_name,
            *args
        )

        return command_id

    def load_credentials(self, user_name=None, password=None, token=None):
        if not user_name and not token:
            raise EngineValidationError('The user name can not be empty')
        if not password and not token:
            raise EngineValidationError('The password can not be empty')

        command_id = uuid.uuid4().hex
        self._thread_pool.submit(self._thread_credentials_load, command_id, user_name, password, token)
        return command_id

    def get_current_token(self):
        return self._tesla_api.token

    def sanitize_option_codes(self, codes):
        return re.sub(f'[^{VALID_CHARS}]', '', codes.upper())

    def translate_option_codes(self, codes):
        sanitized_codes = self.sanitize_option_codes(codes)
        return translate_codes(sanitized_codes)

    def switch_api(self, new_api, is_demo=False):
        logger.info(f'Trying to switch api. Demo {is_demo}')
        self._api_not_updating.wait()
        self._api_not_updating.clear()
        self._api_active_accesses.counter_is_zero.wait()
        logger.info(f'Switching api now. Demo {is_demo}')
        self._tesla_api = new_api
        self._api_not_updating.set()
        self.raise_event(self.events.API_SWITCHED, is_demo)

    def enable_demo_mode(self):
        self.raise_event(self.events.REQUEST_DEMO_API)

    def enable_real_mode(self):
        self.raise_event(self.events.REQUEST_REAL_API)

    def reset_api_token(self):
        self._api_not_updating.wait()
        self._api_not_updating.clear()
        self._api_active_accesses.counter_is_zero.wait()
        self._tesla_api.token = ''
        self._api_not_updating.set()

    def get_engine_version(self):
        return __version__
