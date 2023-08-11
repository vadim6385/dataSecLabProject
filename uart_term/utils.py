#
# Utilities library
# Copyright (c) 2023 Vadim Darchuk, Yotal Alter, Michael Palas
#
from __future__ import unicode_literals

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt


def load_ui_widget(filename, this):
    """
    uic.loadUi().
    """
    uic.loadUi(filename, this)


class CustomLineEdit(QLineEdit):
    """Custom line edit class that handles special key events."""

    key_event = QtCore.pyqtSignal(int, name='key_event')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
            self.key_event.emit(event.key())
            event.accept()
        else:
            super(CustomLineEdit, self).keyPressEvent(event)


__version__ = "1.0"
