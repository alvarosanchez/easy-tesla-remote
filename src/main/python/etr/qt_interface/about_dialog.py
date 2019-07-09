from PyQt5.QtWidgets import QDialog
from .auto_generated.about_dialog_auto import Ui_AboutDialog
from .license_dialog import LicenseDialog

class AboutDialog(QDialog, Ui_AboutDialog):

    def __init__(self, engine_version, ui_version, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.uiVersion.setText(ui_version)
        self.engineVersion.setText(engine_version)
        self.closeButton.clicked.connect(self.close)
        self.licenseButton.clicked.connect(self._on_license)

    def _on_license(self):
        license_dialog = LicenseDialog(self, False)
        license_dialog.exec_()
