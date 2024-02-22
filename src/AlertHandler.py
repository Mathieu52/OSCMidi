import sys
from PySide6.QtWidgets import QApplication, QMessageBox

def show_warning(title, message):
    alert = QMessageBox()
    alert.setWindowTitle(title)
    alert.setText(message)
    alert.setIcon(QMessageBox.Icon.Warning)
    alert.exec_()

def show_info(title, message):
    alert = QMessageBox()
    alert.setWindowTitle(title)
    alert.setText(message)
    alert.setIcon(QMessageBox.Icon.Information)
    alert.exec_()