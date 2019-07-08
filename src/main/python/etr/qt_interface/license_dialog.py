from PyQt5.QtWidgets import QDialog
from .auto_generated.license_dialog_auto import Ui_LicenseDialog


class LicenseDialog(QDialog, Ui_LicenseDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.licenseAccept.clicked.connect(self._on_license_accept)
        self.licenseDecline.clicked.connect(self._on_license_decline)

    def _on_license_accept(self):
        self.accept()

    def _on_license_decline(self):
        self.reject()
