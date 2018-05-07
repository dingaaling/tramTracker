#!/usr/bin/env python3

import os
import numpy as np
import cv2

class TramDiffTracker():
    """Tram Diff Tracker"""

    NONE = "NONE"
    ARRIVING = "ARRIVING"
    DEPARTING = "DEPARTING"

    def __init__(self, threshold=700000):
        """Create a tram diff tracker instance"""
        self._threshold = threshold
        self._detection_count = 0
        self._detection_direction = TramDiffTracker.NONE

    def detect(self, previous_image, current_image):
        # Crop the images to a fixed view
        previous_image = previous_image[125:200, 325:600]
        current_image = current_image[125:200, 325:600]

        diff = cv2.absdiff(previous_image, current_image)
        diff_sum = diff.sum()
        print(diff_sum)

        # If difference from previous frame is above the threshold
        if diff_sum >= self._threshold:
            self._detection_count += 1

            # If this is the first detection in a series calculate its direction
            if self._detection_count == 1:
                self._detection_direction = self._determine_direction(diff)
            
            # If this is the third detection in a series return the direction
            if self._detection_count == 3:
                return self._detection_direction

            # Else return no detection
            return TramDiffTracker.NONE

        # The tram was not detected so clear state
        self._detection_count = 0
        self._detection_direction = TramDiffTracker.NONE
        return TramDiffTracker.NONE

    def _determine_direction(self, diff):
        diff_left = diff[:, :(diff.shape[1] // 2), :]
        diff_right = diff[:, (diff.shape[1] // 2):, :]

        if diff_left.sum() >= diff_right.sum():
            return TramDiffTracker.ARRIVING
        else:
            return TramDiffTracker.DEPARTING