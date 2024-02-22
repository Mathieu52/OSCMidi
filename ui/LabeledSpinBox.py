from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class LabeledSpinBox(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.spinbox: QSpinBox = None
        self.label: QLabel = None
        self.initUI(text)

    def initUI(self, text: str, *args):
        layout = QHBoxLayout()

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.setAlignment(Qt.AlignCenter)

        self.spinbox = QSpinBox()

        layout.addWidget(self.label, 0)
        layout.addWidget(self.spinbox, 1)
        self.setLayout(layout)