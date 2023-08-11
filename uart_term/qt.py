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

from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def load_ui_widget(filename, this, custom=None):
    """
    Abstracts out using custom loadUi(), necessary with pySide, or PYQt's
    uic.loadUi().
    """
    uic.loadUi(filename, this)
