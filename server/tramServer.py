#!/usr/bin/env python3

import sys
import pyberrynet

def main():
    """Tram Server"""

    berrynet = pyberrynet.run(warm_up=10, path='/home/pi/repos/BerryNet')
    
    try:
        results = berrynet.upload('picamera')

        if results == None:
            return

        results = results.replace('<br />', '\n')
        results = results.split('\n')

        for result in results:
            if result == None or result == '':
                continue
            
            print(result)

    except KeyboardInterrupt:
        pass
    finally:
        berrynet.close()

if __name__ == '__main__':
    main()
