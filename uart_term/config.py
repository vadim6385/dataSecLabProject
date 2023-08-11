#
# Configuration file
# Copyright (c) 2023 Vadim Darchuk, Yotal Alter, Michael Palas
#
from __future__ import unicode_literals

__version__ = "1.0"

# By default, a thread is used to process the serial port. If this is set to
# False, a timer will poll the serial port at a fixed interval, which can have
# obvious negative side effects of delayed recv.
USE_SERIAL_THREAD = True
