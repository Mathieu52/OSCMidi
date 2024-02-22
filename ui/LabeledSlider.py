from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class LabeledSlider(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.slider: QSlider = None
        self.label: QLabel = None
        self.initUI(text)

    def initUI(self, text: str):
        layout = QHBoxLayout()

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.setAlignment(Qt.AlignCenter)

        self.slider = QSlider(Qt.Horizontal)

        layout.addWidget(self.label, 0)
        layout.addWidget(self.slider, 1)
        self.setLayout(layout)