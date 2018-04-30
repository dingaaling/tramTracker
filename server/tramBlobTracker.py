#!/usr/bin/env python3

import os
import numpy as np
import cv2

class TramBlobTracker():
    """Tram Blob Tracker"""

    def __init__(self):
        """Create a tram blob tracker instance"""
        
        # Setup SimpleBlobDetector parameters
        self._params = cv2.SimpleBlobDetector_Params()
        
        # Change thresholds
        self._params.minThreshold = 10
        self._params.maxThreshold = 200
        
        # Filter by Area.
        self._params.filterByArea = True
        self._params.minArea = 1000
        
        # Filter by Circularity
        self._params.filterByCircularity = True
        self._params.minCircularity = 0.1
        
        # Filter by Convexity
        self._params.filterByConvexity = False
        self._params.minConvexity = 0.87
        
        # Filter by Inertia
        self._params.filterByInertia = False
        self._params.minInertiaRatio = 0.01

        # Setup SimpleBlobDetector detector
        self._detector = cv2.SimpleBlobDetector_create(self._params)

    def _find_keypoint(self, image):
        # Image crop/filtering
        image = image[100:250, 100:800]
        image = cv2.GaussianBlur(image, (3, 3), 0)

        # Detect blobs
        keypoints = self._detector.detect(image)

        # Extract keypoint info
        if len(keypoints) > 0:
            x, y = keypoints[0].pt[0],keypoints[0].pt[1]
            size = keypoints[0].size

            return x, y, size

        return None