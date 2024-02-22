from midi.message.NoteMessage import NoteMessage
from midi.message.NoteState import NoteState
from midi.message.Type import Type


class KeyPressureMessage(NoteMessage):
    def __init__(self, status_byte: int, data1: int = 0, data2: int = 0, data3: int = 0):
        super().__init__(status_byte, data1, data2, data3)

    def get_note(self):
        return self._data1 & 0x7F

    def get_pressure(self):
        return self._data2 & 0x7F
