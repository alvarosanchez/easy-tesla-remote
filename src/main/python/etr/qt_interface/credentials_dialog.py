import logging

from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
)
from PyQt5.QtCore import pyqtSignal
from .auto_generated.credentials_dialog_auto import Ui_CredentialsDialog
from .util.engine_signals import EngineSignals

from engine.app_engine import EngineValidationError


logger = logging.getLogger(__name__)


class CredentialsDialog(QDialog, Ui_CredentialsDialog):

    def __init__(self, app_engine, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        
        self.app_engine = app_engine
        self.engine_signals = EngineSignals(app_engine, self)

        self.engine_signals.credentials_result.connect(self._on_engine_credentials_result)
        self.engine_signals.api_switched.connect(self.accept)

        self.buttonBox.accepted.connect(self._on_accepted)
        self.buttonBox.rejected.connect(self.reject)
        self.DemoMode.clicked.connect(self._on_demo_mode)
        self.finished.connect(self._on_finished)

    def _on_accepted(self):
        logger.debug('Sending credentials to the engine')
        try:
            self.switch_input_status(False)
            self.show_message('')
            self.app_engine.load_credentials(
                self.get_user_name(),
                self.get_password(),
                self.get_token()
            )
        except EngineValidationError as error:
            logger.debug("Credentials didn't pass validation")
            self.switch_input_status(True)
            self.show_message(str(error))

    def _on_finished(self):
        logger.debug('CredentialsDialog closed unwiring engine events')
        self.engine_signals.unwire_events()

    def _on_demo_mode(self):
        logger.debug('Switching to demo mode')
        self.switch_input_status(False)
        self.app_engine.enable_demo_mode()

    def _on_engine_credentials_result(self, command_id, response, result, error):
        logger.debug(f'Credentials result {command_id}, {result}, {error}')
        if result:
            self.accept()
        else:
            self.show_message(error)
            self.switch_input_status(True)

    def switch_input_status(self, input_enabled):
        self.DemoMode.setEnabled(input_enabled)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(input_enabled)
        self.buttonBox.button(QDialogButtonBox.Cancel).setEnabled(input_enabled)
        self.userName.setEnabled(input_enabled)
        self.userPassword.setEnabled(input_enabled)
        self.apiToken.setEnabled(input_enabled)

    def get_user_name(self):
        return self.userName.text()

    def get_password(self):
        return self.userPassword.text()

    def get_token(self):
        return self.apiToken.text()

    def show_message(self, message):
        self.message.setText(message)
        self.TokenMessage.setText(message)
