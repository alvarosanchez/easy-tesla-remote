import logging

from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)


logger = logging.getLogger(__name__)


class EngineSignals(QObject):
    """
    Wrapper to turn engine events into QT signals.

    This class is usefull to make sure that the engine
    events are processed by QT's event loop.
    """

    api_switched = pyqtSignal(bool)
    command_completed = pyqtSignal(str, str, dict, bool, str)
    credentials_required = pyqtSignal()
    credentials_result = pyqtSignal(str, dict, bool, str)
    new_frames_ready = pyqtSignal(list)
    poll_starting = pyqtSignal()
    poll_stopped = pyqtSignal()
    poll_stopping = pyqtSignal()
    request_demo_api = pyqtSignal()
    request_real_api = pyqtSignal()

    def __init__(self, app_engine, parent=None):
        super().__init__(parent=parent)
        self._app_engine = app_engine
        self._event_mappings = {
            app_engine.events.API_SWITCHED: self._on_engine_api_switched,
            app_engine.events.COMMAND_COMPLETED: self._on_engine_command_completed,
            app_engine.events.CREDENTIALS_REQUIRED: self._on_engine_credentials_required,
            app_engine.events.CREDENTIALS_RESULT: self._on_engine_credentials_result,
            app_engine.events.NEW_FRAMES_READY: self._on_engine_new_frames,
            app_engine.events.POLL_STARTING: self._on_engine_poll_starting,
            app_engine.events.POLL_STOPPED: self._on_engine_poll_stopped,
            app_engine.events.POLL_STOPPING: self._on_engine_poll_stopping,
            app_engine.events.REQUEST_DEMO_API: self._on_engine_request_demo_api,
            app_engine.events.REQUEST_REAL_API: self._on_engine_request_real_api
        }
        self.wire_events()

    def wire_events(self):
        for key in self._event_mappings:
            self._app_engine.register_handler(key, self._event_mappings[key])

    def unwire_events(self):
        for key in self._event_mappings:
            self._app_engine.unregister_handler(key, self._event_mappings[key])

    def _on_engine_command_completed(self,  command_id, command_name, response, result, error):
        logger.debug(f'Received completed event for command with id {command_id}')
        self.command_completed.emit(command_id, command_name, response, result, error)

    def _on_engine_credentials_required(self):
        logger.debug('Credentias required received')
        self.credentials_required.emit()

    def _on_engine_credentials_result(self, command_id, response, result, error):
        logger.debug(f'Received credentials result with id {command_id}')
        self.credentials_result.emit(command_id, response, result, error)

    def _on_engine_new_frames(self, frames):
        logger.debug('New frames received')
        self.new_frames_ready.emit(frames)

    def _on_engine_poll_starting(self):
        logger.debug('Engine poll starting received')
        self.poll_starting.emit()

    def _on_engine_poll_stopped(self):
        logger.debug('Engine poll stopped received')
        self.poll_stopped.emit()

    def _on_engine_poll_stopping(self):
        logger.debug('Engine poll stopping received')
        self.poll_stopping.emit()
    
    def _on_engine_request_demo_api(self):
        logger.debug('Demo API request received')
        self.request_demo_api.emit()

    def _on_engine_request_real_api(self):
        logger.debug('Real API request received')
        self.request_real_api.emit()

    def _on_engine_api_switched(self, is_demo):
        logger.debug('Api switched received')
        self.api_switched.emit(is_demo)
