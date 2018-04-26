#!/usr/bin/env python3

import sys
import time
import numpy as np
from cv2 import imwrite
from cv2 import VideoCapture
from imageQueue import ImageQueue

def main():
    try:
        run()
    except KeyboardInterrupt:
        pass
    finally:
        pass

def run():
    camera = VideoCapture(0)
    image_queue = ImageQueue()
    
    # Fill image queue
    image_count = 0
    while image_count < 5:
        status, image = camera.read()
        if not status:
            continue

        image_queue.enqueue(image)
        image_count += 1
        time.sleep(1)

    i = 0
    while True:
        print(i)
    
        # Read image from the camera
        status, current_image = camera.read()
        if not status:
            continue

        # Push the image onto the queue
        image_queue.enqueue(current_image)

        # Pull image from the queue
        previous_image = image_queue.dequeue()

        print(current_image.shape)
        print(previous_image.shape)

        # TODO: discuss cropping
        # x = 0
        # y = 0
        # w = 500
        # h = 500
        # cropped_image = image[y:y + h, x: x + w]
        # print(cropped_image.shape)

        # TODO: write image for testing
        image_name = '%d.png' % (int(time.time()))
        imwrite(image_name, current_image)

        time.sleep(1)
        i += 1

if __name__ == '__main__':
    main()
