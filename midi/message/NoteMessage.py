from midi.message.ChannelMessage import ChannelMessage


class NoteMessage(ChannelMessage):
    def __init__(self, status_byte: int, data1: int = 0, data2: int = 0, data3: int = 0):
        super().__init__(status_byte, data1, data2, data3)

    def get_note(self):
        return self._data1 & 0x7F
