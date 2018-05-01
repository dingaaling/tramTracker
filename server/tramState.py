#!/usr/bin/env python3

import sys
import time

class TramState():
    """Tram State"""

    UNKNOWN = "UNKNOWN"
    NOW = "NOW"
    ESTIMATE = "ESTIMATE"

    def __init__(self):
        """Create a tram state instance"""

        self._last_departure = None
        self._last_arrival = None
        self._interval = None
        self._is_now = False

    def set_arrival(self):
        # Get the current time
        current_time = self._current_time()

        # If the first arrival detected simply set state
        if self._last_arrival == None:
            self._last_arrival = current_time
            return

        # Set the state
        self._interval = current_time - self._last_arrival
        self._last_arrival = current_time
        self._is_now = True

    def set_departure(self):
        # Get the current time
        current_time = self._current_time()

        # Set the state
        self._last_departure = current_time
        self._is_now = False

    def get_wait(self):
        # Get the current time
        current_time = self._current_time()

        if self._interval == None:
            return TramState.UNKNOWN, 0

        if self._is_now:
            return TramState.NOW, 0

        # Calculate the next estimated arrival and subtract the current time
        # Note that this means we can have negative arrival times based on delay
        next_arrival = self._last_arrival + self._interval
        wait_estimate = next_arrival - current_time

        return TramState.ESTIMATE, wait_estimate

    def _current_time(self):
        return int(time.time())