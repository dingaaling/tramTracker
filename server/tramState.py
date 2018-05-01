#!/usr/bin/env python3

import sys
import time

class TramState():
    """Tram State"""

    UNKNOWN = "UNKNOWN"
    NOW = "NOW"
    ESTIMATE = "ESTIMATE"

    def __init__(self, buffer_seconds=60):
        """Create a tram state instance"""

        self._last_departure = None
        self._last_arrival = None
        self._interval = None
        self._is_now = False
        self._buffer_seconds = buffer_seconds

    def set_arrival(self):
        # Get the current time
        current_time = self._current_time()

        # If the first arrival detected simply set state
        if self._last_arrival == None:
            self._last_arrival = current_time
            return

        # If the tram arrives twice in a row it is switching scheduals
        # between rush hour and normal operation
        if self._is_now:
            self._last_arrival = current_time
            self._interval = None
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
            return TramState.UNKNOWN, -1

        if self._is_now:
            # Calculate the time the current tram has been docked
            docked_time = current_time - self._last_arrival
            return TramState.NOW, docked_time

        # Calculate the next estimated arrival and subtract the current time
        # Note that this means we can have negative arrival times based on delay
        next_arrival = self._last_arrival + self._interval + self._buffer_seconds
        wait_estimate = next_arrival - current_time

        return TramState.ESTIMATE, wait_estimate

    def _current_time(self):
        return int(time.time())