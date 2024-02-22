from abc import ABC, abstractmethod

from PySide6.QtWidgets import QListWidgetItem


class SearchableItem(QListWidgetItem):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_score(self):
        ...

    def __cmp__(self, other):
        return self.get_score() - other.get_score()

    def __lt__(self, other):
        return self.__cmp__(other) > 0
