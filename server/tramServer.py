#!/usr/bin/env python3

import os
import sys
import time
from berryNetProvider import BerryNetProvider

def main():
    """Tram Server"""

    berrynet = BerryNetProvider()
    
    try:
        while True:
            results = berrynet.analyze('boardcam')
            detections = _parse_detections(results)

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
