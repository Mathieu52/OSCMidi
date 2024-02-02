from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class SeparatorFactory():
    @staticmethod
    def createSeparator(shape: QFrame.Shape):
        separator = QFrame()
        separator.setFrameShape(shape)
        separator.setFrameShadow(QFrame.Shadow.Plain)
        return separator

    @staticmethod
    def createHorizontalSeparator():
        return SeparatorFactory.createSeparator(QFrame.Shape.HLine)

    @staticmethod
    def createVerticalSeparator():
        return SeparatorFactory.createSeparator(QFrame.Shape.VLine)