import random
import time
from typing import cast

from PySide6 import QtWidgets, QtGui

import sys

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from events import Events

import AlertHandler
from Port import Port
from ui import NoteWidget
from ui.EffectFactory import EffectFactory
from ui.LabeledDropDown import LabeledDropDown
from ui.LabeledSlider import LabeledSlider
from ui.LabeledSpinBox import LabeledSpinBox
from ui.Note import Note
from ui.NoteWidget import NoteWidget
from ui.OrientablePushButton import OrientablePushButton
from ui.PortListModel import PortListModel


class OSCMidiWidget(QWidget, Events):
    __events__ = (
    'on_selected_input_change', 'on_selected_output_change', 'on_running_state_change', 'on_start', 'on_stop',
    'on_particle_enabled_change', 'on_particle_limit_enabled_change', 'on_particle_limit_change',
    'on_particle_lifetime_change', 'on_notes_change', 'on_search_text_change')

    DEFAULT_PARTICLE_LIMIT: int = 16
    MAXIMUM_PARTICLE_LIMIT: int = 50000

    PARTICLE_LIFETIME_DEFAULT: float = 0.1
    PARTICLE_LIFETIME_MINIMUM: float = 0.01
    PARTICLE_LIFETIME_MAXIMUM: float = 0.4
    PARTICLE_LIFETIME_SLIDER_SCALE: float = 0.001

    def __init__(self):
        super().__init__()

        self._searchClearButton: QPushButton = None
        self._searchBar: QLineEdit = None
        self._removeItemButton:QPushButton = None
        self._addItemButton: QPushButton = None
        self._noteListWidget: QListWidget = None
        self._labeledSlider: LabeledSlider = None
        self._labeledSpinBox: LabeledSpinBox = None
        self._particleLifeTimeSlider: QSlider = None
        self._enableParticleLimitButton: QPushButton = None
        self._enableParticleButton: QPushButton = None
        self._particleLimitSpinBox: QSpinBox = None
        self._inputSelector: LabeledDropDown = None
        self._outputSelector: LabeledDropDown = None
        self._startButton: QPushButton = None

        self._noInput: bool = False
        self._noOutput: bool = False
        self._running_state: bool = False

        self._lastInputPort: Port = None
        self._lastOutputPort: Port = None

        self.initUI()
        self.initUIEvent()

    def refreshParticleBox(self):
        self._labeledSlider.setVisible(self._enableParticleButton.isChecked())
        self._enableParticleLimitButton.setVisible(self._enableParticleButton.isChecked())
        self._labeledSpinBox.setVisible(
            self._enableParticleButton.isChecked() and self._enableParticleLimitButton.isChecked())

    def refreshInputDropdown(self):
        self._noInput = self._inputSelector.dropdown.count() == 0 or self._inputSelector.dropdown.currentIndex() < 0

        if self.isThereAvailableInputs():
            EffectFactory.createEffect(self._inputSelector.dropdown, 'red')
            self._inputSelector.dropdown.setToolTip('No MIDI input found')
        else:
            self._inputSelector.dropdown.setGraphicsEffect(None)
            self._inputSelector.dropdown.setToolTip(None)

        self.refreshStartButton()

    def refreshOutputDropdown(self):
        self._noOutput = self._outputSelector.dropdown.count() == 0 or self._outputSelector.dropdown.currentIndex() < 0

        if self.isThereAvailableOutputs():
            EffectFactory.createEffect(self._outputSelector.dropdown, 'red')
            self._outputSelector.dropdown.setToolTip('No MIDI output selected')
        else:
            self._outputSelector.dropdown.setGraphicsEffect(None)
            self._outputSelector.dropdown.setToolTip(None)

        self.refreshStartButton()

    def refreshStartButton(self):
        self._startButton.setEnabled(self.canRun())

        if self.canRun():
            EffectFactory.createEffect(self._startButton, 'green' if self._running_state else 'red')
            self._startButton.setToolTip(None)
        else:
            self._startButton.setGraphicsEffect(None)
            self._startButton.setToolTip('Start disabled, there might be an issue')
            self._running_state = False

        if self.isRunning():
            if self._startButton.text() != 'Stop':
                self._startButton.setText('Stop')
                self.on_running_state_change(True)
                self.on_start()
        else:
            if self._startButton.text() != 'Start':
                self._startButton.setText('Start')
                self.on_running_state_change(False)
                self.on_stop()

    def startButtonClicked(self):
        self._running_state = not self._running_state
        self.refreshStartButton()

    def createIOBox(self):
        box = QGroupBox()
        layout = QVBoxLayout()
        box.setLayout(layout)

        box.setTitle('Input / Output')

        self._inputSelector = LabeledDropDown('Input : ')
        self._inputSelector.dropdown.setModel(PortListModel())

        self._outputSelector = LabeledDropDown('Output : ')
        self._outputSelector.dropdown.setModel(PortListModel())

        layout.addWidget(self._inputSelector)
        layout.addWidget(self._outputSelector)

        return box

    def createParticleSettingsBox(self):
        box = QGroupBox()
        layout = QVBoxLayout()
        box.setLayout(layout)

        box.setTitle('Particle Settings')

        self._enableParticleButton = QPushButton()
        self._enableParticleButton.setCheckable(True)
        self._enableParticleButton.setText("Enable Particles")

        self._enableParticleLimitButton = QPushButton()
        self._enableParticleLimitButton.setCheckable(True)
        self._enableParticleLimitButton.setText("Limit Particles")

        self._labeledSpinBox = LabeledSpinBox('Limit : ')

        self._particleLimitSpinBox = self._labeledSpinBox.spinbox
        self._particleLimitSpinBox.setMinimum(1)
        self._particleLimitSpinBox.setMaximum(OSCMidiWidget.MAXIMUM_PARTICLE_LIMIT)
        self._particleLimitSpinBox.setValue(OSCMidiWidget.DEFAULT_PARTICLE_LIMIT)

        self._labeledSlider = LabeledSlider('Particle lifetime : ')
        self._particleLifeTimeSlider = self._labeledSlider.slider
        self._particleLifeTimeSlider.setMinimum(
            int(OSCMidiWidget.PARTICLE_LIFETIME_MINIMUM / OSCMidiWidget.PARTICLE_LIFETIME_SLIDER_SCALE))
        self._particleLifeTimeSlider.setMaximum(
            int(OSCMidiWidget.PARTICLE_LIFETIME_MAXIMUM / OSCMidiWidget.PARTICLE_LIFETIME_SLIDER_SCALE))
        self.setParticleLifeTime(OSCMidiWidget.PARTICLE_LIFETIME_DEFAULT)

        layout.addWidget(self._enableParticleButton)
        layout.addWidget(self._enableParticleLimitButton)
        layout.addWidget(self._labeledSpinBox)
        layout.addWidget(self._labeledSlider)

        # Setup events

        self._enableParticleButton.clicked.connect(lambda: self.refreshParticleBox())
        self._enableParticleLimitButton.clicked.connect(lambda: self.refreshParticleBox())

        # Call events once to refresh everything
        self.refreshParticleBox()

        # tooltips
        self._labeledSlider.setToolTip("The duration of particles, how long they will last")


        return box

    def createStartButton(self):
        box = QWidget()
        layout = QHBoxLayout()
        box.setLayout(layout)

        self._startButton = QPushButton('Start')

        layout.addWidget(self._startButton)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 0, 40, 0)

        return box

    def createNotePanel(self):
        box = QGroupBox()
        layout = QVBoxLayout()
        box.setLayout(layout)

        box.setTitle('Notes')

        searchLayout = QHBoxLayout()
        self._searchBar = QLineEdit()
        self._searchClearButton = QPushButton('Clear')

        searchBarLabel = QLabel("Search")
        searchLayout.addWidget(searchBarLabel)
        searchLayout.addWidget(self._searchBar)
        searchLayout.addWidget(self._searchClearButton)

        layout.addLayout(searchLayout)

        self._noteListWidget = QListWidget()
        self._noteListWidget.setWrapping(False)
        self._noteListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        buttonLayout = QHBoxLayout()
        self._addItemButton = QPushButton('+')
        self._removeItemButton = QPushButton("-")

        buttonLayout.addWidget(self._addItemButton)
        buttonLayout.addWidget(self._removeItemButton)

        layout.addWidget(self._noteListWidget, 1)
        layout.addLayout(buttonLayout, 0)
        # Setup Actions

        self._addItemButton.clicked.connect(self.addNoteItem)
        self._removeItemButton.clicked.connect(self.removeNoteItem)

        self._searchClearButton.clicked.connect(lambda: self._searchBar.setText(""))
        self._searchBar.textChanged.connect(lambda: self._noteListWidget.sortItems())

        # tooltips
        self._searchBar.setToolTip("Your note list will be ordered according to the content of the search bar")
        searchBarLabel.setToolTip("Your note list will be ordered according to the content of the search bar")

        self._addItemButton.setToolTip("Adds a new note to your note list")
        self._removeItemButton.setToolTip("Removes selected notes from your note list, you can select notes by clicking on one or by dragging your mouse over them")

        self._noteListWidget.setToolTip("Your personal note list! Recommended use : Note the songs your know and don't know (a note is considered known when it is checked)")

        return box

    def createDialogButtonBox(self):
        box = QGroupBox()
        layout = QVBoxLayout()
        box.setLayout(layout)

        box.setTitle('Actions')

        self._dialog_button_box = QDialogButtonBox(Qt.Vertical)

        self._get_random_checked_note_button = QPushButton("Random")
        self._dialog_button_box.addButton(self._get_random_checked_note_button, QDialogButtonBox.ActionRole)
        layout.addWidget(self._dialog_button_box, 1)

        self._get_random_checked_note_button.clicked.connect(self.showRandomSong)

        #tooltips
        self._get_random_checked_note_button.setToolTip("When you don't know what to play, click this button! It will randomly give you one of the songs you know!")

        return box

    def showRandomSong(self):
        notes: [Note] = self.getCheckedNotes(True)
        if len(notes) > 0:
            song = notes[random.randint(0, len(notes) - 1)].getText()
        else:
            song = "No known song\nTime to learn some!"

        AlertHandler.show_info("Random song!", song)

    def setAvailableInputs(self, inputs: [Port]) -> None:
        index = self._inputSelector.dropdown.currentIndex()
        self._inputSelector.dropdown.setModel(PortListModel(inputs))

        if index >= self._inputSelector.dropdown.count():
            self._inputSelector.dropdown.setCurrentIndex(self._inputSelector.dropdown.count() - 1)
            self.on_selected_input_change(self.getSelectedInput())
        else:
            self._inputSelector.dropdown.setCurrentIndex(index)

    def getAvailableInputs(self) -> [Port]:
        inputs: [Port] = []

        for index in range(0, self._inputSelector.dropdown.count()):
            inputs.append(self._inputSelector.dropdown.itemData(index, Qt.UserRole))

        return inputs

    def isThereAvailableInputs(self) -> bool:
        return self._noInput

    def getSelectedInput(self) -> Port | None:
        index = self._inputSelector.dropdown.currentIndex()
        if index < 0:
            return None

        return self._inputSelector.dropdown.itemData(index, Qt.UserRole)

    def setSelectedInput(self, port_name: str):
        i = 0
        for port in self.getAvailableInputs():
            if port.getName() == port_name:
                self._inputSelector.dropdown.setCurrentIndex(i)
                self._onInputChange()
                break
            i = i + 1

    def isOutputSelectorOpened(self) -> bool:
        return self._outputSelector.dropdown.view().isVisible()

    def resetSelectedInput(self) -> None:
        self._inputSelector.dropdown.setCurrentIndex(-1)
        self._onInputChange()

    def setAvailableOutputs(self, outputs: [Port]) -> None:
        index = self._outputSelector.dropdown.currentIndex()
        self._outputSelector.dropdown.setModel(PortListModel(outputs))

        if index >= self._outputSelector.dropdown.count():
            self._outputSelector.dropdown.setCurrentIndex(self._outputSelector.dropdown.count() - 1)
            self.on_selected_output_change(self.getSelectedOutput())
        else:
            self._outputSelector.dropdown.setCurrentIndex(index)

    def getAvailableOutputs(self) -> [Port]:
        outputs: [Port] = []

        for index in range(0, self._outputSelector.dropdown.count()):
            outputs.append(self._outputSelector.dropdown.itemData(index, Qt.UserRole))

        return outputs

    def isThereAvailableOutputs(self) -> bool:
        return self._noOutput

    def getSelectedOutput(self) -> Port | None:
        index = self._outputSelector.dropdown.currentIndex()
        if index < 0:
            return None

        return self._outputSelector.dropdown.itemData(index, Qt.UserRole)

    def setSelectedOutput(self, port_name: str):
        i = 0
        for port in self.getAvailableOutputs():
            if port.getName() == port_name:
                self._outputSelector.dropdown.setCurrentIndex(i)
                self._onOutputChange()
                break
            i = i + 1

    def isInputSelectorOpened(self) -> bool:
        return self._inputSelector.dropdown.view().isVisible()

    def resetSelectedOutput(self) -> None:
        self._outputSelector.dropdown.setCurrentIndex(-1)
        self._onOutputChange()

    def setParticlesEnabled(self, value) -> None:
        if value == self._enableParticleButton.isChecked():
            return

        self._enableParticleButton.setChecked(value)
        self.on_particle_enabled_change(value)

    def areParticlesEnabled(self) -> bool:
        return self._enableParticleButton.isChecked()

    def setLimitParticles(self, value) -> None:
        if value == self._enableParticleLimitButton.isChecked():
            return

        self._enableParticleLimitButton.setChecked(value)
        self.on_particle_limit_enabled_change(value)

    def areParticlesLimited(self) -> bool:
        return self._enableParticleLimitButton.isChecked()

    def setParticleLimit(self, limit) -> None:
        self._particleLimitSpinBox.setValue(limit)

    def getParticleLimit(self) -> int:
        return self._particleLimitSpinBox.value()

    def setParticleLifeTime(self, lifetime) -> None:
        self._particleLifeTimeSlider.setValue(int(lifetime / OSCMidiWidget.PARTICLE_LIFETIME_SLIDER_SCALE))

    def getParticleLifeTime(self) -> float:
        return self._particleLifeTimeSlider.value() * OSCMidiWidget.PARTICLE_LIFETIME_SLIDER_SCALE

    def getNotes(self):
        notes: [Note] = []
        for row in range(self._noteListWidget.count()):
            item = self._noteListWidget.item(row)
            notes.append(item)

        return notes

    def getCheckedNotes(self, checked):
        notes: [Note] = []
        for row in range(self._noteListWidget.count()):
            item = self._noteListWidget.item(row)
            if item.isChecked() == checked:
                notes.append(item)

        return notes

    def getSelectedNoteItems(self):
        return self._noteListWidget.selectedItems()

    def addNoteItem(self, checked: bool = False, text: str = ""):
        item = Note(checked=checked, text=text)
        item_widget = NoteWidget(item)

        item.setSearchStringFunction(lambda: self.getSearchText())

        # Set size hint
        item.setSizeHint(item_widget.sizeHint())
        self._noteListWidget.addItem(item)
        self._noteListWidget.setItemWidget(item, item_widget)

        # Add event listeners
        item_widget.text_box.textChanged.connect(lambda: self.on_notes_change(self.getNotes()))
        item_widget.check_box.stateChanged.connect(lambda: self.on_notes_change(self.getNotes()))

        # Call the change
        self.on_notes_change(self.getNotes())

    def removeNoteItem(self):
        for item in self.getSelectedNoteItems():
            self._noteListWidget.takeItem(self._noteListWidget.row(item))
        self._noteListWidget.clearSelection()

        # Call the change
        self.on_notes_change(self.getNotes())

    def getSearchText(self) -> str:
        return self._searchBar.text()

    def setSearchText(self, text: str) -> None:
        self._searchBar.setText(text)

    def start(self) -> None:
        if self.canRun():
            self._running_state = True
            self.refreshStartButton()

    def stop(self) -> None:
        self._running_state = False
        self.refreshStartButton()

    def isRunning(self) -> bool:
        return self._running_state

    def canRun(self) -> bool:
        return (not self.isThereAvailableOutputs()) and (not self.isThereAvailableInputs())

    def initUI(self):
        self.setWindowTitle('OSCMidi')
        layout = QHBoxLayout()
        innerLayout = QVBoxLayout()

        innerLayout.addWidget(self.createIOBox(), 1)
        innerLayout.addWidget(self.createParticleSettingsBox(), 0)
        innerLayout.addWidget(self.createStartButton(), 0)

        layout.addLayout(innerLayout, 1)
        layout.addWidget(self.createNotePanel(), 2)
        layout.addWidget(self.createDialogButtonBox(), 0)

        self.setLayout(layout)
        self.show()

    def _onInputChange(self):
        selected_input: Port = self.getSelectedInput()
        if self._lastInputPort == selected_input:
            return

        self.on_selected_input_change(selected_input)
        self._lastInputPort = selected_input

    def _onOutputChange(self):
        selected_output: Port = self.getSelectedOutput()
        print(self._lastOutputPort, " = ", selected_output)

        if self._lastOutputPort == selected_output:
            return
        self._lastOutputPort = selected_output
        self.on_selected_output_change(selected_output)

    def initUIEvent(self):
        self._inputSelector.dropdown.activated.connect(self._onInputChange)
        self._outputSelector.dropdown.activated.connect(self._onOutputChange)

        self._enableParticleButton.clicked.connect(lambda: self.on_particle_enabled_change(self.areParticlesEnabled()))
        self._enableParticleLimitButton.clicked.connect(
            lambda: self.on_particle_limit_enabled_change(self.areParticlesLimited()))

        self._particleLimitSpinBox.valueChanged.connect(lambda: self.on_particle_limit_change(self.getParticleLimit()))
        self._particleLifeTimeSlider.valueChanged.connect(
            lambda: self.on_particle_lifetime_change(self.getParticleLifeTime()))

        self._inputSelector.dropdown.currentIndexChanged.connect(self.refreshInputDropdown)
        self._outputSelector.dropdown.currentIndexChanged.connect(self.refreshOutputDropdown)
        self._startButton.clicked.connect(self.startButtonClicked)

        self.refreshInputDropdown()
        self.refreshOutputDropdown()
        self.refreshStartButton()

        self._searchBar.textChanged.connect(self.on_search_text_change)

        self.on_running_state_change += lambda value: self._inputSelector.setEnabled(not value)
        self.on_running_state_change += lambda value: self._outputSelector.setEnabled(not value)

        self.on_notes_change += lambda notes: self._noteListWidget.sortItems() if self.getSearchText() != '' else None
