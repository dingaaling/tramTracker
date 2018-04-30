#!/usr/bin/env python3

import sys
import time
import json
import serial
import requests
import datetime
import numpy as np
from cv2 import imwrite
from cv2 import VideoCapture
from imageQueue import ImageQueue
from tramBlobTracker import TramBlobTracker
from tramDiffTracker import TramDiffTracker

def main():
    """Tram Server"""
    try:
        camera = VideoCapture(0)
        serial_bus = None # serial.Serial('/dev/ttyUSB0', 19200)
        image_queue = ImageQueue()
        tram_blob_tracker = TramBlobTracker()
        tram_diff_tracker = TramDiffTracker()

        # Run the server loop
        run(camera, serial_bus, image_queue, tram_diff_tracker)
    except KeyboardInterrupt:
        pass
    finally:
        camera.release()
        # serialbus.close()

def run(camera, serial_bus, image_queue, tram_diff_tracker):
    # Fill image queue
    print('Populating initial image queue.')

    image_count = 0
    while image_count < 5:
        status, image = camera.read()
        if not status:
            continue

        image_queue.enqueue(image)
        image_count += 1
        time.sleep(1)

    image_count = 0
    while True:
        print(image_count)
    
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

        detected = tram_diff_tracker.detect(previous_image, current_image)
        print(detected)

        # TODO: write image for testing
        if detected:
            image_name = '%d-detected.png' % (int(time.time()))
            imwrite(image_name, current_image)

        # # TODO: process data and pass results to update function
        # update()

        time.sleep(1)
        image_count += 1

def update():
    time_object = datetime.datetime.now()
    time_value = str(json.dumps(time_object.isoformat()).strip('\"'))

    payload = {}
    payload['departingTime'] = time_value
    payload['arrivingTime'] = time_value
    json_payload = json.dumps(payload, indent=1)
    
    try:
        response = requests.post("http://localhost:8000/update", \
            headers = { u'content-type': u'application/json' }, \
            data=json_payload)

        print('Status: %d' % (response.status_code))
    except Exception:
        print("Connection Refused")

if __name__ == '__main__':
    main()