from PySide6.QtGui import *
from PySide6.QtCore import *

class PortListModel(QAbstractListModel):
    def __init__(self, ports=[], parent=None):
        super().__init__(parent)
        self._ports = ports

    def rowCount(self, parent):
        return len(self._ports)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            port = self._ports[index.row()]
            return port.getName()
        elif role == Qt.UserRole:
            return self._ports[index.row()]  # Return the Port object as UserRole