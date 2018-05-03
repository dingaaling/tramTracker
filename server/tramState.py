#!/usr/bin/env python3

import sys
import time
import datetime

class TramState():
    """Tram State"""

    UNKNOWN = "UNKNOWN"
    DOCKED = "DOCKED"
    ESTIMATE = "ESTIMATE"

    def __init__(self):
        """Create a tram state instance"""

        self._last_departure = None
        self._last_arrival = None
        self._interval = None
        self._is_docked = False

    def set_arrival(self):
        # Get the current time
        current_time = self._current_time()

        # If the tram is already docked ignore the second tram parking
        if self._is_docked:
            return

        # Set the state
        self._last_arrival = current_time
        self._interval = self._get_tram_interval()
        self._is_docked = True

    def set_departure(self):
        # Get the current time
        current_time = self._current_time()

        # Set the state
        self._last_departure = current_time
        self._interval = self._get_tram_interval()
        self._is_docked = False

    def get_wait(self):
        # Get the current time
        current_time = self._current_time()

        if self._interval == None:
            return TramState.UNKNOWN, -1

        if self._is_docked:
            # Calculate the time the current tram has been docked
            docked_time = current_time - self._last_arrival
            return TramState.DOCKED, docked_time

        # Calculate the next estimated arrival and subtract the current time
        # Note that this means we can have negative arrival times based on delay
        next_departure = self._last_departure + self._interval
        wait_estimate = next_departure - current_time

        return TramState.ESTIMATE, wait_estimate

    def _get_tram_interval(self):
        # Current time is formatted in locale of the service (EST)
        current_datetime = datetime.datetime.now()
        current_time = int(current_datetime.strftime('%H%M%S'))
        current_weekday = int(current_datetime.weekday())
        
        # If the tram is not currently running return no interval
        if self._is_tram_active(current_time, current_weekday) == False:
            return None
        
        # If it is a weekday check for rush hour
        if self._is_tram_rush_hour(current_time, current_weekday):
            # 4 minutes of air time in seconds
            return 240
        
        # 10 minutes of air time in seconds
        return 600

    def _is_tram_active(self, current_time, current_weekday):
        # 6:00am
        opening_time = 60000
        
        # 2:00am
        closing_time = 20000
        
        # Saturday and Sunday mornings (late night)
        if self._is_weekend(current_weekday):
            # 3:30am
            closing_time = 33000
            
        return current_time >= opening_time or current_time < closing_time

    def _is_tram_rush_hour(self, current_time, current_weekday):
        if self._is_weekend(current_weekday):
            return False
        
        # 7:00am
        morning_start_time = 70000
        
        # 10:00am
        morning_end_time = 100000
        
        # 3:00pm
        evening_start_time = 150000
        
        # 8:00pm
        evening_end_time = 200000
        
        # If the current time is within the morning rush hour interval
        if current_time >= morning_start_time and current_time < morning_end_time:
            return True
        
        # If the current time is within the evening rush hour interval
        if current_time >= evening_start_time and current_time < evening_end_time:
            return True
        
        return False

    def _is_weekend(self, current_weekday):
        # If the current weekday is a weekend day
        return current_weekday == 5 or current_weekday == 6

    def _current_time(self):
        return int(time.time())