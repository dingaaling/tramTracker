#!/usr/bin/env python3

import os
import sys
import time
import pyberrynet

def main():
    """Tram Server"""

    berrynet = pyberrynet.run(warm_up=10, path='/home/pi/repos/BerryNet')
    
    try:
        while True:
            os.system()

            results = berrynet.upload('picamera')
            detections = _parse_detections(results)

            print('results:')
            for detection in detections:
                print(detection)

            time.sleep(3)

    except KeyboardInterrupt:
        pass
    finally:
        berrynet.close()

def _parse_detections(results):
    if results == None:
        return list()

    results = results.replace('<br />', '\n')
    results = results.split('\n')

    detections = list()
    for result in results:
        if result == None or result == '':
            continue

        detections.append(list(result.split(' ')))

    return detections

if __name__ == '__main__':
    main()
