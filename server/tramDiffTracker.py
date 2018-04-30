#!/usr/bin/env python3

import os
import numpy as np
import cv2

class TramDiffTracker():
    """Tram Diff Tracker"""

    def __init__(self, threshold=900000):
        """Create a tram diff tracker instance"""
        self._threshold = threshold

    def detect(self, previous_image, current_image):
        # Crop the images
        previous_image = previous_image[125:200, 325:600]
        current_image = current_image[125:200, 325:600]

        diff = cv2.absdiff(previous_image, current_image)
        diff_sum = diff.sum()
        print(diff_sum)

        if diff_sum >= self._threshold:
            return True

        return False