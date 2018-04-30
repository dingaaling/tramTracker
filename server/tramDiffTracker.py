#!/usr/bin/env python3

import os
import numpy as np
import cv2

class TramDiffTracker():
    """Tram Diff Tracker"""

    NONE = "NONE"
    ARRIVING = "ARRIVING"
    DEPARTING = "DEPARTING"

    def __init__(self, threshold=900000):
        """Create a tram diff tracker instance"""
        self._threshold = threshold
        self._is_detected = True

    def detect(self, previous_image, current_image):
        # Crop the images to a fixed view
        previous_image = previous_image[125:200, 325:600]
        current_image = current_image[125:200, 325:600]

        diff = cv2.absdiff(previous_image, current_image)
        diff_sum = diff.sum()
        print(diff_sum)

        if diff_sum >= self._threshold and self._is_detected == False:
            # Determain the tram's direction of travel
            self._is_detected = True
            return self._determine_direction(diff)

        self._is_detected = False
        return TramDiffTracker.NONE

    def _determine_direction(self, diff):
        diff_left = diff[:, :(diff.shape[1] // 2), :]
        diff_right = diff[:, (diff.shape[1] // 2):, :]

        if diff_left.sum() >= diff_right.sum():
            return TramDiffTracker.ARRIVING
        else:
            return TramDiffTracker.DEPARTING