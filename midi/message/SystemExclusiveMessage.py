from midi.message.Manufacturer import Manufacturer
from midi.message.MIDIMessage import MIDIMessage


class SystemExclusiveMessage(MIDIMessage):
    def __init__(self, status_byte: int, data1: int = 0, data2: int = 0, data3: int = 0):
        super().__init__(status_byte, data1, data2, data3)

    def getManufacturer(self):
        return Manufacturer(self._data1 & 0x7F)

    def getMessage(self):
        return [self._data2, self._data3]