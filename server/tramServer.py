#!/usr/bin/env python3

import sys
import pyberrynet

def main():
    """Tram Server"""

    berrynet = pyberrynet.run()
    results = berrynet.upload('picamera')
    print(results)
    berrynet.close()

if __name__ == '__main__':
    main()