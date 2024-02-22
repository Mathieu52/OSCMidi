from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class EffectFactory():
    @staticmethod
    def createEffect(target: QObject, color: str, blurRadius: float = 20):
        effect = QGraphicsDropShadowEffect(target)
        effect.setColor(QColor(color))
        effect.setOffset(0, 0)
        effect.setBlurRadius(blurRadius)
        target.setGraphicsEffect(effect)
        return effect