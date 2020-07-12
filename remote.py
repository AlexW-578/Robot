import os
import sys
import struct

TYPE_KEY = 1
VAL_RELEASE = 0
VAL_PRESS = 1
VAL_REPEAT = 2

keymap = {103: "F", 108: "B", 106: "R", 105: "L", 352: "X"}

dev = sys.argv[1]
print("Using", dev)
ir = os.open(dev, os.O_RDONLY | os.O_NONBLOCK)


def getkey():
    while True:
        try:

            cmd = os.read(ir, 16)

            (type, code, value) = struct.unpack("8xHHI", cmd)

            if type == TYPE_KEY \
                    and (value == VAL_PRESS or value == VAL_REPEAT):
                return keymap.get(code, None)
        except:
            return None
