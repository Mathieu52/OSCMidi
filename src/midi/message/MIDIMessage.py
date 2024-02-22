from midi.message.Type import Type

class MIDIMessage:
    def __init__(self, status_byte: int, data1: int = 0, data2: int = 0, data3: int = 0):
        self._type: Type = parseType(status_byte)
        self._status_byte = status_byte
        self._data1 = data1
        self._data2 = data2
        self._data3 = data3

    def get_type(self):
        return self._type


def parseType(status_byte: int) -> Type:
    if status_byte < 0x80 or status_byte > 0xFF:
        return Type.UNKNOWN
    elif status_byte < 0xF0:
        code: int = status_byte & 0xF0
        return Type(code)
    else:
        return Type(status_byte)