from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class LabeledDropDown(QWidget):
    def __init__(self, text: str, *args, parent=None):
        super().__init__(parent)
        self.dropdown: QComboBox = None
        self.label: QLabel = None
        self.initUI(text, args)

    def initUI(self, text: str, *args):
        layout = QHBoxLayout()

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.setAlignment(Qt.AlignCenter)

        self.dropdown = QComboBox()
        self.dropdown.addItems(args[0])

        layout.addWidget(self.label, 0)
        layout.addWidget(self.dropdown, 1)
        self.setLayout(layout)