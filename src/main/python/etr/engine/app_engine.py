import concurrent.futures
import logging
import uuid

from threading import Event

from .util.event_support import EventSupport
from .util.option_codes import translate_codes
from .tesla.api import TeslaApiError


logger = logging.getLogger(__name__)


class EngineValidationError(Exception):
    pass


class EngineCommands:
    WAKE_UP = 'wake_up'
    FLASH_LIGHTS = 'flash_lights'
    HONK = 'honk'


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
        self.commands = EngineCommands
        self.events = EngineEvents
        self.terminate = Event()
        self.terminated = Event()
        self.terminated.set()
        self._tesla_api = tesla_api
        self.poll_rate = 3
        self.thread_pool = concurrent.futures.ThreadPoolExecutor()

    def _thread_api_poller(self):
        logger.info(f'Poller thread started')
        self.raise_event(self.events.POLL_STARTING)
        first_loop = True
        while first_loop or not self.terminate.wait(self.poll_rate):
            first_loop = False
            logger.info(f'Poll tick started')
            new_frames = []
            future_results = []

            try:
                cars = self._tesla_api.get_vehicles()
            except TeslaApiError as error:
                if error.status_code == 401:
                    self.raise_event(self.events.CREDENTIALS_REQUIRED)
                    self.terminate.set()
                    break
                else:
                    raise

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for car in cars:
                    if car['state'] == 'online':
                        future_results.append(
                            executor.submit(self._tesla_api.get_vehicle_data, car['id'])
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

        self.terminated.set()
        logger.info(f'Poller terminated')
        self.raise_event(self.events.POLL_STOPPED)

    def _thread_api_command(self, command_id, command_name, function, *args):
        try:
            result = function(*args)
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

    def _thread_credentials_load(self, command_id, user_name, password, token):
        logger.info(f'Credentials load started')
        try:
            if token:
                # Test the token
                self._tesla_api.token = token
                self._tesla_api.get_vehicles()
                result = { 'access_token': token }
            else:
                # No token so use the user and password to obtain a new one
                result = self._tesla_api.get_token(user_name, password)
                self._tesla_api.token = result['access_token']
            self.raise_event(self.events.CREDENTIALS_RESULT, command_id, result, True, '')
        except Exception as error:
            logger.error(error)
            self.raise_event(self.events.CREDENTIALS_RESULT, command_id, {}, False, str(error))
        logger.info(f'Credentials load completed')

    def poll_start(self):
        if self.terminated.is_set():
            if not self._tesla_api.token:
                logger.debug('poll_start invoked but credentials are required')
                self.raise_event(self.events.CREDENTIALS_REQUIRED)
            else:
                logger.debug('poll_start invoked')
                self.terminated.clear()
                self.terminate.clear()
                self.thread_pool.submit(self._thread_api_poller)
        else:
            logger.debug('poll_start invoked but terminated flag is not set')

    def poll_stop(self):
        self.terminate.set()
        self.raise_event(self.events.POLL_STOPPING)

    def send_car_command(self, command_name, *args):
        command_id = uuid.uuid4().hex

        function_map = {
            self.commands.WAKE_UP: self._tesla_api.wake_up,
            self.commands.HONK: self._tesla_api.honk,
            self.commands.FLASH_LIGHTS: self._tesla_api.flash_lights
        }

        if command_name not in function_map:
            raise EngineValidationError(f'{command_name} command not supported')

        self.thread_pool.submit(
            self._thread_api_command, 
            command_id,
            command_name,
            function_map[command_name], 
            *args
        )

        return command_id

    def load_credentials(self, user_name=None, password=None, token=None):
        if not user_name and not token:
            raise EngineValidationError('The user name can not be empty')
        if not password and not token:
            raise EngineValidationError('The password can not be empty')

        command_id = uuid.uuid4().hex
        self.thread_pool.submit(self._thread_credentials_load, command_id, user_name, password, token)
        return command_id

    def get_current_token(self):
        return self._tesla_api.token

    def translate_option_codes(self, codes):
        return translate_codes(codes)

    def switch_api(self, new_api, is_demo=False):
        logger.info(f'Switching api. Demo {is_demo}')
        # TO-DO: make this thread safe
        self._tesla_api = new_api
        self.raise_event(self.events.API_SWITCHED, is_demo)

    def enable_demo_mode(self):
        self.raise_event(self.events.REQUEST_DEMO_API)

    def enable_real_mode(self):
        self.raise_event(self.events.REQUEST_REAL_API)
