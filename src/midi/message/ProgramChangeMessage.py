from midi.message.ChannelMessage import ChannelMessage
from midi.message.ProgramChange import ProgramChange


class ProgramChangeMessage(ChannelMessage):
    def __init__(self, status_byte: int, data1: int = 0, data2: int = 0, data3: int = 0):
        super().__init__(status_byte, data1, data2, data3)

    def get_program_change(self) -> ProgramChange:
        return ProgramChange(self._data1 & 0x7F)