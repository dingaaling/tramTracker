#!/usr/bin/env python3

import sys
from queue import Queue

class ImageQueue():
    """Image Queue"""

    def __init__(self):
        """Create an image queue instance"""

        self._queue = Queue()

    def enqueue(self, image):
        self._queue.put(image)

    def dequeue(self):
        return self._queue.get()