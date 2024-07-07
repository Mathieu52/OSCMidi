import math,re,os
from threading import Thread
from time import sleep
from typing import cast

import rtmidi
from PySide6.QtCore import QThread, Signal, QTimer
from rtmidi import MidiIn

import AlertHandler
from Port import Port
from PianoOSC import PianoOSC
from midi.message import Type
from ui.OSCMidiWidget import OSCMidiWidget

class OSCMidiController:

    Port_DEFAULT_VALUE: int = 9000
    IP_DEFAULT_VALUE: str = '127.0.0.1'

    def __init__(self, oscmidi_widget: OSCMidiWidget, IP: str = IP_DEFAULT_VALUE):
        self.oscmidi_widget = oscmidi_widget

        self._midi_in = rtmidi.MidiIn()
        self._midi_out = rtmidi.MidiOut()

        self._midi_in.ignore_types(False, False, False)

        self.list_of_output_ports: [Port] = None
        self.list_of_input_ports: [Port] = None

        self.IP: str = IP
        self.port: int = OSCMidiController.Port_DEFAULT_VALUE
        self._piano: PianoOSC = None

        self.connectUI()
        self._ports_thread: QTimer = QTimer()
        self._ports_thread.timeout.connect(self.resfreshAvailablePorts)
        self._ports_thread.start(1000)

    def connectUI(self):
        self.oscmidi_widget.on_selected_input_change += lambda input: self.openInputPort(input)
        self.oscmidi_widget.on_selected_output_change += lambda output: self.openOutputPort(output)
        self.oscmidi_widget.on_start += self.start
        self.oscmidi_widget.on_stop += self.stop

    def openInputPort(self, input_port: Port):
        if input_port is not None and input_port.getIndex() >= 0 and input_port.getName() != 'None':
            if self._midi_in is not None:
                self._midi_in.close_port()

            try:
                self._midi_in.open_port(input_port.getIndex())
                return
            except:
                self._midi_in.close_port()
                AlertHandler.show_warning('Device is not available',
                                          "Device ({input_port.getName()}) is currently in use, make sure it's not")
                self.oscmidi_widget.resetSelectedInput()
                return
        else:
            self._midi_out.close_port()
            self.oscmidi_widget.stop()

    def openOutputPort(self, output_port: Port):
        if output_port is not None and output_port.getIndex() >= 0:
            if self._midi_out is not None:
                self._midi_out.close_port()

            try:
                self._midi_out.open_port(output_port.getIndex())
                return
            except:
                self._midi_out.close_port()
                AlertHandler.show_warning('Device is not available',
                                          f"An issue has occurred while trying to connect to device:\n{output_port.getName()}")
                self.oscmidi_widget.resetSelectedOutput()
                return
        else:
            self._midi_out.close_port()
            self.oscmidi_widget.stop()

    @staticmethod
    def isInputAvailable(portNumber):
        try:
            pass
            #pygame.midi.Input(portNumber).close()
        except:
            return False

        return True

    @staticmethod
    def isOutputAvailable(portNumber):
        try:
            pass
            # pygame.midi.Output(portNumber).close()
        except:
            return False

        return True

    def simulateKey(self, midi_message):
        if Type(midi_message[0]) == Type.RESET:
            self._piano.resetKeys()
            self._piano.clearParticles()
            return

        type: Type = Type(midi_message[0] & 0xF0)

        if not type == Type.NOTE_OFF and not type == Type.NOTE_ON:
            return

        velocity: int = midi_message[2] & 0x7F
        note: int = midi_message[1] & 0x7F

        if type == Type.NOTE_ON:
            print("NOTE_ON")
        elif type == Type.NOTE_OFF:
            print("NOTE_OFF")
        print("NOTE: ", note)
        print("VELOCITY: ", velocity)

        if not self._piano.hasKey(note):
            return

        if type == Type.NOTE_ON:
            if self.oscmidi_widget.areParticlesEnabled():
                self._piano.createParticle(note, self.oscmidi_widget.getParticleLifeTime())
            self._piano.pressKey(note)
        elif type == Type.NOTE_OFF or velocity == 0:
            self._piano.releaseKey(note)


    ########Thread Functions############

    def MainThread(self):
        print("Now listening to note events on " + str(self._midi_in) + "...")
        while self.oscmidi_widget.isRunning():
            if self._midi_in.is_port_open():
                message = self._midi_in.get_message()

                if message:
                    if self._midi_out.is_port_open():
                        self._midi_out.send_message(message[0])

                    try:
                        self.simulateKey(message[0])
                    except OSError:
                        AlertHandler.show_warning("OSC Client issue", "Start OSC Client first")
                        self.oscmidi_widget.stop()
                else:
                    sleep(0.01)



        print("Closed threads, not listening anymore")

    ########Initalize UI Funcs############

    def start(self):
        self.startOSCClient()

        if not self._piano:
            AlertHandler.show_warning("OSC Client issue", "Start OSC Client first")
            self.oscmidi_widget.stop()
            return

        if not self._midi_in.is_port_open():
            AlertHandler.show_warning("Input port issue", "Select an input port")
            self.oscmidi_widget.stop()
            return

        self.startThreads()

    @staticmethod
    def clearMidiInputPort(input_port: MidiIn):
        if input_port.is_port_open():
            while input_port.get_message():
                continue


    def stop(self):
        # Cleanup
        if self._midi_in.is_port_open():
            OSCMidiController.clearMidiInputPort(self._midi_in)

    def startThreads(self):
        Thread(target=self.MainThread).start()

    def startOSCClient(self):
        if self._piano is None:
            self._piano = PianoOSC(self.IP, self.port, self.oscmidi_widget.areParticlesLimited(), self.oscmidi_widget.getParticleLimit())

    def resfreshAvailablePorts(self):
        self.list_of_input_ports = []
        self.list_of_output_ports = [Port('None', -2)]

        if self.oscmidi_widget.isInputSelectorOpened() or self.oscmidi_widget.isOutputSelectorOpened():
            return

        for i in range(self._midi_in.get_port_count()):
            try:
                self.list_of_input_ports.append(Port(self._midi_in.get_port_name(i), i))
            except Exception as e:
                print(f"Error while adding input port: {e}")

        for i in range(self._midi_out.get_port_count()):
            try:
                self.list_of_output_ports.append(Port(self._midi_out.get_port_name(i), i))
            except Exception as e:
                print(f"Error while adding output port: {e}")

        self.oscmidi_widget.setAvailableInputs(self.list_of_input_ports)
        self.oscmidi_widget.setAvailableOutputs(self.list_of_output_ports)