from midi.message.ChannelPressureMessage import ChannelPressureMessage
from midi.message.ControllerMessage import ControllerMessage
from midi.message.KeyPressureMessage import KeyPressureMessage
from midi.message.MIDIMessage import parseType, MIDIMessage
from midi.message.NoteStateMessage import NoteStateMessage
from midi.message.PitchMessage import PitchMessage
from midi.message.ProgramChangeMessage import ProgramChangeMessage
from midi.message.QuarterFrameMessage import QuarterFrameMessage
from midi.message.SongPositionPointerMessage import SongPositionPointerMessage
from midi.message.SongSelectMessage import SongSelectMessage
from midi.message.SystemExclusiveMessage import SystemExclusiveMessage
from midi.message.Type import Type


def create(status_byte: int, data1: int = 0, data2: int = 0, data3: int = 0) -> MIDIMessage | None:
    type: Type = parseType(status_byte)

    match type:
        case Type.NOTE_OFF:
            return NoteStateMessage(status_byte, data1, data2, data3)
        case Type.NOTE_ON:
            return NoteStateMessage(status_byte, data1, data2, data3)
        case Type.KEY_PRESSURE:
            return KeyPressureMessage(status_byte, data1, data2, data3)
        case Type.CONTROLLER:
            return ControllerMessage(status_byte, data1, data2, data3)
        case Type.PROGRAM_CHANGE:
            return ProgramChangeMessage(status_byte, data1, data2, data3)
        case Type.CHANNEL_PRESSURE:
            return ChannelPressureMessage(status_byte, data1, data2, data3)
        case Type.PITCH:
            return PitchMessage(status_byte, data1, data2, data3)
        case Type.SYSTEM_EXCLUSIVE:
            return SystemExclusiveMessage(status_byte, data1, data2, data3)
        case Type.MIDI_QUARTER_FRAME:
            return QuarterFrameMessage(status_byte, data1, data2, data3)
        case Type.SONG_POSITION_POINTER:
            return SongPositionPointerMessage(status_byte, data1, data2, data3)
        case Type.SONG_SELECT:
            return SongSelectMessage(status_byte, data1, data2, data3)
        case Type.TUNE_REQUEST:
            return MIDIMessage(status_byte, data1, data2, data3)
        case Type.MIDI_CLOCK:
            return MIDIMessage(status_byte, data1, data2, data3)
        case Type.MIDI_START:
            return MIDIMessage(status_byte, data1, data2, data3)
        case Type.MIDI_CONTINUE:
            return MIDIMessage(status_byte, data1, data2, data3)
        case Type.MIDI_STOP:
            return MIDIMessage(status_byte, data1, data2, data3)
        case Type.ACTIVE_SENSE:
            return MIDIMessage(status_byte, data1, data2, data3)
        case Type.RESET:
            return MIDIMessage(status_byte, data1, data2, data3)
        case _:
            return None