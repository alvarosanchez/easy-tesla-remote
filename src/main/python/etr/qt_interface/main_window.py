import logging

from PyQt5.QtWidgets import (
    QMainWindow, 
    QMessageBox,
)
from PyQt5.QtCore import QTimer

from .util.engine_signals import EngineSignals
from .auto_generated.main_window_auto import Ui_MainWindow
from .vehicle_view import VehicleView
from .credentials_dialog import CredentialsDialog
from .token_dialog import TokenDialog
from .option_codes_dialog import OptionCodesDialog
from .license_dialog import LicenseDialog


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app_engine, parent=None):
        super().__init__(parent=parent)
        self.app_engine = app_engine
        self.setupUi(self)

        self.initial_connection_timer = QTimer(self)
        self.initial_connection_timer.timeout.connect(self._on_initial_connection)
        self.load_abort_timer = QTimer(self)
        self.load_abort_timer.timeout.connect(self._on_load_abort)

        self.pending_commands = []

        self.credentials_dialog = None

        self.engine_signals = EngineSignals(app_engine, self)
        self.engine_signals.credentials_required.connect(self._on_engine_credentials_required)
        self.engine_signals.poll_starting.connect(self._on_engine_poll_starting)
        self.engine_signals.poll_stopped.connect(self._on_engine_poll_stop)
        self.engine_signals.poll_stopping.connect(self._on_engine_poll_stop)
        self.engine_signals.command_completed.connect(self._on_engine_command_completed)

        self.actionExit.triggered.connect(self.close)
        self.actionLoad.triggered.connect(self._on_connect)
        self.actionDisconnect.triggered.connect(self._on_disconnect)
        self.actionGet_Account_Keys.triggered.connect(self._on_show_token)
        self.actionOption_Code_Translator.triggered.connect(self._on_option_code_translator)

    def showEvent(self, event):
        license_dialog = LicenseDialog(self)
        if license_dialog.exec_() == 1:
            self.initial_connection_timer.start(1)
        else:
            self.load_abort_timer.start(1)

    def closeEvent(self, event):
        logger.debug('Main window closed unwiring engine events')
        self.engine_signals.unwire_events()

    def show_dialog(self, text, icon=QMessageBox.Information):
        message_box = QMessageBox(self)
        message_box.setIcon(icon)
        message_box.setText(text)
        message_box.exec_()

    def _on_initial_connection(self):
        self.initial_connection_timer.stop()
        self._on_connect()

    def _on_load_abort(self):
        self.load_abort_timer.stop()
        self.close()

    def _on_show_token(self):
        dialog = TokenDialog(self.app_engine.get_current_token(), self)
        dialog.exec_()

    def _on_option_code_translator(self):
        dialog = OptionCodesDialog(self.app_engine, self)
        dialog.exec_()

    def _on_disconnect(self):
        self.app_engine.poll_stop()
        self.app_engine.enable_real_mode()

    def _on_connect(self):
        logger.debug('Sending start poll to engine')
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
        logger.debug('Loading new frames')

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

    def _on_engine_credentials_required(self):
        logger.debug('Asking user for credentials')
        if self.credentials_dialog == None:
            self.credentials_dialog = CredentialsDialog(self.app_engine, self)
            if self.credentials_dialog.exec_() == 1:
                self.app_engine.poll_start()
            self.credentials_dialog = None

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
