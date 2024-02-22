from midi.message.MIDIMessage import MIDIMessage


class ChannelMessage(MIDIMessage):
    def __init__(self, status_byte: int, data1: int = 0, data2: int = 0, data3: int = 0):
        super().__init__(status_byte, data1, data2, data3)

    def get_channel(self):
        return self._status_byte & 0x0F
