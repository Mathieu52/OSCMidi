from threading import Thread
from time import sleep

from pythonosc import udp_client
from pythonosc.udp_client import UDPClient

from Particle import Particle


class PianoOSC():
    NOTE_START: int = 21
    NOTE_RANGE: int = 108

    PARAMETER_PATH: str = '/avatar/parameters/'
    KEY_PATH: str = PARAMETER_PATH
    PARTICLE_PATH: str = PARAMETER_PATH + 'P'
    RESET_PATH: str = PARAMETER_PATH + 'K1'

    PARTICLE_IN_USE_LIMIT: int = 128

    def __init__(self, IP: str, port: int, limitParticles: bool, particleLimit: int):
        self._stopThreads: bool = False
        self.limitParticles: bool = limitParticles
        self.particleLimit: int = particleLimit

        self._particleList: [Particle] = []
        self._particleUsed: dict[int, bool] = {}

        self.client: UDPClient = udp_client.SimpleUDPClient(IP, port)

        Thread(target=self._particleBufferThread).start()

    def __del__(self):
        self._stopThreads = True

    def hasKey(self, note: int):
        return PianoOSC.NOTE_START <= note <= PianoOSC.NOTE_START + PianoOSC.NOTE_RANGE

    def _adjustNote(self, note: int) -> int:
        return note - PianoOSC.NOTE_START + 1

    def createParticle(self, note, lifetime):
        # Limit particles
        if self.limitParticles and len(self._particleList) >= self.particleLimit:
            return

        if not self.hasKey(note):
            return

        self._particleList.append(Particle(note, lifetime))

    def clearParticles(self):
        self._particleList.clear()
        self._particleUsed.clear()

    def sendParticleState(self, index: int, state: int):
        print(f"sendParticleState {'{'}index: {index}\tstate: {state}{'}'}")
        self.client.send_message(PianoOSC.PARTICLE_PATH + str(index + 1), float(state) / 100.0)

    def _particleBufferThread(self):
        while not self._stopThreads:
            sleep(.01)
            if len(self._particleList) >= 1:
                for i in range(0, PianoOSC.PARTICLE_IN_USE_LIMIT):
                    if i not in self._particleUsed or not self._particleUsed[i]:
                        self._particleUsed[i] = True
                        Thread(target=self._sendParticle, args=(i, self._particleList.pop(0))).start()
                        break
    def _sendParticle(self, index: int, particle: Particle):
        self.sendParticleState(index, self._adjustNote(particle.note))
        sleep(particle.lifetime)

        self.sendParticleState(index, 0)
        sleep(particle.lifetime)

        # Declare that you're done with the particle
        self._particleUsed[index] = False
    def sendKeyState(self, key: int, state: int):
        if not self.hasKey(key):
            return

        print(f"sendKeyState {'{'}key: {key}\tstate: {state}{'}'}")
        self.client.send_message(PianoOSC.PARAMETER_PATH + str(self._adjustNote(key)), state)

    def pressKey(self, key: int):
        self.sendKeyState(key, 1)

    def releaseKey(self, key: int):
        self.sendKeyState(key, 0)

    def resetKeys(self):
        self.client.send_message(PianoOSC.RESET_PATH, 0)
        for key in range(2, 88):
            self.releaseKey(key)
            sleep(.1)

    def setLimitParticles(self, value):
        self.limitParticles = value

    def areParticlesLimited(self):
        return self.limitParticles

    def setParticleLimit(self, limit):
        self.particleLimit = limit

    def getParticleLimit(self):
        return self.particleLimit