from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QPushButton


class OrientablePushButton(QPushButton):
    class Orientation:
        Horizontal = 0
        VerticalTopToBottom = 1
        VerticalBottomToTop = 2

    def __init__(self, parent=None, text="", icon=None):
        super().__init__(text, parent)
        if icon is not None:
            self.setIcon(icon)
        self.mOrientation = self.Orientation.Horizontal

    def sizeHint(self):
        return QSize(100, 30)  # You may adjust the size as needed

    def orientation(self):
        return self.mOrientation

    def setOrientation(self, orientation):
        self.mOrientation = orientation

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.mOrientation == self.Orientation.Horizontal:
            # Implement horizontal painting logic
            pass
        elif self.mOrientation == self.Orientation.VerticalTopToBottom:
            # Implement vertical top to bottom painting logic
            pass
        elif self.mOrientation == self.Orientation.VerticalBottomToTop:
            # Implement vertical bottom to top painting logic
            pass
