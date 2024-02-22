from midi.message.MIDIMessage import MIDIMessage


class SongPositionPointerMessage(MIDIMessage):
    def __init__(self, status_byte: int, data1: int = 0, data2: int = 0, data3: int = 0):
        super().__init__(status_byte, data1, data2, data3)

    def get_position(self):
        return ((self._data1 & 0xFF) << 8) | (self._data2 & 0xFF)
