from PySide6.QtWidgets import QHBoxLayout, QWidget, QLabel, QLineEdit, QCheckBox

from ui.Note import Note


class NoteWidget(QWidget):
    def __init__(self, note: Note, parent=None):
        super(NoteWidget, self).__init__(parent)

        layout = QHBoxLayout()
        layout.setSpacing(10)

        self._note = note

        self.check_box = QCheckBox()
        self.text_box = QLineEdit()

        self.check_box.setChecked(note.isChecked())
        self.text_box.setText(note.getText())

        layout.addWidget(self.check_box, 0)
        layout.addWidget(self.text_box, 1)

        layout.setContentsMargins(0, 1, 0, 1)

        self.setLayout(layout)

        self._note.on_state_change += lambda checked: self.check_box.setChecked(checked)
        self._note.on_text_change += lambda text: self.text_box.setText(text)

        self.check_box.stateChanged.connect(self._note.setChecked)
        self.text_box.textChanged.connect(self._note.setText)


    def getNote(self):
        return self._note