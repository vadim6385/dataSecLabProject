#
# Main Window
# Copyright (c) 2023 Vadim Darchuk, Yotal Alter, Michael Palas
#
import codecs
import os
import re

import serial
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QMessageBox, QListWidgetItem, QFileDialog, QDialog
from pkg_resources import parse_version

import guisave
from config import USE_SERIAL_THREAD, __version__
from settings import SettingsDialog
from utils import load_ui_widget, populate_serial_ports, str_to_hex, hex_to_raw, human_size

if USE_SERIAL_THREAD:
    import serialthread

class MainWindow(QMainWindow):
    """The main window."""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        load_ui_widget(os.path.join(os.path.dirname(__file__), 'uart_term.ui'), self)
        self.serial = None
        self.rx = 0
        self.tx = 0
        self.history_index = 0

        self.statusBar().showMessage("Not connected")

        ports = []
        try:
            ports = populate_serial_ports()
        except EnvironmentError:
            pass

        if not len(ports):
            self.statusBar().showMessage(
                'No serial ports found.  You can try manually entering one.')

        self.btn_open.clicked.connect(self.onBtnOpen)
        self.btn_send.clicked.connect(self.onBtnSend)
        self.input.returnPressed.connect(self.onBtnSend)
        self.input.textChanged.connect(self.onInputChanged)
        self.line_end.currentIndexChanged.connect(self.onInputChanged)
        self.btn_clear.clicked.connect(self.onBtnClear)
        self.btn_open_log.clicked.connect(self.onBtnOpenLog)
        self.actionQuit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.onAbout)
        self.history.itemDoubleClicked.connect(self.onHistoryDoubleClick)

        self.input.setEnabled(False)
        self.btn_send.setEnabled(False)
        self.history.setEnabled(False)

        self.rxtx = QLabel("TX: 0 B  RX: 0 B")
        self.statusBar().addPermanentWidget(self.rxtx)

        self.settings = QtCore.QSettings('uart_term', 'uart_term')
        self.settings.beginGroup("mainWindow")
        guisave.load(self, self.settings)
        self.settings.endGroup()

        self.ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        if parse_version(serial.VERSION) >= parse_version("3.0"):
            self.serial = serial.Serial(timeout=0.1,
                                        write_timeout=5.0,
                                        inter_byte_timeout=1.0)
        else:
            self.serial = serial.Serial(timeout=0.1,
                                        writeTimeout=5.0,
                                        interCharTimeout=1.0)
        if not USE_SERIAL_THREAD:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.doReadData)
        else:
            self.thread = serialthread.SerialThread(self.serial)
            self.thread.recv.connect(self.recv)
            self.thread.recv_error.connect(self.onRecvError)

        self.input.key_event.connect(self.onInputKey)

    def uiConnectedEnable(self, connected):
        """Toggle enabled on controls based on connect."""
        if connected:
            self.btn_open.setText("&Close Device")
            self.onInputChanged()
        else:
            self.btn_open.setText("&Open Device")
            self.btn_send.setEnabled(connected)
        self.input.setEnabled(connected)
        self.history.setEnabled(connected)

    def onBtnOpen(self):
        """Open button clicked."""
        if self.serial.isOpen():
            if not USE_SERIAL_THREAD:
                self.timer.stop()
                self.serial.close()
            else:
                self.thread.close()
            self.uiConnectedEnable(False)
            self.statusBar().showMessage("Not connected")
        else:
            dlg = SettingsDialog(self)
            if dlg.exec_():
                settings = dlg.getValues()
                for key in settings:
                    setattr(self.serial, key, settings[key])
            else:
                return

            try:
                self.serial.open()
            except serial.SerialException as exp:
                QMessageBox.critical(self, 'Error Opening Serial Port',
                                     str(exp))
            except (IOError, OSError) as exp:
                QMessageBox.critical(self, 'IO Error Opening Serial Port',
                                     str(exp))
            else:
                if parse_version(serial.VERSION) >= parse_version("3.0"):
                    self.serial.reset_input_buffer()  # pylint: disable=no-member
                    self.serial.reset_output_buffer()  # pylint: disable=no-member
                else:
                    self.serial.flushInput()  # pylint: disable=no-member
                    self.serial.flushOutput()  # pylint: disable=no-member
                self.statusBar().showMessage('Connected to ' + settings['port'] +
                                             ' ' +
                                             str(settings['baudrate']) + ',' +
                                             str(settings['parity']) + ',' +
                                             str(settings['bytesize']) + ',' +
                                             str(settings['stopbits']))
                self.uiConnectedEnable(True)
                if not USE_SERIAL_THREAD:
                    self.timer.start(100)
                else:
                    self.thread.start()

    def doLog(self, text):
        """Write to log file."""
        text = text.decode("utf-8", 'backslashreplace')
        if self.remove_escape.isChecked():
            text = self.ansi_escape.sub('', text)
        if self.output_hex.isChecked():
            text = str_to_hex(text)
            text = ' '.join(a + b for a, b in zip(text[::2], text[1::2]))
            text = text + ' '

        cursor = self.log.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        if not self.lock.isChecked():
            self.log.moveCursor(QtGui.QTextCursor.End)

        if self.enable_log.isChecked() and len(self.log_file.text()):
            with open(self.log_file.text(), "a") as handle:
                handle.write(text)

    def encodeInput(self):
        """
        Interpret the user input text as hex or append appropriate line ending.
        """
        endings = [u"\n", u"\r", u"\r\n", u"\n\r", u"", u""]
        text = self.input.text()

        if self.line_end.currentText() == "Hex":
            text = ''.join(text.split())
            if len(text) % 2:
                raise ValueError('Hex encoded values must be a multiple of 2')
            text = hex_to_raw(text)
        else:
            text = text + endings[self.line_end.currentIndex()]
        return text.encode()

    def onInputChanged(self):
        """Input line edit changed."""
        try:
            self.encodeInput()
        except ValueError:
            self.input.setStyleSheet("color: rgb(255, 0, 0);")
            self.btn_send.setEnabled(False)
            return
        self.input.setStyleSheet("color: rgb(0, 0, 0);")
        if self.serial is not None and self.serial.isOpen():
            self.btn_send.setEnabled(True)

    def onInputKey(self, key):
        """Input line edit key pressed."""
        if key == Qt.Key_Up:
            if self.history_index > 0:
                self.history_index -= 1
                item = self.history.item(self.history_index)
                self.input.setText(item.text())
        elif key == Qt.Key_Down:
            if self.history_index < self.history.count():
                self.history_index += 1
                if self.history_index == self.history.count():
                    self.input.setText("")
                else:
                    item = self.history.item(self.history_index)
                    self.input.setText(item.text())

    def onBtnSend(self):
        """Send button clicked."""
        if not self.serial.isOpen():
            return
        try:
            raw = self.encodeInput()
            if not USE_SERIAL_THREAD:
                ret = self.serial.write(raw)
            else:
                ret = self.thread.write(raw)
            self.tx = self.tx + ret
            self.rxtx.setText("TX: " + human_size(self.tx) + "  RX: " +
                              human_size(self.rx))
        except serial.SerialException as exp:
            QMessageBox.critical(self, 'Serial write error', str(exp))
            return
        except ValueError as exp:
            QMessageBox.critical(self, 'Input Error', str(exp))
            return

        if self.echo_input.isChecked():
            self.doLog(raw)

        if len(self.input.text()):
            item = QListWidgetItem(self.input.text())
            self.history.addItem(item)
            self.history.scrollToItem(item)
            self.history_index = self.history.count()

        self.input.clear()

    def onBtnOpenLog(self):
        """Open log file button clicked."""
        dialog = QFileDialog(self)
        dialog.setWindowTitle('Open File')
        dialog.setNameFilter("All files (*.*)")
        dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.selectedFiles()[0]
            self.log_file.setText(filename)

    def onHistoryDoubleClick(self, item):
        """Send log item double clicked."""
        self.input.setText(item.text())
        self.onBtnSend()

    def onBtnClear(self):
        """Clear button clicked."""
        self.log.clear()

    def doReadData(self):
        """Read serial port."""
        if self.serial.isOpen:
            try:
                text = self.serial.read(2048)
            except serial.SerialException as exp:
                QMessageBox.critical(self, 'Serial read error', str(exp))
            else:
                self.recv(text)

    def recv(self, text):
        """Receive data from the serial port signal."""
        if len(text):
            size = len(text)
            self.rx = self.rx + size
            self.rxtx.setText("TX: " + human_size(self.tx) + "  RX: " +
                              human_size(self.rx))
            self.doLog(text)

    def onRecvError(self, error):
        """Receive error when reading serial port from signal."""
        QMessageBox.critical(self, 'Serial read error', error)
        self.onBtnOpen()

    def onAbout(self):
        """About menu clicked."""
        msg = QMessageBox(self)
        image = QImage(":/icons/32x32/uart_term.png")
        pixmap = QPixmap(image).scaledToHeight(32,
                                               Qt.SmoothTransformation)
        msg.setIconPixmap(pixmap)
        msg.setInformativeText("Copyright (c) 2023 Vadim Darchuk, Yotam Alter, Michael Palas")
        msg.setWindowTitle("UART Terminal " + __version__)
        with codecs.open(os.path.join(os.path.dirname(__file__), 'LICENSE.txt'),
                         encoding='utf-8') as f:
            msg.setDetailedText(f.read())
        msg.setText(
            "<p><b>UART Terminal</b> is a simple line based serial terminal GUI"
            " written in Python. This is a tool that's useful for talking to a"
            " variety of serial based hardware that can involve custom protocols"
            " or just a standard command line interface.  It runs on anything"
            " that supports Python and Qt.")

        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def closeEvent(self, unused_event):
        """Handle window close event."""
        _ = unused_event
        if not USE_SERIAL_THREAD:
            self.timer.stop()
            self.serial.close()
        else:
            self.thread.close()
        self.settings.beginGroup("mainWindow")
        guisave.save(self, self.settings,
                     ["ui", "remove_escape",
                      "echo_input", "log_file", "enable_log", "line_end",
                      "splitter", "output_hex"])
        self.settings.endGroup()
