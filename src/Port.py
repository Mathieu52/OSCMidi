class Port:
    def __init__(self, name: str, index: int):
        self._name = name
        self._index = index

    def getName(self) -> str:
        return self._name

    def getIndex(self) -> int:
        return self._index

    def toTuple(self):
        return tuple(self._name, self._index)

    def __eq__(self, other):
        if not isinstance(other, Port):
            return False

        if self.getName() != other.getName():
            return False

        if self.getIndex() != other.getIndex():
            return False

        return True

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __str__(self):
        return f"{'{'}name={self.getName()}\t index={self.getIndex()}{'}'}"
