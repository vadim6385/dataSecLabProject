#
# A simple line based GUI serial terminal. This is the main runner file
#
# Copyright (c) 2023 Vadim Darchuk, Yotal Alter, Michael Palas
#

import sys

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow


def main():
    """Create main app and window."""
    app = QApplication(sys.argv)
    app.setApplicationName("UART Terminal")
    win = MainWindow(None)
    win.setWindowTitle("UART Terminal")
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
