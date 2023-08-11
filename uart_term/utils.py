#
# Utilities library
# Copyright (c) 2023 Vadim Darchuk, Yotal Alter, Michael Palas
#
from __future__ import unicode_literals

import glob
import sys

import serial
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


def populate_serial_ports():
    """Gather all serial ports found on system."""
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            ser = serial.Serial(port)
            ser.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def _chunks(text, chunk_size):
    """Chunk text into chunk_size."""
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]


def str_to_hex(text):
    """Convert text to hex encoded bytes."""
    return ''.join('{:02x}'.format(ord(c)) for c in text)


def hex_to_raw(hexstr):
    """Convert a hex encoded string to raw bytes."""
    return ''.join(chr(int(x, 16)) for x in _chunks(hexstr, 2))


def human_size(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if nbytes == 0:
        return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
