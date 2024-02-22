import difflib
from typing import Sequence

from PySide6.QtWidgets import QListWidgetItem
from events import Events

from ui.searchable.SearchableItem import SearchableItem

import Levenshtein as levenshtein


class Note(SearchableItem, Events):
    __events__ = ('on_state_change', 'on_text_change', 'on_change')

    def __init__(self, checked: bool, text: str):
        super(Note, self).__init__()
        self._checked = checked
        self._text = text

        self._search_string_function = None

        self.on_state_change += self.on_change
        self.on_text_change += self.on_change

    def setChecked(self, checked: bool):
        if bool(self._checked) == bool(checked):
            return

        self._checked = bool(checked)
        self.on_state_change(checked)

    def setText(self, text: str):
        if self._text == text:
            return

        self._text = text
        self.on_text_change(text)

    def isChecked(self) -> bool:
        return bool(self._checked)

    def getText(self) -> str:
        return self._text

    def setSearchStringFunction(self, search):
        self._search_string_function = search

    def get_score(self):
        if self._search_string_function is not None:
            return levenshtein.ratio(self._search_string_function(), self.getText())




