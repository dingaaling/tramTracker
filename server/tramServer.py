#!/usr/bin/env python3

import os
import sys
import time
import json
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
        image_queue = ImageQueue()
        tram_state = TramState()
        tram_diff_tracker = TramDiffTracker()

        # Run the server loop
        run(camera, image_queue, tram_state, tram_diff_tracker)
    except KeyboardInterrupt:
        pass
    finally:
        camera.release()

def run(camera, image_queue, tram_state, tram_diff_tracker):
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
            write_image(current_image, direction)

        if direction == TramDiffTracker.DEPARTING:
            # Update tram state for departure
            tram_state.set_departure()

            # Write detection image for accuracy testing
            write_image(current_image, direction)

        wait_status, wait_value = tram_state.get_wait()
        print('Estimated Wait: %s, %d' % (wait_status, wait_value))

        # TODO: process data and pass results to update function
        update_frontend(wait_status, wait_value)
        # update_display()

        time.sleep(1)
        image_count += 1

def update_frontend(wait_status, wait_value):
    payload = {}
    payload['status'] = wait_status
    payload['countdown'] = wait_value
    json_payload = json.dumps(payload, indent=1)
    
    try:
        response = requests.post("http://localhost:8000/update", \
            headers = { u'content-type': u'application/json' }, \
            data=json_payload)

        print('Update Frontend Status: %d' % (response.status_code))
    except Exception:
        print('Update Frontend Status: Failed')

def write_image(current_image, direction):
    current_time = datetime.datetime.now()
    file_time = current_time.strftime('%d-%m-%Y_%H-%M-%S')
    dashboard_time = current_time.strftime('%d/%m/%Y %H:%M:%S')
    
    # Write detection image for accuracy testing
    image_name = '%s-%s.png' % (file_time, direction)
    image_path = '../dashboard/public/' + image_name
    imwrite(image_path, current_image)

    payload = {}
    payload['time'] = dashboard_time
    payload['direction'] = direction
    payload['name'] = image_name
    json_payload = json.dumps(payload, indent=1)
    
    try:
        response = requests.post("http://localhost:8000/image", \
            headers = { u'content-type': u'application/json' }, \
            data=json_payload)

        print('Update Frontend Image: %d' % (response.status_code))
    except Exception:
        print('Update Frontend Image: Failed')

if __name__ == '__main__':
    main()