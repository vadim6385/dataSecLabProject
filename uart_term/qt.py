# Copyright (c) 2023 Vadim Darchuk, Yotam Alter, Michael Palas
#
# Based on
#    https://github.com/mfitzp/pyqtconfig/blob/master/pyqtconfig/qt.py
#
# Copyright (c) 2013, Martin Fitzpatrick
# All rights reserved.


from __future__ import unicode_literals
import sys
import os

PYSIDE = 0
PYQT4 = 1
PYQT5 = 2

USE_QT_PY = None

QT_API_ENV = os.environ.get('QT_API')
ETS = dict(pyqt=PYQT4, pyqt4=PYQT4, pyqt5=PYQT5, pyside=PYSIDE)

if QT_API_ENV and QT_API_ENV in ETS:
    USE_QT_PY = ETS[QT_API_ENV]
elif 'PyQt4' in sys.modules:
    USE_QT_PY = PYQT4
elif 'PyQt5' in sys.modules:
    USE_QT_PY = PYQT5
else:
    try:
        import PyQt4
        USE_QT_PY = PYQT4
    except:
        try:
            import PyQt5
            USE_QT_PY = PYQT5
        except ImportError:
            try:
                import PySide
                USE_QT_PY = PYSIDE
            except:
                pass

if USE_QT_PY == PYQT5:
    from PyQt5 import QtGui, QtCore, QtWidgets, uic
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

elif USE_QT_PY == PYSIDE:
    from PySide import QtCore, QtGui, QtUiTools
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import *
    QtCore.pyqtSignal = QtCore.Signal
    QtCore.pyqtSlot = QtCore.Slot

elif USE_QT_PY == PYQT4:
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    from PyQt4 import QtCore, QtGui, uic
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

def load_ui_widget(filename, this, custom=None):
    """
    Abstracts out using custom loadUi(), necessary with pySide, or PYQt's
    uic.loadUi().
    """
    if USE_QT_PY == PYSIDE:
        from pyside_dynamic import loadUi
        loadUi(filename, this, custom)
    else:
        uic.loadUi(filename, this)
