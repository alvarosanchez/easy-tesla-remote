from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
)
from PyQt5.QtCore import pyqtSignal
from .auto_generated.credentials_dialog_auto import Ui_CredentialsDialog


class CredentialsDialog(QDialog, Ui_CredentialsDialog):

    submit_credentials = pyqtSignal(str, str)
    demo_mode = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.reject)
        self.DemoMode.clicked.connect(self.on_demo_mode)

    def on_accept(self):
        self.submit_credentials.emit(
            self.get_user_name(),
            self.get_password()
        )

    def on_demo_mode(self):
        self.demo_mode.emit()

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
