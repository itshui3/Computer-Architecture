# Inventory Notes
# I import sys
# from cpu I import everything
# I create a cpu object
# then I run load() and then run()
import os
#!/usr/bin/env python3
programs = {
    'print8': [],
    'mult': []
}

with open(os.path.abspath("ls8/print8.ls8"), 'r') as program:
    for p in program:
        byte = ''
        for c in p:
            if c != str(1) and c != str(0):
                break
            else:
                byte = byte + c
        if len(byte) > 0:
            programs['print8'].append(int(byte, 2))
with open(os.path.abspath("ls8/mult.ls8"), 'r') as mult:
    for p in mult:
        byte = ''
        for c in p:
            if c != str(1) and c != str(0):
                break
            else:
                byte = byte + c
        if len(byte) > 0:
            programs['mult'].append(int(byte, 2))

"""Main."""
if __name__ == "__main__":

    import sys
    from cpu import *

    cpu = CPU() # I create a cpu class

    cpu.load(programs[sys.argv[1]]) # I call the .load() method
    params = []
    if len(sys.argv) > 2: params = sys.argv[2:]

    cpu.run(params)
