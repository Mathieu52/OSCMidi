from enum import Enum
class Type(Enum):
    UNKNOWN = 0x00
    NOTE_OFF = 0x80
    NOTE_ON = 0x90
    KEY_PRESSURE = 0xA0
    CONTROLLER = 0xB0
    PROGRAM_CHANGE = 0xC0
    CHANNEL_PRESSURE = 0xD0
    PITCH = 0xE0

    # Special type
    SYSTEM_EXCLUSIVE = 0xF0
    MIDI_QUARTER_FRAME = 0xF1
    SONG_POSITION_POINTER = 0xF2
    SONG_SELECT = 0xF3
    TUNE_REQUEST = 0xF6
    MIDI_CLOCK = 0xF8
    MIDI_START = 0xFA
    MIDI_CONTINUE = 0xFB
    MIDI_STOP = 0xFC
    ACTIVE_SENSE = 0xFE
    RESET = 0xFF