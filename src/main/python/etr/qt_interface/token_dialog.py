from PyQt5.QtWidgets import QDialog
from .auto_generated.token_dialog_auto import Ui_TokenDialog


class TokenDialog(QDialog, Ui_TokenDialog):

    def __init__(self, token, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.tokenBox.setPlainText(token)
        self.buttonBox.accepted.connect(self.accept)
