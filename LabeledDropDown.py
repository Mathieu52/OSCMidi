from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class LabeledDropDown(QHBoxLayout):
    label:QLabel = None
    dropdown:QComboBox = None

    def __init__(self, text: str, *args, parent=None):
        super().__init__(parent)
        self.initUI(text, args)

    def initUI(self, text: str, *args):
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setAlignment(Qt.AlignCenter)

        self.dropdown = QComboBox()
        self.dropdown.addItems(args[0])

        self.addWidget(self.label, 0)
        self.addWidget(self.dropdown, 1)