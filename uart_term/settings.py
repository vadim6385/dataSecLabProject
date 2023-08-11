#
# settings dialog
# Copyright (c) 2023 Vadim Darchuk, Yotal Alter, Michael Palas
#
import os

import serial
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

import guisave
from utils import load_ui_widget, populate_serial_ports


class SettingsDialog(QDialog):
    """Settings dialog."""

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        load_ui_widget(os.path.join(os.path.dirname(__file__), 'settings.ui'),
                       self)

        try:
            self.port.addItems(populate_serial_ports())
        except EnvironmentError:
            pass

        self.buttonBox.accepted.connect(self.onAccept)

        self.baudrate.setCurrentIndex(self.baudrate.findText("115200"))

        self.bytesize.addItem("5", serial.FIVEBITS)
        self.bytesize.addItem("6", serial.SIXBITS)
        self.bytesize.addItem("7", serial.SEVENBITS)
        self.bytesize.addItem("8", serial.EIGHTBITS)
        self.bytesize.setCurrentIndex(self.bytesize.findText("8"))

        self.parity.addItem("None", serial.PARITY_NONE)
        self.parity.addItem("Even", serial.PARITY_EVEN)
        self.parity.addItem("Odd", serial.PARITY_ODD)
        self.parity.addItem("Mark", serial.PARITY_MARK)
        self.parity.addItem("Space", serial.PARITY_SPACE)
        self.parity.setCurrentIndex(self.parity.findText("None"))

        self.stopbits.addItem("1", serial.STOPBITS_ONE)
        self.stopbits.addItem("1.5", serial.STOPBITS_ONE_POINT_FIVE)
        self.stopbits.addItem("2", serial.STOPBITS_TWO)
        self.stopbits.setCurrentIndex(self.stopbits.findText("1"))

        self.settings = QtCore.QSettings('uart_term', 'uart_term')
        self.settings.beginGroup("settingsDialog")
        guisave.load(self, self.settings)
        self.settings.endGroup()

    def getValues(self):
        """
        Return a dictionary of settings.
        This returns direct attributes of the serial object.
        """
        return {'port': self.port.currentText(),
                'baudrate': int(self.baudrate.currentText()),
                'bytesize': self.bytesize.itemData(self.bytesize.currentIndex()),
                'parity': self.parity.itemData(self.parity.currentIndex()),
                'stopbits': self.stopbits.itemData(self.stopbits.currentIndex()),
                'xonxoff': self.xonxoff.isChecked(),
                'rtscts': self.rtscts.isChecked(),
                'dsrdtr': self.dsrdtr.isChecked()}

    def onAccept(self):
        """Accept changes."""
        self.settings.beginGroup("settingsDialog")
        guisave.save(self, self.settings,
                     ["port", "baudrate", "bytesize", "parity", "stopbits",
                      "xonxoff", "rtscts", "dsrdtr"])
        self.settings.endGroup()
