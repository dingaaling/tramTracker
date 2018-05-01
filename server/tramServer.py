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
from tramState import TramState
from tramDiffTracker import TramDiffTracker

def main():
    """Tram Server"""
    try:
        camera = VideoCapture(0)
        serial_bus = None # serial.Serial('/dev/ttyUSB0', 19200)
        image_queue = ImageQueue()
        tram_state = TramState()
        tram_diff_tracker = TramDiffTracker()

        # Run the server loop
        run(camera, serial_bus, image_queue, tram_state, tram_diff_tracker)
    except KeyboardInterrupt:
        pass
    finally:
        camera.release()
        # serial_bus.close()

def run(camera, serial_bus, image_queue, tram_state, tram_diff_tracker):
    # Fill image queue
    print('Focusing the camera...')
    image_count = 0
    while image_count < 10:
        status, image = camera.read()
        if not status:
            continue

        image_count += 1
        time.sleep(1)

    print('Populating the initial image queue...')
    image_count = 0
    while image_count < 1:
        status, image = camera.read()
        if not status:
            continue

        image_queue.enqueue(image)
        image_count += 1
        time.sleep(1)

    print('Starting tram detection...')
    image_count = 0
    while True:
        print('Image Number: %d' % (image_count))

        # Read image from the camera
        status, current_image = camera.read()
        if not status:
            continue

        # Push the image onto the queue
        image_queue.enqueue(current_image)

        # Pull image from the queue
        previous_image = image_queue.dequeue()

        # Leverage the tram diff tracker to detect tram if present (None state returned if not)
        direction = tram_diff_tracker.detect(previous_image, current_image)
        print('Direction: %s' % (direction))

        if direction == TramDiffTracker.ARRIVING:
            # Update tram state for arrival
            tram_state.set_arrival()

            # Write detection image for accuracy testing
            image_name = '%d-ARRIVING.png' % (int(time.time()))
            imwrite(image_name, current_image)

        if direction == TramDiffTracker.DEPARTING:
            # Update tram state for departure
            tram_state.set_departure()

            # Write detection image for accuracy testing
            image_name = '%d-DEPARTING.png' % (int(time.time()))
            imwrite(image_name, current_image)

        status, current_estimate = tram_state.get_wait()
        print('Estimated Wait: %s, %d' % (status, current_estimate))

        # TODO: process data and pass results to update function
        # update_frontend()
        # update_display()

        time.sleep(1)
        image_count += 1

def update_frontend():
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

def update_display():
    pass

if __name__ == '__main__':
    main()