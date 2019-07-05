import logging

from PyQt5.QtWidgets import (
    QMainWindow, 
    QMessageBox,
)

from .util.engine_signals import EngineSignals
from .auto_generated.main_window_auto import Ui_MainWindow
from .vehicle_view import VehicleView
from .credentials_dialog import CredentialsDialog
from .token_dialog import TokenDialog

from engine.app_engine import EngineValidationError


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app_engine, parent=None):
        super().__init__(parent=parent)
        self.app_engine = app_engine
        self.setupUi(self)

        self.pending_commands = []

        self.credentials_dialog = None

        self.engine_signals = EngineSignals(app_engine, self)
        self.engine_signals.credentials_required.connect(self._on_engine_credentials_required)
        self.engine_signals.poll_starting.connect(self._on_engine_poll_starting)
        self.engine_signals.poll_stopped.connect(self._on_engine_poll_stop)
        self.engine_signals.poll_stopping.connect(self._on_engine_poll_stop)
        self.engine_signals.credentials_result.connect(self._on_engine_credentials_result)
        self.engine_signals.command_completed.connect(self._on_engine_command_completed)
        self.engine_signals.api_switched.connect(self._on_engine_api_switched)

        self.actionExit.triggered.connect(self.close)
        self.actionLoad.triggered.connect(self._on_connect)
        self.actionDisconnect.triggered.connect(self._on_disconnect)
        self.actionGet_Account_Keys.triggered.connect(self._on_show_token)

    def showEvent(self, event):
        self._on_connect()

    def closeEvent(self, event):
        logger.info('Main window closed unwiring engine events')
        self.engine_signals.unwire_events()

    def show_dialog(self, text, icon=QMessageBox.Information):
        message_box = QMessageBox(self)
        message_box.setIcon(icon)
        message_box.setText(text)
        message_box.exec_()

    def _on_show_token(self):
        dialog = TokenDialog(self.app_engine.get_current_token(), self)
        dialog.exec_()

    def _on_disconnect(self):
        self.app_engine.poll_stop()

    def _on_connect(self):
        logger.info('Sending start poll to engine')
        self.app_engine.poll_start()

    def _on_engine_poll_starting(self):
        try:
            self.engine_signals.new_frames_ready.connect(self._on_new_frames_ready)
        except Exception as error:
            logger.error(error)
        else:
            self.actionLoad.setEnabled(False)
            self.actionGet_Account_Keys.setEnabled(True)
            self.actionDisconnect.setEnabled(True)

    def _on_engine_poll_stop(self):
        try:
            self.engine_signals.new_frames_ready.disconnect(self._on_new_frames_ready)
        except Exception as error:
            logger.debug(f'Signal disconnection failed: {error}')

        for index in range(self.tabWidget.count() - 1, -1, -1):
            self.tabWidget.removeTab(index)

        self.actionLoad.setEnabled(True)
        self.actionGet_Account_Keys.setEnabled(False)
        self.actionDisconnect.setEnabled(False)

    def _on_engine_command_completed(self, command_id, command_name, response, result, error):
        if command_id in self.pending_commands:
            self.pending_commands.remove(command_id)
            logger.debug(
                f'{command_name} command with id {command_id}'\
                f' completed with result {result}'
            )
            if not result:
                message = ''
                if command_name == self.app_engine.commands.WAKE_UP:
                    message = 'Wake up command failed'
                elif command_name == self.app_engine.commands.FLASH_LIGHTS:
                    message = 'Flash lights command failed'
                elif command_name == self.app_engine.commands.HONK:
                    message = 'Honk command failed'
                else:
                    message = 'Command failed'
                self.show_dialog(message, QMessageBox.Warning)

    def _on_new_frames_ready(self, frames):
        logger.info('Loading new frames')

        for frame in frames:
            existing_tab = None

            for index in range(self.tabWidget.count()):
                tab = self.tabWidget.widget(index)
                if tab.current_frame['id'] == frame['id']:
                    existing_tab = tab
                    break

            if existing_tab == None:
                existing_tab = VehicleView()

                existing_tab.wake_up.connect(self._on_vehicle_wake_up)
                existing_tab.honk.connect(self._on_vehicle_honk)
                existing_tab.flash_lights.connect(self._on_vehicle_flash_lights)

                tab_name = frame['vin']
                if  'display_name' in frame \
                        and frame['display_name'] != None \
                        and frame['display_name'] != '':
                    tab_name = frame['display_name']
                self.tabWidget.addTab(existing_tab, tab_name)

            existing_tab.load_frame(frame)

    def _on_engine_credentials_result(self, command_id, response, result, error):
        logger.debug(f'credentials result {command_id}, {result}, {error}')
        if result:
            dialog = self.credentials_dialog
            self.credentials_dialog = None
            dialog.accept()
        else:
            self.credentials_dialog.show_message(error)
            self.credentials_dialog.switch_input_status(True)

    def _on_engine_credentials_required(self):
        logger.debug('Asking user for credentials')
        if self.credentials_dialog == None:
            self.credentials_dialog = CredentialsDialog(self)
            self.credentials_dialog.submit_credentials.connect(
                self._on_credentials_dialog_submited
            )
            self.credentials_dialog.demo_mode.connect(
                self._on_credentials_demo_mode
            )
            if self.credentials_dialog.exec_() == 1:
                self.app_engine.poll_start()
            self.credentials_dialog = None

    def _on_credentials_dialog_submited(self):
        try:
            self.credentials_dialog.switch_input_status(False)
            self.credentials_dialog.show_message('')
            self.app_engine.load_credentials(
                self.credentials_dialog.get_user_name(),
                self.credentials_dialog.get_password(),
                self.credentials_dialog.get_token()
            )
        except EngineValidationError as error:
            self.credentials_dialog.switch_input_status(True)
            self.credentials_dialog.show_message(str(error))

    def _on_credentials_demo_mode(self):
        self.credentials_dialog.switch_input_status(False)
        self.app_engine.enable_demo_mode()

    def _on_engine_api_switched(self):
        if self.credentials_dialog != None:
            dialog = self.credentials_dialog
            self.credentials_dialog = None
            dialog.accept()

    def _on_vehicle_wake_up(self, car_id):
        logger.debug(f'Waking up car {car_id}')
        self.pending_commands.append(
            self.app_engine.send_car_command(self.app_engine.commands.WAKE_UP, car_id)
        )
        self.show_dialog('Waking up car. It may take a few seconds')

    def _on_vehicle_honk(self, car_id):
        logger.debug(f'Honking car {car_id}')
        self.pending_commands.append(
            self.app_engine.send_car_command(self.app_engine.commands.HONK, car_id)
        )

    def _on_vehicle_flash_lights(self, car_id):
        logger.debug(f'Flashing lights car {car_id}')
        self.pending_commands.append(
            self.app_engine.send_car_command(self.app_engine.commands.FLASH_LIGHTS, car_id)
        )
