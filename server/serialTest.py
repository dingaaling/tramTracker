#!/usr/bin/env python3

import sys
import time
import serial

def main():
    """Serial Test"""

    serialbus = serial.Serial('/dev/ttyUSB0', 19200)
    
    try:
        while True:
            serialbus.read() # read a single byte
            serialbus.write(b'NOW,0') # write bytes
            serialbus.write(b'LEAVING,580') # write bytes

            time.sleep(3)

    except KeyboardInterrupt:
        pass
    finally:
        serialbus.close()

if __name__ == '__main__':
    main()