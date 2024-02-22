from midi.message.MIDIMessage import MIDIMessage


class QuarterFrameMessage(MIDIMessage):
    def __init__(self, status_byte: int, data1: int = 0, data2: int = 0, data3: int = 0):
        super().__init__(status_byte, data1, data2, data3)

    def get_framerate(self):
        high_nibble = (self._data1 & 0xF0) >> 4

        if high_nibble == 7:
            frames_per_second = (self._data1 & 0b00110000) >> 4
            if frames_per_second == 0:
                return 24.0
            elif frames_per_second == 1:
                return 25.0
            elif frames_per_second == 2:
                return 29.97
            elif frames_per_second == 3:
                return 30.0

        return None

    def get_high_nibble(self) -> bool | None:
        high_nibble = (self._data1 & 0xF0) >> 4
        if high_nibble == 7:
            return None

        return high_nibble % 2 == 1

    def get_low_nibble(self) -> int | None:
        high_nibble = (self._data1 & 0xF0) >> 4
        if high_nibble == 7:
            return None

        return self._data1 & 0x0F
