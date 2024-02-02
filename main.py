from PySide6 import QtWidgets, QtGui

import sys

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from EffectFactory import EffectFactory
from LabeledDropDown import LabeledDropDown
from SeparatorFactory import SeparatorFactory


class DropDownWidget(QWidget):
    input = None
    output = None
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initUIEvent()

    def refreshInputDropdown(self):
        if self.input.dropdown.count() == 0:
            EffectFactory.createEffect(self.input.dropdown, 'red')
            self.input.dropdown.setToolTip('No MIDI input found')
        else:
            self.input.dropdown.setGraphicsEffect(None)
            self.input.dropdown.setToolTip(None)

    def refreshOutputDropdown(self):
        if self.output.dropdown.count() == 0:
            EffectFactory.createEffect(self.output.dropdown, 'red')
            self.output.dropdown.setToolTip('No MIDI output found')
        else:
            self.output.dropdown.setGraphicsEffect(None)
            self.output.dropdown.setToolTip(None)

    def initUI(self):
        self.setWindowTitle('Vertical Drop Down Lists')
        layout = QVBoxLayout()

        ioBox = QGroupBox()
        ioLayout = QVBoxLayout()
        ioBox.setLayout(ioLayout)

        ioBox.setTitle('Input / Output')

        # Creating the first drop-down list
        self.input = LabeledDropDown('Input : ', '1', '2', '3', ioLayout)
        self.output = LabeledDropDown('Output : ', '1', '2', '3', ioLayout)

        ioLayout.addLayout(self.input)
        ioLayout.addLayout(self.output)

        layout.addWidget(ioBox)

        self.setLayout(layout)
        self.resize(300, 200)  # Set a size for the widget
        self.show()

    def initUIEvent(self):
        self.input.dropdown.currentIndexChanged.connect(self.refreshInputDropdown)
        self.output.dropdown.currentIndexChanged.connect(self.refreshOutputDropdown)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DropDownWidget()
    sys.exit(app.exec())
    pro