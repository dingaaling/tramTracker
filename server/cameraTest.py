#!/usr/bin/env python3

import sys
import time
import numpy as np
from cv2 import VideoCapture

def main():
    camera = VideoCapture(0)
    
    for i in range(10):
        print(i)
        return_value, image = camera.read()
        print(return_value)
        print(image.shape)

        time.sleep(1)

if __name__ == '__main__':
    main()
