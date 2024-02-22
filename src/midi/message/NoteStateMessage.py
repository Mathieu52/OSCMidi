from midi.message.NoteMessage import NoteMessage
from midi.message.NoteState import NoteState
from midi.message.Type import Type


class NoteStateMessage(NoteMessage):
    def __init__(self, status_byte: int, data1: int = 0, data2: int = 0, data3: int = 0):
        super().__init__(status_byte, data1, data2, data3)

    def get_state(self):
        if self._type == Type.NOTE_ON:
            return NoteState.ON
        if self._type == Type.NOTE_OFF:
            return NoteState.OFF

        return NoteState.UNKNOWN

    def get_velocity(self):
        return self._data2 & 0x7F
