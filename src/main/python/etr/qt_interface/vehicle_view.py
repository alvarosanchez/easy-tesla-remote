import json

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import (
    Qt, 
    pyqtSignal,
)
from PyQt5.QtGui import (
    QStandardItemModel, 
    QStandardItem,
)

from etr.engine.util.option_codes import translate_codes

from .auto_generated.vehicle_view_auto import Ui_VehicleView
from .util.adapters import AdapterTracker
from etr.engine.util.dictionaries import dump_to_tupple_list


class VehicleView(QWidget, Ui_VehicleView):

    wake_up = pyqtSignal(str)
    honk = pyqtSignal(str)
    flash_lights = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.action_wake_up.clicked.connect(self.on_action_wake_up)
        self.action_flash.clicked.connect(self.on_action_flash_lights)
        self.action_honk.clicked.connect(self.on_action_honk)

    def load_frame(self, frame):
        self.current_frame = frame
        self.enable_actions(frame)
        self.populate_overview(frame)
        self.populate_option_codes(frame)
        self.populate_json_raw_data(frame)
        self.populate_keyvalue_raw_data(frame)

    def enable_actions(self, frame):
        car_asleep = frame['state'] != 'online'
        self.action_wake_up.setEnabled(car_asleep)
        self.action_flash.setEnabled(not car_asleep)
        self.action_honk.setEnabled(not car_asleep)

    def populate_option_codes(self, frame):
        self.option_code_widgets = []

        codes = translate_codes(frame['option_codes'])

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
        
        self.tableView.setModel(model)

    def populate_json_raw_data(self, frame):
        text = json.dumps(frame, sort_keys=True, indent=4, separators=(',', ': '))
        self.frameJson.setPlainText(text)

    def populate_keyvalue_raw_data(self, frame):
        data = dump_to_tupple_list(frame)

        model = QStandardItemModel()
        model.setColumnCount(2)
        
        for tupple in data:
            item01 = QStandardItem(tupple[0])
            item01.setFlags(Qt.ItemIsEditable)
            item02 = QStandardItem(str(tupple[1]))
            item02.setFlags(Qt.ItemIsEditable)
            
            row = [
                item01,
                item02
            ]
            model.appendRow(row)
        
        self.frameKeyValue.setModel(model)
        self.frameKeyValue.setColumnWidth(0, 400)

    def populate_overview(self, frame):
        for key in vars(self):
            attribute = getattr(self, key)
            if issubclass(type(attribute), QWidget):
                mapping = attribute.property('jsonAttribute')
                adapter = attribute.property('valueAdapter')
                target_property = attribute.property('targetProperty')
                if mapping != None and adapter != None and target_property != None:
                    AdapterTracker.execute_adapter(adapter, frame, mapping, attribute, target_property)

    def on_action_wake_up(self):
        self.wake_up.emit(str(self.current_frame['id']))

    def on_action_honk(self):
        self.honk.emit(str(self.current_frame['id']))

    def on_action_flash_lights(self):
        self.flash_lights.emit(str(self.current_frame['id']))
