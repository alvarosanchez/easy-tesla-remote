from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import (
    QStandardItemModel, 
    QStandardItem,
)
from PyQt5.QtCore import Qt
from .auto_generated.option_codes_dialog_auto import Ui_OptionsCodeDialog
from engine.app_engine import EngineValidationError 


class OptionCodesDialog(QDialog, Ui_OptionsCodeDialog):

    def __init__(self, app_engine, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.app_engine = app_engine

        self.translateCodes.clicked.connect(self.on_translate_codes)
        self.closeDialog.clicked.connect(self.reject)
    
    def on_translate_codes(self):
        self.show_message('')
        try:
            codes = self.optionCodes.toPlainText()
            codes = self.app_engine.sanitize_option_codes(codes)
            self.optionCodes.setPlainText(codes.replace(',', ', '))
            translated = self.app_engine.translate_option_codes(codes)
            self.populate_option_codes(translated)
        except Exception as error:
            self.show_message(str(error))

    def show_message(self, message):
        self.message.setText(message)      
    
    def populate_option_codes(self, codes):
        self.option_code_widgets = []

        model = QStandardItemModel()
        model.setColumnCount(2)
        
        for code in codes:
            item01 = QStandardItem(code[0])
            item01.setFlags(Qt.ItemIsEditable)
            item02 = QStandardItem(code[1])
            item02.setFlags(Qt.ItemIsEditable)
            
            row = [
                item01,
                item02
            ]
            model.appendRow(row)
        
        self.codeTable.setModel(model)