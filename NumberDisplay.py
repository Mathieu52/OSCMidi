from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
class NumberDisplay(QWidget):
    def __init__(self, label_text, number_text):
        super().__init__()
        self.label = QLabel(label_text)
        self.number_label = QLabel()
        self.number_label.setText(number_text)
        self.number_label.setStyleSheet("color: #007bff")  # Example styling for the number field


        layout = QHBoxLayout()
        layout.addWidget(self.label, 0)
        layout.addWidget(self.number_label)

        self.setLayout(layout)