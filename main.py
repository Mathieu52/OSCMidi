from PySide6 import QtWidgets, QtGui

import sys

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from EffectFactory import EffectFactory
from LabeledDropDown import LabeledDropDown
from LabeledSlider import LabeledSlider
from LabeledSpinBox import LabeledSpinBox
from NumberDisplay import NumberDisplay
from SeparatorFactory import SeparatorFactory


class OSCMidiWidget(QWidget):
    DEFAULT_PARTICLE_LIMIT: int = 16
    MAXIMUM_PARTICLE_LIMIT: int = 50000

    def __init__(self):
        super().__init__()

        self.enableParticleLimitButton = None
        self.enableParticleButton = None
        self.particleLimitSpinBox = None
        self.inputSelector = None
        self.outputSelector = None
        self.portStyleSelector = None
        self.startButton: QPushButton = None

        self.noInput: bool = False
        self.noOutput: bool = False
        self.running: bool = False

        self.initUI()
        self.initUIEvent()

    def refreshInputDropdown(self):
        self.noInput = self.inputSelector.dropdown.count() == 0
        if self.noInput:
            EffectFactory.createEffect(self.inputSelector.dropdown, 'red')
            self.inputSelector.dropdown.setToolTip('No MIDI input found')
        else:
            self.inputSelector.dropdown.setGraphicsEffect(None)
            self.inputSelector.dropdown.setToolTip(None)

        self.refreshStartButton()

    def refreshOutputDropdown(self):
        self.noOutput = self.outputSelector.dropdown.count() == 0
        if self.noOutput:
            EffectFactory.createEffect(self.outputSelector.dropdown, 'red')
            self.outputSelector.dropdown.setToolTip('No MIDI output found')
        else:
            self.outputSelector.dropdown.setGraphicsEffect(None)
            self.outputSelector.dropdown.setToolTip(None)

        self.refreshStartButton()

    def refreshStartButton(self):
        disable : bool = self.noInput or self.noOutput

        if not disable:
            EffectFactory.createEffect(self.startButton, 'green' if self.running else 'red')
        else:
            self.startButton.setGraphicsEffect(None)

        if disable:
            self.running = False
            self.startButton.setEnabled(False)
        else:
            self.startButton.setEnabled(True)

        if self.running:
            self.startButton.setText('Stop')
        else:
            self.startButton.setText('Start')
    def startButtonClicked(self):
        self.running = not self.running
        self.refreshStartButton()


    def createIOBox(self):
        box = QGroupBox()
        layout = QVBoxLayout()
        box.setLayout(layout)

        box.setTitle('Input / Output')

        self.inputSelector = LabeledDropDown('Input : ', '1', '2', '3', layout)
        self.outputSelector = LabeledDropDown('Output : ', '1', '2', '3', layout)

        layout.addWidget(self.inputSelector)
        layout.addWidget(self.outputSelector)

        return box

    def createPortStyleBox(self):
        box = QGroupBox()
        layout = QVBoxLayout()
        box.setLayout(layout)

        box.setTitle('Port Style')

        self.portStyleSelector = LabeledDropDown('Style : ', '1', '2', layout)

        layout.addWidget(self.portStyleSelector)

        return box

    def createParticleSettingsBox(self):
        box = QGroupBox()
        layout = QVBoxLayout()
        box.setLayout(layout)

        box.setTitle('Particle Settings')

        self.enableParticleButton = QPushButton()
        self.enableParticleButton.setCheckable(True)
        self.enableParticleButton.setText("Enable Particles")

        self.enableParticleLimitButton = QPushButton()
        self.enableParticleLimitButton.setCheckable(True)
        self.enableParticleLimitButton.setText("Limit Particles")

        labeledSpinBox = LabeledSpinBox('Limit : ')

        self.particleLimitSpinBox = labeledSpinBox.spinbox
        self.particleLimitSpinBox.setMinimum(1)
        self.particleLimitSpinBox.setMaximum(OSCMidiWidget.MAXIMUM_PARTICLE_LIMIT)
        self.particleLimitSpinBox.setValue(OSCMidiWidget.DEFAULT_PARTICLE_LIMIT)

        labeledSlider = LabeledSlider('Particle lifetime : ')
        self.particleLifeTimeSlider = labeledSlider.slider
        self.particleLifeTimeSlider.setMinimum(10)
        self.particleLifeTimeSlider.setMaximum(1000)


        layout.addWidget(self.enableParticleButton)
        layout.addWidget(self.enableParticleLimitButton)
        layout.addWidget(labeledSpinBox)
        layout.addWidget(labeledSlider)

        # Setup events

        activateParticleLifeTimeSlider = lambda: labeledSlider.setVisible(self.enableParticleButton.isChecked())
        self.enableParticleButton.clicked.connect(activateParticleLifeTimeSlider)

        activateLimitButton = lambda: self.enableParticleLimitButton.setVisible(self.enableParticleButton.isChecked())
        self.enableParticleButton.clicked.connect(activateLimitButton)

        activateLimitSpinBox = lambda: labeledSpinBox.setVisible(self.enableParticleButton.isChecked() and self.enableParticleLimitButton.isChecked())
        self.enableParticleButton.clicked.connect(activateLimitSpinBox)
        self.enableParticleLimitButton.clicked.connect(activateLimitSpinBox)

        # Call events once to refresh everything
        activateParticleLifeTimeSlider()
        activateLimitButton()
        activateLimitSpinBox()

        return box

    def createStartButton(self):
        box = QWidget()
        layout = QHBoxLayout()
        box.setLayout(layout)

        self.startButton = QPushButton("Start")

        layout.addWidget(self.startButton)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 0, 40, 0)

        return box

    def initUI(self):
        self.setWindowTitle('OSCMidi')
        layout = QVBoxLayout()

        layout.addWidget(self.createIOBox())
        layout.addWidget(self.createPortStyleBox())
        layout.addWidget(self.createParticleSettingsBox())
        layout.addWidget(self.createStartButton())

        self.setLayout(layout)
        self.resize(300, 200)  # Set a size for the widget
        self.show()

    def initUIEvent(self):
        self.inputSelector.dropdown.currentIndexChanged.connect(self.refreshInputDropdown)
        self.outputSelector.dropdown.currentIndexChanged.connect(self.refreshOutputDropdown)
        self.startButton.clicked.connect(self.startButtonClicked)

        self.refreshInputDropdown()
        self.refreshOutputDropdown()
        self.refreshStartButton()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OSCMidiWidget()
    sys.exit(app.exec())