# Inventory Notes
# I import sys
# from cpu I import everything
# I create a cpu object
# then I run load() and then run()

#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU() # I create a cpu class

cpu.load() # I call the .load() method
cpu.run() # I call the .run() method, this should run some sort of protocol until a halt command is received